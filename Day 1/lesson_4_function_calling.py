"""
Lesson 4: Azure OpenAI Function Calling Feature
================================================

Learn how to use OpenAI's function calling to build flexible AI systems.

This script demonstrates:
- Defining functions as JSON schemas
- Letting AI decide when to call functions
- Executing function suggestions
- Building the tool loop
- Creating custom integrations
- Handling multiple function calls

Author: Saurabh Shirgaokar
Date: 2026
Level: Advanced

What This Does:
- Shows how AI "suggests" function calls
- You decide when to execute
- You handle the results
- You feed results back to AI
- Full transparency and control

This is the foundation of:
- LangChain agents (they use this under the hood)
- Custom AI systems
- Production AI applications
- Flexible integrations
"""

# ============================================================================
# STEP 1: SETUP AND IMPORTS
# ============================================================================
"""
Import the native OpenAI client (not LangChain).

Key difference from previous lessons:
- Direct OpenAI client = lower level
- Full control and transparency
- See exactly what happens
- Understand the mechanism
"""

import os
from openai import AzureOpenAI
import json
from sqlalchemy import create_engine, text
import pandas as pd

print("="*70)
print("STEP 1: SETUP")
print("="*70)

# Create Azure OpenAI client (direct, not wrapped)
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15"
)

print("✓ Connected to Azure OpenAI")
print("✓ Using native OpenAI client (not LangChain)")
print("✓ Full control over function calling loop\n")


# ============================================================================
# EXAMPLE 1: SIMPLE WEATHER FUNCTIONS
# ============================================================================
"""
Example 1 shows the basic function calling pattern with a weather API.

Key concepts:
- Define Python function
- Define JSON schema for AI
- AI suggests function calls
- You execute them
"""

print("="*70)
print("EXAMPLE 1: WEATHER FUNCTION CALLING")
print("="*70)

# Step 1: Define Python function (real implementation)
def get_current_weather(location, unit="fahrenheit"):
    """
    Get the current weather in a given location.
    
    Args:
        location (str): City and state, e.g. "San Francisco, CA"
        unit (str): Temperature unit - "fahrenheit" or "celsius"
    
    Returns:
        str: JSON string with weather data
    
    Note: This is mock data for demonstration
    """
    
    # Mock weather data for different cities
    weather_data = {
        "new york": {"temperature": "40", "condition": "cloudy"},
        "san francisco": {"temperature": "50", "condition": "clear"},
        "las vegas": {"temperature": "70", "condition": "sunny"},
    }
    
    # Find matching city
    location_lower = location.lower()
    found_weather = None
    
    for city, weather in weather_data.items():
        if city in location_lower:
            found_weather = weather
            break
    
    # Return as JSON string (important!)
    if found_weather:
        return json.dumps({
            "location": location,
            "temperature": found_weather["temperature"],
            "condition": found_weather["condition"],
            "unit": unit
        })
    else:
        return json.dumps({
            "location": location,
            "temperature": "unknown",
            "condition": "data not available"
        })


# Test the function
print("\nTesting Python function:")
result = get_current_weather("New York")
print(f"  Result: {result}")
print(f"  Type: {type(result)} (JSON string, not dict)\n")


# Step 2: Define tools for AI (JSON schema)
"""
This is the CRUCIAL step. AI doesn't know how to call the function.
Instead, we give it a description so it can decide WHEN to call it.
"""

tools = [
    {
        "type": "function",
        "function": {
            # Function name (must match Python function)
            "name": "get_current_weather",
            
            # Description for AI (help AI understand what this does)
            "description": "Get the current weather in a given location. "
                          "The default unit when not specified is fahrenheit",
            
            # Parameters (what does this function accept)
            "parameters": {
                "type": "object",
                "properties": {
                    # Parameter 1: location
                    "location": {
                        "type": "string",
                        "description": "The city and state, "
                                      "e.g. San Francisco, CA"
                    },
                    # Parameter 2: unit (optional)
                    "unit": {
                        "type": "string",
                        "enum": ["fahrenheit", "celsius"],
                        "description": "The temperature unit. "
                                      "Default is fahrenheit"
                    }
                },
                # Which parameters are required
                "required": ["location"]
            }
        }
    }
]

print("Tool definition created:")
print("  - Function: get_current_weather")
print("  - Parameters: location (required), unit (optional)")
print("  - AI can now decide when to call this\n")


# Step 3: Prepare user message
messages = [
    {
        "role": "user",
        "content": "What's the weather in San Francisco, New York, and Las Vegas?"
    }
]

print("User question:")
print(f"  '{messages[0]['content']}'\n")


# Step 4: FIRST API CALL - Get function suggestions
"""
Key insight: AI doesn't execute the function here.
AI just SUGGESTS calling it and what arguments to use.
This is the crucial difference from LangChain agents!
"""

print("FIRST API CALL: Ask AI what functions to call")
print("-" * 70)

response = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages,
    tools=tools,  # Available tools
    tool_choice="auto",  # Let AI decide whether to call functions
)

# Extract AI's response
response_message = response.choices[0].message
tool_calls = response_message.tool_calls

print(f"AI Response: 'I need to call functions'")
print(f"Number of function calls: {len(tool_calls) if tool_calls else 0}\n")

if tool_calls:
    print("Function calls suggested by AI:")
    for i, tool_call in enumerate(tool_calls, 1):
        print(f"\n  Call {i}:")
        print(f"    Function: {tool_call.function.name}")
        print(f"    Arguments: {tool_call.function.arguments}")
        print(f"    Call ID: {tool_call.id}")


# Step 5: Execute suggested functions
"""
Key insight: WE decide when and how to execute.
WE handle the errors.
WE format the results.
This is full control!
"""

print("\n" + "="*70)
print("STEP 2: EXECUTE SUGGESTED FUNCTIONS")
print("="*70)

# Map function names to actual Python functions
available_functions = {
    "get_current_weather": get_current_weather
}

# Add AI's suggestion to message history (IMPORTANT!)
messages.append(response_message)

print("\nExecuting functions...\n")

for tool_call in tool_calls:
    function_name = tool_call.function.name
    
    print(f"Executing: {function_name}")
    
    # Get the actual Python function
    function_to_call = available_functions[function_name]
    
    # Parse arguments (they're JSON strings!)
    function_args = json.loads(tool_call.function.arguments)
    print(f"  Arguments: {function_args}")
    
    # Actually call the function
    function_response = function_to_call(**function_args)
    print(f"  Result: {function_response}\n")
    
    # Add result to message history (CRUCIAL!)
    messages.append({
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": function_response
    })

print("All functions executed and results added to history")


# Step 6: SECOND API CALL - Get final answer
"""
Now AI has the function results.
AI uses them to provide the final answer.
"""

print("\n" + "="*70)
print("STEP 3: SECOND API CALL - GET FINAL ANSWER")
print("="*70)

second_response = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages  # Includes question + function suggestions + results
)

final_answer = second_response.choices[0].message.content

print("\nFinal Answer from AI:")
print(f"  {final_answer}\n")


# ============================================================================
# EXAMPLE 2: DATABASE FUNCTION CALLING
# ============================================================================
"""
Example 2 shows function calling with database queries.

This demonstrates:
- Connecting to database
- Creating functions that query it
- AI suggesting database queries
- You executing them
- AI using results
"""

print("\n" + "="*70)
print("EXAMPLE 2: DATABASE FUNCTION CALLING")
print("="*70)

# Setup database connection
print("\nSetting up COVID database...")

database_file_path = "./db/test.db"

# Load data and create database (from previous lessons)
try:
    df = pd.read_csv("./data/all-states-history.csv").fillna(value=0)
    engine = create_engine(f'sqlite:///{database_file_path}')
    df.to_sql('all_states_history', con=engine, if_exists='replace', index=False)
    print("✓ Database created/updated")
except Exception as e:
    print(f"✗ Database setup failed: {e}")
    print("  Continuing with examples anyway...\n")


# Step 1: Define database query functions
def get_hospitalized_increase_for_state_on_date(state_abbr, specific_date):
    """
    Get hospitalized increase for a state on a specific date.
    
    Args:
        state_abbr (str): State abbreviation, e.g. 'AK', 'NY'
        specific_date (str): Date in 'YYYY-MM-DD' format
    
    Returns:
        str: JSON string with results
    """
    
    try:
        engine = create_engine(f'sqlite:///{database_file_path}')
        
        with engine.connect() as connection:
            # SQL query
            query = text("""
                SELECT date, hospitalizedIncrease
                FROM all_states_history
                WHERE state = :state AND date = :date
            """)
            
            result = connection.execute(
                query,
                {"state": state_abbr, "date": specific_date}
            ).fetchone()
        
        if result:
            return json.dumps({
                "date": result[0],
                "hospitalizedIncrease": result[1],
                "state": state_abbr
            })
        else:
            return json.dumps({
                "date": specific_date,
                "hospitalizedIncrease": 0,
                "state": state_abbr,
                "note": "No data found"
            })
    
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_total_cases_for_state_in_month(state_abbr, year_month):
    """
    Get total cases for a state in a specific month.
    
    Args:
        state_abbr (str): State abbreviation, e.g. 'AK', 'NY'
        year_month (str): Month in 'YYYY-MM' format
    
    Returns:
        str: JSON string with results
    """
    
    try:
        engine = create_engine(f'sqlite:///{database_file_path}')
        
        with engine.connect() as connection:
            query = text("""
                SELECT SUM(cases) as total_cases
                FROM all_states_history
                WHERE state = :state AND date LIKE :year_month
            """)
            
            result = connection.execute(
                query,
                {"state": state_abbr, "year_month": f"{year_month}%"}
            ).fetchone()
        
        total = result[0] if result and result[0] else 0
        
        return json.dumps({
            "state": state_abbr,
            "period": year_month,
            "total_cases": total
        })
    
    except Exception as e:
        return json.dumps({"error": str(e)})


print("✓ Database query functions defined\n")


# Step 2: Test the database functions
print("Testing database functions:")
result = get_hospitalized_increase_for_state_on_date("AK", "2021-03-05")
print(f"  get_hospitalized_increase_for_state_on_date('AK', '2021-03-05')")
print(f"  Result: {result}\n")


# Step 3: Define tools for database functions
tools_sql = [
    {
        "type": "function",
        "function": {
            "name": "get_hospitalized_increase_for_state_on_date",
            "description": "Retrieves the daily increase in hospitalizations "
                          "for a specific state on a specific date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": "The state abbreviation (e.g., 'NY', 'CA', 'AK')"
                    },
                    "specific_date": {
                        "type": "string",
                        "description": "The specific date in 'YYYY-MM-DD' format"
                    }
                },
                "required": ["state_abbr", "specific_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_cases_for_state_in_month",
            "description": "Retrieves total COVID cases for a specific state "
                          "in a specific month.",
            "parameters": {
                "type": "object",
                "properties": {
                    "state_abbr": {
                        "type": "string",
                        "description": "The state abbreviation (e.g., 'NY', 'CA')"
                    },
                    "year_month": {
                        "type": "string",
                        "description": "The month in 'YYYY-MM' format"
                    }
                },
                "required": ["state_abbr", "year_month"]
            }
        }
    }
]

print("Tool definitions created:")
print("  1. get_hospitalized_increase_for_state_on_date")
print("  2. get_total_cases_for_state_in_month\n")


# Step 4: Ask a database question
messages_sql = [
    {
        "role": "user",
        "content": "How many people were hospitalized in Alaska on 2021-03-05?"
    }
]

print("User question:")
print(f"  '{messages_sql[0]['content']}'\n")


# Step 5: First API call for database
print("="*70)
print("FIRST API CALL: Database question")
print("="*70)

response_sql = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages_sql,
    tools=tools_sql,
    tool_choice="auto"
)

response_message_sql = response_sql.choices[0].message
tool_calls_sql = response_message_sql.tool_calls

print(f"\nAI suggests {len(tool_calls_sql) if tool_calls_sql else 0} function call(s)")

if tool_calls_sql:
    for tool_call in tool_calls_sql:
        print(f"\n  Function: {tool_call.function.name}")
        print(f"  Arguments: {tool_call.function.arguments}")


# Step 6: Execute database function calls
print("\n" + "="*70)
print("EXECUTE DATABASE FUNCTIONS")
print("="*70)

available_functions_sql = {
    "get_hospitalized_increase_for_state_on_date": 
        get_hospitalized_increase_for_state_on_date,
    "get_total_cases_for_state_in_month": 
        get_total_cases_for_state_in_month,
}

messages_sql.append(response_message_sql)

print("\nExecuting functions...\n")

for tool_call in tool_calls_sql:
    function_name = tool_call.function.name
    function_to_call = available_functions_sql[function_name]
    
    function_args = json.loads(tool_call.function.arguments)
    print(f"Calling: {function_name}")
    print(f"  Arguments: {function_args}")
    
    function_response = function_to_call(**function_args)
    print(f"  Result: {function_response}\n")
    
    messages_sql.append({
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": function_response
    })


# Step 7: Second API call for final answer
print("="*70)
print("SECOND API CALL: Get final answer")
print("="*70)

second_response_sql = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages_sql
)

final_answer_sql = second_response_sql.choices[0].message.content

print("\nFinal Answer:")
print(f"  {final_answer_sql}\n")


# ============================================================================
# ADVANCED: BUILDING A REUSABLE FUNCTION LOOP
# ============================================================================
"""
Create a reusable function that handles the entire loop.

This is the pattern you'd use for production systems.
"""

print("="*70)
print("BONUS: REUSABLE FUNCTION CALLING LOOP")
print("="*70)

def call_function_with_tools(user_question, tools, available_functions):
    """
    Generic function calling loop.
    
    Args:
        user_question (str): The user's question
        tools (list): List of tool definitions
        available_functions (dict): Map of function names to Python functions
    
    Returns:
        str: Final answer from AI
    """
    
    # Initialize messages
    messages = [{"role": "user", "content": user_question}]
    
    print(f"\nQuestion: {user_question}")
    print("-" * 70)
    
    # Loop until AI doesn't call functions
    while True:
        # Call API
        response = client.chat.completions.create(
            model="gpt-4-1106",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Check if AI called functions
        if not response_message.tool_calls:
            # No more functions - return final answer
            return response_message.content
        
        # Add AI's suggestion to history
        messages.append(response_message)
        
        # Execute each function
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            
            # Parse arguments and execute
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            
            # Add result to messages
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })


# Test the reusable function
print("\nUsing the reusable function:\n")

answer = call_function_with_tools(
    "What's the weather in San Francisco and New York?",
    tools,
    available_functions
)

print(f"\nAnswer: {answer}\n")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
"""
WHAT YOU LEARNED:

1. FUNCTION CALLING LOOP
   - Define Python functions
   - Describe them as JSON schemas
   - AI suggests function calls
   - You execute them
   - You feed results back
   - AI provides final answer

2. THE TWO API CALLS
   - First: Get function suggestions
   - Second: Get final answer with results

3. MESSAGE ROLES
   - user: Questions from user
   - assistant: AI responses/suggestions
   - tool: Function results

4. FULL CONTROL
   - You decide when to execute
   - You handle errors
   - You format results
   - You decide what tools to offer

5. THIS IS HOW LANGCHAIN AGENTS WORK
   - LangChain automates this loop
   - Function calling is the foundation
   - Understanding this makes you powerful

PRODUCTION PATTERNS:

1. Define tools as JSON
2. Create reusable loop
3. Add error handling
4. Log function calls
5. Monitor API usage
6. Deploy as service

NEXT STEPS:

1. Try different tools
2. Build domain-specific functions
3. Add error handling
4. Create a function library
5. Deploy as API
6. Combine with LangChain (now you understand how it works!)
"""

print("\n" + "="*70)
print("✅ LESSON 4 COMPLETE!")
print("="*70)
print("""
You now understand:
✓ Function calling mechanism
✓ The tool loop pattern
✓ Message roles and history
✓ AI decision making
✓ How LangChain agents work (this is the foundation!)
✓ Building flexible AI systems

Next: Combine this knowledge with LangChain for even more power!
""")
