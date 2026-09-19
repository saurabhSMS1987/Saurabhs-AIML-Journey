# Lesson 4: Azure OpenAI Function Calling Feature - Complete Code Guide 🔧

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Level:** Advanced  
**Topic:** Building AI Systems with OpenAI Function Calling

---

## Table of Contents

1. [Overview](#overview)
2. [The Progression](#the-progression)
3. [Key Concepts](#key-concepts)
4. [Code Breakdown](#code-breakdown)
5. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
6. [Function Calling Flow](#function-calling-flow)
7. [Practical Examples](#practical-examples)
8. [Advanced Techniques](#advanced-techniques)
9. [Common Patterns](#common-patterns)

---

## Overview

### What This Lesson Teaches

This lesson reveals **the foundation of AI agents** by teaching:
- ✅ What function calling really is
- ✅ Defining functions as JSON schemas
- ✅ Letting AI decide when to call functions
- ✅ Handling AI-generated function calls
- ✅ Building flexible AI systems
- ✅ Creating custom integrations
- ✅ The "tool loop" pattern

### Why Function Calling?

**Previous approach (Lesson 3 with LangChain):**
- LangChain agents handle everything
- Great for quick solutions
- Less control
- Abstraction hides details

**Function Calling approach (Lesson 4 - Native OpenAI):**
- You control everything
- Lower level, more flexible
- See exactly what happens
- Build custom systems
- Understand AI reasoning

### The Real Innovation

Function calling is what makes modern AI "agents":

```
Before Function Calling:
Question → AI → Text response
(Simple, no tool access)

With Function Calling:
Question → AI → "Call this function" → Run function → Feed result back → 
AI → Uses result → Final answer
(Complex, flexible, powerful)
```

---

## The Progression

### Lessons 1-4 Journey

```
Lesson 1: Simple Text
         Question → AI → Answer
         (No tools, direct response)
                    ↓
Lesson 2: CSV Analysis  
         Question → Pandas agent → Answer
         (One tool: Pandas)
                    ↓
Lesson 3: SQL Queries
         Question → SQL agent → Answer
         (One tool: SQL database, auto-managed by LangChain)
                    ↓
Lesson 4: Function Calling ← YOU ARE HERE
         Question → AI → Chooses functions → You execute → AI → Answer
         (Any tools, you have control, understand the mechanism)
```

### Conceptual Shift

**Lesson 3 (SQL Agent):**
```
LangChain does all the work:
- AI writes SQL
- LangChain executes it
- LangChain handles the loop
- You just ask questions
```

**Lesson 4 (Function Calling):**
```
You control the loop:
- AI suggests function calls
- You decide when to execute
- You handle the execution
- You feed results back to AI
- Full transparency and control
```

---

## Key Concepts

### 1. **Functions as Tools (JSON Schema)**

Unlike Python functions, OpenAI needs functions defined as **JSON schemas**:

**Python function:**
```python
def get_weather(location, unit="fahrenheit"):
    """Get weather for a location"""
    # implementation
    return result
```

**OpenAI function definition (JSON):**
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City and state, e.g. New York, NY"
        },
        "unit": {
          "type": "string",
          "enum": ["fahrenheit", "celsius"],
          "description": "Temperature unit"
        }
      },
      "required": ["location"]
    }
  }
}
```

**Why JSON?**
- Language-independent
- Describes what, not how
- AI understands structure
- Works with any backend

### 2. **The Tool Loop (Core Pattern)**

This is the **foundation of AI agents**:

```
┌─ User asks question
│
├─ Send to AI with available tools
│
├─ AI analyzes: "Do I need to call a function?"
│
├─ If NO: AI returns direct answer → Done
│
├─ If YES: AI returns function call suggestion
│           {
│             "function_name": "...",
│             "arguments": {...}
│           }
│
├─ Your code: Parse the suggestion
│
├─ Your code: Call the actual function
│
├─ Your code: Get the result
│
├─ Your code: Add result to message history
│
├─ Send message history back to AI
│
├─ AI analyzes the new information
│
├─ AI returns final answer → Done
│
└─ Or loop again if more functions needed
```

### 3. **Message Roles in Function Calling**

The message history has different roles:

**user:** Questions from user
```json
{"role": "user", "content": "What's the weather in NYC?"}
```

**assistant:** AI responses
```json
{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_123",
      "function": {
        "name": "get_weather",
        "arguments": "{\"location\": \"NYC\"}"
      }
    }
  ]
}
```

**tool:** Function results
```json
{
  "role": "tool",
  "tool_call_id": "call_123",
  "name": "get_weather",
  "content": "{\"temperature\": 50, \"condition\": \"clear\"}"
}
```

This creates a **conversation history** that the AI can follow!

### 4. **Function Arguments are Strings**

Important: AI returns arguments as **JSON strings**, not objects:

```python
# AI returns this:
"arguments": "{\"location\": \"NYC\"}"  # JSON string

# You must parse it:
args = json.loads(tool_call.function.arguments)
# Now: args = {"location": "NYC"}
```

### 5. **Tool Choice Parameter**

Control when AI calls functions:

```python
# "auto" - AI decides (most common)
tool_choice="auto"

# "required" - Must call a function
tool_choice="required"

# Specific function
tool_choice={"type": "function", "function": {"name": "specific_function"}}

# "none" - Never call functions
tool_choice="none"
```

### 6. **The Two-Round Trip**

Function calling requires **two API calls**:

**First call:**
```
User question + Tools definition → AI → Function call suggestion
```

**Second call:**
```
User question + Tools + Function results → AI → Final answer
```

This is why you see TWO `client.chat.completions.create()` calls!

---

## Code Breakdown

### **Step 1: Setup and Imports**

```python
import os
from openai import AzureOpenAI
import json

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15"
)
```

**What's different from LangChain:**
- Direct OpenAI client (not LangChain wrapper)
- Lower level = more control
- Smaller abstraction layer
- See raw API responses

---

### **Step 2: Define Python Functions**

```python
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location. 
    The default unit when not specified is fahrenheit"""
    if "new york" in location.lower():
        return json.dumps({
            "location": "New York",
            "temperature": "40",
            "unit": unit
        })
    elif "san francisco" in location.lower():
        return json.dumps({
            "location": "San Francisco",
            "temperature": "50",
            "unit": unit
        })
    else:
        return json.dumps({
            "location": location,
            "temperature": "unknown"
        })
```

**Important notes:**
- Return values as **JSON strings** (not Python dicts)
- AI doesn't call this directly
- AI just suggests calling it
- **You** execute it when AI asks

---

### **Step 3: Define Functions as JSON Schema**

This is the **crucial step**:

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather in given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g. New York, NY"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["fahrenheit", "celsius"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

**What this does:**
- Tells AI about the function
- Describes each parameter
- Lists required vs optional
- Shows allowed values (enum)
- Doesn't include implementation details

---

### **Step 4: Prepare Messages**

```python
messages = [
    {
        "role": "user",
        "content": "What's the weather in San Francisco, New York, and Las Vegas?"
    }
]
```

This is a regular conversation start.

---

### **Step 5: First API Call - Get Function Suggestions**

```python
response = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages,
    tools=tools,
    tool_choice="auto",  # Let AI decide whether to call functions
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls
```

**What happens:**
- AI reads the question
- AI sees available tools
- AI decides: "I need to call get_current_weather 3 times"
- AI returns function call suggestions
- **NOT** the actual results, just suggestions!

**Response structure:**
```python
response_message.tool_calls = [
    {
        "id": "call_123",
        "function": {
            "name": "get_current_weather",
            "arguments": "{\"location\": \"San Francisco, CA\"}"
        }
    },
    # More calls...
]
```

---

### **Step 6: Execute Suggested Functions**

```python
available_functions = {
    "get_current_weather": get_current_weather,
}

messages.append(response_message)  # Add AI's suggestion to history

for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_to_call = available_functions[function_name]
    
    # Parse the arguments (they're JSON strings!)
    function_args = json.loads(tool_call.function.arguments)
    
    # Actually call the function
    function_response = function_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit")
    )
    
    # Add result to message history
    messages.append({
        "tool_call_id": tool_call.id,
        "role": "tool",
        "name": function_name,
        "content": function_response
    })
```

**Key steps:**
1. Map function names to actual Python functions
2. Add AI's suggestion to history (important!)
3. Parse JSON string arguments
4. Execute the function
5. Add results back to history (crucial!)

---

### **Step 7: Second API Call - Get Final Answer**

```python
second_response = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages,  # Includes original question + AI suggestion + results
)

print(second_response.choices[0].message.content)
# Output: "San Francisco is 50°F, New York is 40°F, Las Vegas is 70°F"
```

**What's different:**
- Same messages list (now with function results!)
- No tools parameter needed (already got the tool calls)
- AI now has actual data to work with
- AI provides final answer

---

## Step-by-Step Walkthrough

### Example: "What's the weather in three cities?"

#### Step 1: User Asks
```
"What's the weather in San Francisco, New York, and Las Vegas?"
```

#### Step 2: First API Call
```
Message: User question
Tools: Weather function definition
AI Response: "I should call get_current_weather 3 times"
(Actual function NOT called yet)
```

#### Step 3: Parse AI Suggestions
```
Suggestion 1: Call get_current_weather("San Francisco, CA")
Suggestion 2: Call get_current_weather("New York, NY")
Suggestion 3: Call get_current_weather("Las Vegas, NV")
```

#### Step 4: Execute Functions
```
Call 1: get_current_weather("San Francisco, CA") → "50°F"
Call 2: get_current_weather("New York, NY") → "40°F"
Call 3: get_current_weather("Las Vegas, NV") → "70°F"
```

#### Step 5: Build Message History
```
messages = [
    {"role": "user", "content": "What's the weather..."},
    {"role": "assistant", "tool_calls": [...]},
    {"role": "tool", "content": "50°F"},
    {"role": "tool", "content": "40°F"},
    {"role": "tool", "content": "70°F"}
]
```

#### Step 6: Second API Call
```
Message history: All previous + function results
AI Response: "San Francisco is 50°F, New York is 40°F, Las Vegas is 70°F"
```

#### Step 7: Return to User
```
"San Francisco is 50°F, New York is 40°F, Las Vegas is 70°F"
```

---

## Function Calling Flow

### Complete Loop Diagram

```
STEP 1: Prepare Messages
   - User question
   - Conversation history
                    ↓
STEP 2: Define Tools (JSON schemas)
   - Function names
   - Parameter descriptions
   - Required vs optional
                    ↓
STEP 3: First API Call
   Send: messages + tools
   Get: AI's function call suggestions
                    ↓
STEP 4: Check for Function Calls
   - tool_calls = response_message.tool_calls
   - If tool_calls is None: Done! Use AI response
   - If tool_calls exists: Continue...
                    ↓
STEP 5: Add AI Response to History
   messages.append(response_message)
                    ↓
STEP 6: Execute Each Suggested Function
   For each tool_call:
     - Get function name
     - Parse arguments (JSON string)
     - Call actual Python function
     - Get result
     - Add to messages as tool role
                    ↓
STEP 7: Second API Call
   Send: updated messages (with results)
   Get: AI's final answer using the results
                    ↓
STEP 8: Check Again for More Function Calls
   - If more tool_calls: Loop back to Step 6
   - If no tool_calls: Done!
                    ↓
STEP 9: Return Final Answer
   AI's response using function results
```

---

## Practical Examples

### Example 1: Weather Query (Simple)

**User:** "What's the weather in NYC?"

**Flow:**
```
1st API call: AI → "Call get_weather('NYC')"
Execute: get_weather('NYC') → "40°F"
2nd API call: AI + result → "The weather in NYC is 40°F"
```

### Example 2: Multiple Functions

**User:** "What's the COVID hospitalization for Alaska on 2021-03-05?"

**Functions available:**
- get_hospitalized_increase_for_state_on_date
- get_positive_cases_for_state_on_date

**Flow:**
```
1st API call: AI → "Call get_hospitalized_increase_for_state_on_date('AK', '2021-03-05')"
Execute: Function → {"hospitalizedIncrease": 3}
2nd API call: AI + result → "Alaska had 3 new hospitalizations on March 5, 2021"
```

### Example 3: Chained Functions

**User:** "Which state had more hospitalizations on a specific date?"

**Flow:**
```
1st API call: AI → "I need to call 2 functions to compare"
   Call 1: get_hospitalized_for_state('NY', date)
   Call 2: get_hospitalized_for_state('CA', date)
Execute both functions
2nd API call: AI + both results → "NY had more hospitalizations"
3rd API call (if needed): AI → "More details..." (if AI wants more info)
```

---

## Advanced Techniques

### 1. **Handling Complex JSON Returns**

```python
# Function returns complex JSON
def get_user_data(user_id):
    return json.dumps({
        "id": user_id,
        "name": "John",
        "contact": {
            "email": "john@example.com",
            "phone": "555-1234"
        },
        "history": [...]
    })

# AI understands complex structure
# Can ask follow-up questions about nested fields
```

### 2. **Validating Function Arguments**

```python
def execute_function_call(tool_call):
    function_name = tool_call.function.name
    
    # Validate function exists
    if function_name not in available_functions:
        return {"error": f"Unknown function: {function_name}"}
    
    # Parse and validate arguments
    try:
        args = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON in arguments"}
    
    # Execute with error handling
    try:
        function = available_functions[function_name]
        result = function(**args)
        return result
    except Exception as e:
        return {"error": str(e)}
```

### 3. **Loop for Multiple Function Calls**

```python
# Keep looping until AI stops calling functions
while True:
    response = client.chat.completions.create(
        model="gpt-4-1106",
        messages=messages,
        tools=tools
    )
    
    response_message = response.choices[0].message
    
    # If no tool calls, AI is done
    if not response_message.tool_calls:
        print(response_message.content)  # Final answer
        break
    
    # Process function calls
    messages.append(response_message)
    
    for tool_call in response_message.tool_calls:
        # Execute function
        result = execute_function(tool_call)
        
        # Add result to messages
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": result
        })
```

### 4. **Conditional Function Definitions**

Based on user input, show different functions:

```python
def get_available_tools(query):
    """Return different tools based on query"""
    
    if "weather" in query.lower():
        return [weather_tools]
    elif "covid" in query.lower():
        return [covid_tools]
    else:
        return [weather_tools, covid_tools]  # All tools

# Use it
query = "Tell me about COVID in Alaska"
tools = get_available_tools(query)

response = client.chat.completions.create(
    model="gpt-4-1106",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

---

## Common Patterns

### Pattern 1: Simple Tool Loop

```python
# Keep asking until AI doesn't need tools
messages = [{"role": "user", "content": question}]

while True:
    response = client.chat.completions.create(
        model="gpt-4-1106",
        messages=messages,
        tools=tools
    )
    
    message = response.choices[0].message
    messages.append(message)
    
    if not message.tool_calls:
        return message.content  # Done!
    
    for tool_call in message.tool_calls:
        result = call_function(tool_call)
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": result
        })
```

### Pattern 2: Function Results as Formatted Text

```python
# Instead of returning raw JSON, format nicely
def get_weather(location):
    data = fetch_weather(location)
    
    # Return formatted string (AI can understand natural language too!)
    return f"Current weather in {location}: {data['temp']}°F, {data['condition']}"
```

### Pattern 3: Error Handling

```python
messages = [{"role": "user", "content": question}]

try:
    response = client.chat.completions.create(
        model="gpt-4-1106",
        messages=messages,
        tools=tools
    )
except Exception as e:
    return f"Error calling API: {e}"

# Process response...
```

---

## Comparison: All Approaches

### Text Only (Lesson 1)
```
Question → AI → Answer
Simple, no tools, direct
```

### Pandas Agent (Lesson 2)
```
Question → LangChain → Pandas code → Answer
LangChain handles everything automatically
```

### SQL Agent (Lesson 3)
```
Question → LangChain → SQL query → DB → Answer
LangChain manages the tool loop
```

### Function Calling (Lesson 4)
```
Question → AI → Function suggestion → You execute → Feed back → AI → Answer
You control the entire loop
```

### Key Differences

| Aspect | LangChain Agents | Function Calling |
|--------|-----------------|-----------------|
| Abstraction | High | Low |
| Control | Less | More |
| Flexibility | Moderate | High |
| Learning | Easier | Harder |
| Understanding | Hides details | Shows everything |
| Customization | Limited | Unlimited |
| Production Use | Good | Excellent |

---

## Summary

**Lesson 4 reveals the mechanism behind AI agents:**

You now understand:
1. ✅ How AI "calls" functions
2. ✅ The tool loop pattern
3. ✅ Message roles and history
4. ✅ How to define tools as JSON
5. ✅ How to execute suggestions
6. ✅ How AI uses results
7. ✅ Building flexible systems

**This knowledge is ESSENTIAL for:**
- Understanding LangChain agents (they use this under the hood)
- Building custom AI systems
- Integrating AI with your code
- Advanced applications
- Production deployments

---

## Next Steps

1. **Modify the examples:** Change function parameters, add new functions
2. **Build custom tools:** Create functions for your domain
3. **Test the loop:** Add print statements to see message flow
4. **Handle errors:** Add validation and error handling
5. **Combine with databases:** Use function calls to query databases
6. **Production integration:** Deploy as API endpoints

---

**Now you understand the foundation of modern AI systems! 🚀**
