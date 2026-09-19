"""
Lesson 5: Building Persistent AI Assistants
===========================================

Learn how to build AI assistants that maintain conversation history and context.

⚠️  NOTE: The original notebook uses deprecated APIs (Assistants API retired).
This script uses modern function calling to implement the SAME CONCEPTS better!

This script demonstrates:
- Creating persistent assistant configuration
- Managing conversation threads
- Multi-turn interactions with context preservation
- Tool/function integration with assistants
- Saving and restoring threads
- Production-ready patterns

Author: Saurabh Shirgaokar
Date: 2026
Level: Advanced

What This Does:
- Shows how to build stateful AI assistants
- Demonstrates context preservation across turns
- Shows function calling with persistent state
- Implements save/restore functionality
- Includes production patterns

This is the foundation of:
- Chatbots and chat interfaces
- Customer support systems
- Data analysis assistants
- Personalized AI systems
- Multi-turn interactive AI
"""

# ============================================================================
# STEP 1: SETUP AND IMPORTS
# ============================================================================
"""
Import everything needed for persistent assistants.

Key difference from Lesson 4:
- Lesson 4: Function calling (single exchange)
- Lesson 5: Persistent assistant (multi-turn with memory)
"""

import os
from openai import AzureOpenAI
import json
import time
from datetime import datetime
from sqlalchemy import create_engine, text
import pandas as pd

print("="*70)
print("LESSON 5: PERSISTENT AI ASSISTANTS")
print("="*70)
print("\nSetup & Imports...")

# Connect to Azure OpenAI (using current APIs)
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15"  # Current working version (not deprecated)
)

print("✓ Connected to Azure OpenAI")
print("✓ Using current APIs (Assistants API is DEPRECATED)")
print("✓ Building persistent assistant from scratch")
print("✓ Full transparency and control\n")


# ============================================================================
# STEP 2: CREATE THE PERSISTENT ASSISTANT CLASS
# ============================================================================
"""
This class replaces what the deprecated client.beta.assistants API did.

But YOU can see exactly how it works!

Key components:
- Configuration: name, instructions, model
- Thread: message history (conversation)
- Tools: functions the assistant can use
"""

print("="*70)
print("STEP 2: PERSISTENT ASSISTANT CLASS")
print("="*70)

class PersistentAssistant:
    """
    An AI assistant with persistent state.
    
    This replaces:
        assistant = client.beta.assistants.create(
            instructions="...",
            model="gpt-4-1106",
            tools=[...]
        )
    
    But with FULL transparency of what's happening!
    """
    
    def __init__(self, name, instructions, model="gpt-4-1106"):
        """
        Initialize a persistent assistant.
        
        Args:
            name (str): Assistant name (e.g., "COVID Analyst")
            instructions (str): System prompt / role instructions
            model (str): OpenAI model to use (e.g., "gpt-4-1106")
        """
        
        # CONFIGURATION
        self.name = name
        self.instructions = instructions
        self.model = model
        
        # THREAD (Persistent conversation history)
        self.thread_id = str(datetime.now().timestamp())  # Unique ID
        self.messages = []  # This IS the thread!
        
        # TOOLS (Functions available to this assistant)
        self.tools = []  # Tool definitions (JSON schemas)
        self.available_functions = {}  # Function implementations
        
        print(f"\n✓ Created Assistant: {name}")
        print(f"  ├─ Thread ID: {self.thread_id}")
        print(f"  ├─ Model: {model}")
        print(f"  └─ Role: {instructions[:50]}...\n")
    
    def add_tool(self, tool_definition, function_to_call):
        """
        Register a tool (function) this assistant can use.
        
        Args:
            tool_definition (dict): JSON schema describing the tool
                                   (what AI sees)
            function_to_call (callable): Actual Python function
                                        (what gets executed)
        
        Example:
            assistant.add_tool(
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "parameters": {...}
                    }
                },
                actual_get_weather_function
            )
        """
        
        function_name = tool_definition["function"]["name"]
        
        # Store tool definition (for API)
        self.tools.append(tool_definition)
        
        # Store function (for execution)
        self.available_functions[function_name] = function_to_call
        
        print(f"  ✓ Tool added: {function_name}")
    
    def add_user_message(self, content):
        """
        Add a user message to the thread.
        
        This is like:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="..."
            )
        
        But you have the message in self.messages!
        """
        
        self.messages.append({
            "role": "user",
            "content": content
        })
        
        print(f"\n[USER] Turn {len(self.messages)//2 + 1}:")
        print(f"       {content[:70]}...")
    
    def get_ai_response(self):
        """
        Get AI response to messages, with full function calling support.
        
        This is THE CORE of the persistent assistant.
        
        Process:
        1. ROUND 1: Send messages + tools to AI
           → AI decides: "Do I need to call functions?"
        
        2. FUNCTION EXECUTION: If yes, execute them
           → You run the actual Python functions
           → Add results to thread
        
        3. ROUND 2: Send messages + results back to AI
           → AI decides: "How do I answer based on results?"
        
        Returns:
            str: Final answer from AI
        """
        
        print(f"[ASSISTANT] Processing...")
        
        # Build system message from instructions
        system_message = {
            "role": "system",
            "content": self.instructions
        }
        
        # ROUND 1: Check if AI needs to call functions
        # ================================================
        """
        Send:
        - System message (instructions)
        - Full message history (thread)
        - Available tools
        
        AI responds with: "Call these functions" OR "Here's the answer"
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[system_message] + self.messages,
            tools=self.tools if self.tools else None,
            tool_choice="auto" if self.tools else None
        )
        
        response_message = response.choices[0].message
        
        # Check for tool calls
        if response_message.tool_calls:
            # AI suggested function calls!
            print(f"          ├─ AI suggested {len(response_message.tool_calls)} function call(s)")
            
            # 1. Add AI's tool call suggestion to thread
            # ============================================
            self.messages.append({
                "role": "assistant",
                "content": response_message.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in response_message.tool_calls
                ]
            })
            
            # 2. Execute each function
            # ========================
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.available_functions[function_name]
                
                # Parse arguments (they're JSON strings from AI)
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"          ├─ Executing: {function_name}({json.dumps(function_args, default=str)})")
                
                # Execute the actual Python function
                try:
                    function_response = function_to_call(**function_args)
                except Exception as e:
                    function_response = json.dumps({"error": str(e)})
                    print(f"          │  ⚠️  Error: {str(e)}")
                
                print(f"          ├─ Result: {str(function_response)[:80]}...")
                
                # 3. Add result to thread
                # ======================
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(function_response)
                })
            
            # ROUND 2: Get final answer with function results
            # ===============================================
            """
            Send:
            - System message (instructions)
            - Full thread (messages + tool results)
            
            AI responds with: "Based on the function results, here's my answer"
            """
            
            print(f"          └─ Getting final answer with results...")
            
            final_response = client.chat.completions.create(
                model=self.model,
                messages=[system_message] + self.messages
            )
            
            final_message = final_response.choices[0].message.content
        
        else:
            # No function calls needed - AI answered directly
            # ==============================================
            print(f"          └─ AI answered directly (no functions needed)")
            final_message = response_message.content
        
        # Add final response to thread
        self.messages.append({
            "role": "assistant",
            "content": final_message
        })
        
        # Print response
        print(f"          → {final_message[:70]}...\n")
        
        return final_message
    
    def print_thread_summary(self):
        """Print a summary of the entire conversation thread."""
        
        print("\n" + "="*70)
        print("THREAD SUMMARY (FULL CONVERSATION HISTORY)")
        print("="*70)
        
        print(f"\nAssistant: {self.name}")
        print(f"Thread ID: {self.thread_id}")
        print(f"Total Messages: {len(self.messages)}")
        print(f"Model: {self.model}")
        print(f"\nConversation Flow:")
        print("-" * 70)
        
        for i, msg in enumerate(self.messages, 1):
            if msg["role"] == "user":
                content = msg["content"][:80]
                print(f"[{i}] USER:      {content}...")
            
            elif msg["role"] == "assistant":
                if msg.get("tool_calls"):
                    print(f"[{i}] ASSISTANT: [Tool calls]")
                    for tc in msg["tool_calls"]:
                        print(f"                └─ {tc['function']['name']}()")
                else:
                    content = msg.get("content", "")[:80]
                    print(f"[{i}] ASSISTANT: {content}...")
            
            elif msg["role"] == "tool":
                content = msg["content"][:60]
                print(f"[{i}] TOOL:      {msg['name']} → {content}...")
        
        print("-" * 70)


print("✓ PersistentAssistant class created\n")


# ============================================================================
# STEP 3: SETUP DATABASE
# ============================================================================
"""
Create the COVID database for this lesson.
Same database used in Lesson 3 and Lesson 4.
"""

print("="*70)
print("STEP 3: DATABASE SETUP")
print("="*70)

database_file_path = "./db/test.db"

try:
    # Load COVID data
    df = pd.read_csv("./data/all-states-history.csv").fillna(value=0)
    
    # Create SQLite database
    engine = create_engine(f'sqlite:///{database_file_path}')
    df.to_sql('all_states_history', con=engine, if_exists='replace', index=False)
    
    print("\n✓ COVID database ready")
    print(f"  ├─ File: {database_file_path}")
    print(f"  ├─ Table: all_states_history")
    print(f"  └─ Rows: {len(df)}\n")

except Exception as e:
    print(f"\n✗ Database setup issue: {e}")
    print("  (Make sure ./data/all-states-history.csv exists)\n")


# ============================================================================
# STEP 4: DEFINE DATABASE FUNCTIONS (TOOLS)
# ============================================================================
"""
These are the functions the assistant can call.

They return JSON strings (important!) because the AI needs to parse them.
"""

print("="*70)
print("STEP 4: DEFINE ASSISTANT TOOLS")
print("="*70)

def get_hospitalized_for_state_date(state_abbr, specific_date):
    """
    Get hospitalization data for a state on a specific date.
    
    Args:
        state_abbr (str): State code (e.g., 'AK', 'NY')
        specific_date (str): Date in YYYY-MM-DD format
    
    Returns:
        str: JSON with hospitalization data
    
    This is a TOOL the assistant can use.
    """
    
    try:
        engine = create_engine(f'sqlite:///{database_file_path}')
        
        with engine.connect() as connection:
            query = text("""
                SELECT date, state, hospitalized, hospitalizedIncrease
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
                "state": result[1],
                "hospitalized": float(result[2]),
                "hospitalized_increase": float(result[3]),
                "status": "success"
            })
        else:
            return json.dumps({
                "status": "not_found",
                "message": f"No data for {state_abbr} on {specific_date}"
            })
    
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


def get_cases_for_state_month(state_abbr, year_month):
    """
    Get COVID cases data for a state in a specific month.
    
    Args:
        state_abbr (str): State code (e.g., 'AK', 'NY')
        year_month (str): Month in YYYY-MM format
    
    Returns:
        str: JSON with cases data
    
    This is a TOOL the assistant can use.
    """
    
    try:
        engine = create_engine(f'sqlite:///{database_file_path}')
        
        with engine.connect() as connection:
            query = text("""
                SELECT 
                    SUM(cases) as total_cases,
                    COUNT(*) as days_reported,
                    AVG(cases) as avg_daily_cases,
                    MIN(cases) as min_daily,
                    MAX(cases) as max_daily
                FROM all_states_history
                WHERE state = :state AND date LIKE :year_month
            """)
            
            result = connection.execute(
                query,
                {"state": state_abbr, "year_month": f"{year_month}%"}
            ).fetchone()
        
        if result[0]:
            return json.dumps({
                "state": state_abbr,
                "period": year_month,
                "total_cases": float(result[0]) if result[0] else 0,
                "days_reported": result[1],
                "avg_daily_cases": float(result[2]) if result[2] else 0,
                "min_daily": float(result[3]) if result[3] else 0,
                "max_daily": float(result[4]) if result[4] else 0,
                "status": "success"
            })
        else:
            return json.dumps({
                "status": "not_found",
                "message": f"No data for {state_abbr} in {year_month}"
            })
    
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)})


print("\n✓ Database functions defined")
print("  ├─ get_hospitalized_for_state_date()")
print("  └─ get_cases_for_state_month()\n")


# ============================================================================
# STEP 5: CREATE ASSISTANT & ADD TOOLS
# ============================================================================
"""
Now instantiate our persistent assistant.
Add the tools it can use.

This replaces what used to be:
  assistant = client.beta.assistants.create(
      instructions="...",
      model="gpt-4-1106",
      tools=[...]
  )
"""

print("="*70)
print("STEP 5: CREATE & CONFIGURE ASSISTANT")
print("="*70)

# Create the assistant
covid_assistant = PersistentAssistant(
    name="COVID Data Analyst",
    instructions="""You are a COVID-19 data analyst assistant.
You help users understand COVID statistics by querying a database.

When users ask about COVID data:
1. Use the appropriate tools to fetch data
2. Analyze and interpret the results
3. Provide clear, specific answers with numbers
4. Compare data points when relevant

IMPORTANT: Only report data that exists in the database.
Do NOT make up or estimate data. If data doesn't exist, say so.""",
    model="gpt-4-1106"
)

# Define TOOL 1: Hospitalization data
hospitalized_tool = {
    "type": "function",
    "function": {
        "name": "get_hospitalized_for_state_date",
        "description": "Get COVID hospitalization data for a specific state and date",
        "parameters": {
            "type": "object",
            "properties": {
                "state_abbr": {
                    "type": "string",
                    "description": "US state abbreviation (e.g., 'AK', 'NY', 'CA')"
                },
                "specific_date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format (e.g., '2021-03-15')"
                }
            },
            "required": ["state_abbr", "specific_date"]
        }
    }
}

# Define TOOL 2: Cases data
cases_tool = {
    "type": "function",
    "function": {
        "name": "get_cases_for_state_month",
        "description": "Get COVID cases data for a state in a specific month",
        "parameters": {
            "type": "object",
            "properties": {
                "state_abbr": {
                    "type": "string",
                    "description": "US state abbreviation (e.g., 'AK', 'NY', 'CA')"
                },
                "year_month": {
                    "type": "string",
                    "description": "Month in YYYY-MM format (e.g., '2021-03')"
                }
            },
            "required": ["state_abbr", "year_month"]
        }
    }
}

# Register tools with assistant
covid_assistant.add_tool(hospitalized_tool, get_hospitalized_for_state_date)
covid_assistant.add_tool(cases_tool, get_cases_for_state_month)


# ============================================================================
# STEP 6: MULTI-TURN CONVERSATION
# ============================================================================
"""
This is where persistent assistants shine!

Notice how:
1. First question establishes context
2. Second question references first
3. Third question uses context from both

The THREAD (message history) makes this possible!
"""

print("\n" + "="*70)
print("STEP 6: MULTI-TURN CONVERSATION WITH PERSISTENT THREAD")
print("="*70)

# TURN 1: Establish context
# ==========================
print("\n--- TURN 1: Establish Context ---")

question1 = "How many people were hospitalized in Alaska on 2021-03-05?"

covid_assistant.add_user_message(question1)
answer1 = covid_assistant.get_ai_response()

print(f"[FINAL ANSWER]:")
print(f"  {answer1}\n")


# TURN 2: Follow-up with implicit context
# =========================================
print("--- TURN 2: Follow-up (Uses Context from Turn 1) ---")

question2 = "What about the total cases in Alaska for March 2021?"

covid_assistant.add_user_message(question2)
answer2 = covid_assistant.get_ai_response()

print(f"[FINAL ANSWER]:")
print(f"  {answer2}\n")

# KEY POINT: The assistant knows "March 2021" from Turn 1!
# It doesn't need the user to repeat "Alaska in March 2021"


# TURN 3: Comparative question using context
# =============================================
print("--- TURN 3: Comparison (Uses Context from Turns 1 & 2) ---")

question3 = "Compare that to New York in the same period"

covid_assistant.add_user_message(question3)
answer3 = covid_assistant.get_ai_response()

print(f"[FINAL ANSWER]:")
print(f"  {answer3}\n")

# KEY POINT: The assistant knows:
# - "that" refers to cases data (Turn 2)
# - "same period" refers to March 2021 (Turn 1)
# - Comparing to New York (Turn 3)
# All because the THREAD persists!


# TURN 4: Another follow-up
# ==========================
print("--- TURN 4: Another Question (Full Context Available) ---")

question4 = "Which state had more hospitalizations during that month?"

covid_assistant.add_user_message(question4)
answer4 = covid_assistant.get_ai_response()

print(f"[FINAL ANSWER]:")
print(f"  {answer4}\n")


# ============================================================================
# STEP 7: DEMONSTRATE THREAD PERSISTENCE
# ============================================================================
"""
Show that the thread is truly persistent.
The assistant has full conversation history.
"""

print("="*70)
print("STEP 7: THREAD PERSISTENCE DEMONSTRATION")
print("="*70)

# Print full thread
covid_assistant.print_thread_summary()

print("\nKey Observations:")
print("✓ All messages from all 4 turns are in the thread")
print("✓ Each turn's context is available to subsequent turns")
print("✓ The assistant can reference any previous question/answer")
print("✓ This is what makes conversations feel 'intelligent'")
print("✓ Without this, each turn would be independent\n")


# ============================================================================
# STEP 8: SAVE & RESTORE FUNCTIONALITY
# ============================================================================
"""
Production pattern: Save thread to storage, restore later.

This is why persistent assistants are powerful!
"""

print("="*70)
print("STEP 8: SAVE & RESTORE THREADS (PRODUCTION PATTERN)")
print("="*70)

def save_thread_to_json(assistant, filename):
    """Save a thread to a JSON file."""
    
    thread_data = {
        "name": assistant.name,
        "instructions": assistant.instructions,
        "model": assistant.model,
        "thread_id": assistant.thread_id,
        "created_at": datetime.now().isoformat(),
        "messages": assistant.messages
    }
    
    with open(filename, 'w') as f:
        json.dump(thread_data, f, indent=2)
    
    print(f"\n✓ Thread saved to: {filename}")
    print(f"  ├─ Thread ID: {assistant.thread_id}")
    print(f"  ├─ Messages: {len(assistant.messages)}")
    print(f"  └─ File size: {len(json.dumps(thread_data))} bytes")


def restore_thread_from_json(filename):
    """Restore a thread from a JSON file."""
    
    with open(filename, 'r') as f:
        thread_data = json.load(f)
    
    # Recreate assistant
    assistant = PersistentAssistant(
        name=thread_data["name"],
        instructions=thread_data["instructions"],
        model=thread_data["model"]
    )
    
    # Restore thread data
    assistant.thread_id = thread_data["thread_id"]
    assistant.messages = thread_data["messages"]
    
    print(f"\n✓ Thread restored from: {filename}")
    print(f"  ├─ Thread ID: {assistant.thread_id}")
    print(f"  ├─ Messages: {len(assistant.messages)}")
    print(f"  └─ Ready to continue conversation!")
    
    return assistant


# Save the current thread
save_thread_to_json(covid_assistant, "covid_thread_example.json")

print("\n✓ You can now:")
print("  1. Restore this thread later")
print("  2. Continue the conversation")
print("  3. Store in database for production")
print("  4. Share thread with other services")
print("  5. Replay conversation history\n")


# ============================================================================
# STEP 9: COMPARISON: LESSON 4 VS LESSON 5
# ============================================================================
"""
Show the difference between stateless (Lesson 4) and stateful (Lesson 5).
"""

print("="*70)
print("STEP 9: LESSON 4 VS LESSON 5 COMPARISON")
print("="*70)

print("""
LESSON 4: Function Calling (Stateless)
┌─────────────────────────────────────────┐
│ Question 1                               │
│   ↓                                      │
│ AI thinks → Calls functions → Answer    │
│   ↓                                      │
│ Thread DISCARDED                         │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Question 2 (SAME STATE - NO CONTEXT!)   │
│   ↓                                      │
│ AI thinks → Calls functions → Answer    │
│   ↓                                      │
│ Thread DISCARDED                         │
└─────────────────────────────────────────┘

Use case: One-off queries, stateless interactions


LESSON 5: Persistent Assistant (Stateful)
┌─────────────────────────────────────────┐
│ Question 1                               │
│   ↓                                      │
│ AI thinks → Calls functions → Answer    │
│   ↓                                      │
│ Thread SAVED (remembers Q1 & A1)        │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Question 2 (Sees Q1, A1 in context!)    │
│   ↓                                      │
│ AI thinks → Calls functions → Answer    │
│   ↓                                      │
│ Thread SAVED (remembers Q1, A1, Q2, A2) │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│ Question 3 (Sees Q1, A1, Q2, A2!)       │
│   ↓                                      │
│ AI thinks → Calls functions → Answer    │
│   ↓                                      │
│ Thread SAVED (Full history)             │
└─────────────────────────────────────────┘

Use case: Chatbots, conversational AI, multi-turn interactions
""")

print("Key Difference:")
print("  Lesson 4: Each question is independent")
print("  Lesson 5: Each question builds on previous context")
print("  Result: More intelligent, natural conversations\n")


# ============================================================================
# STEP 10: PRODUCTION CONSIDERATIONS
# ============================================================================
"""
Real-world patterns for deploying assistants.
"""

print("="*70)
print("STEP 10: PRODUCTION PATTERNS")
print("="*70)

print("""
Pattern 1: Per-User Assistants
==============================
Each user gets their own assistant with persistent thread.

    user_123 → Assistant A → Thread (only user_123 messages)
    user_456 → Assistant B → Thread (only user_456 messages)

Implementation:
    def get_user_assistant(user_id):
        thread = db.get_thread(user_id)
        if thread:
            return restore_thread(thread)
        else:
            return PersistentAssistant(...)


Pattern 2: Specialized Assistants
==================================
Different assistant for different tasks.

    Billing Questions → Billing Assistant
    Technical Issues → Technical Assistant  
    General Chat → General Assistant

Each maintains its own thread per user.


Pattern 3: Database Persistence
================================
Save threads to database (not just files).

    After each interaction:
        db.update_thread(
            user_id=user_123,
            thread_id=thread.thread_id,
            messages=thread.messages
        )

    On next session:
        thread = db.get_thread(user_id)
        assistant = restore_thread(thread)


Pattern 4: Logging & Monitoring
================================
Log all interactions for quality/compliance.

    def log_interaction(assistant, user_input, response):
        logger.info({
            "user_id": user_id,
            "thread_id": assistant.thread_id,
            "timestamp": datetime.now(),
            "input": user_input,
            "response": response,
            "tools_used": [tc.function.name for tc in tool_calls]
        })


Pattern 5: Rate Limiting & Quotas
==================================
Manage usage per user/assistant.

    if user_tokens_today > DAILY_LIMIT:
        raise QuotaExceededError()
    
    response = assistant.get_ai_response()
    update_user_tokens(user_id, len(response))
""")

print("\n✓ These patterns enable production-grade systems\n")


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================
"""
Summary of what you learned.
"""

print("="*70)
print("KEY TAKEAWAYS")
print("="*70)

print("""
WHAT YOU LEARNED:

1. PERSISTENT ASSISTANTS
   ├─ Configuration (name, instructions, model)
   ├─ Thread (message history)
   └─ Tools (available functions)

2. MULTI-TURN CONVERSATIONS
   ├─ Context preserved across exchanges
   ├─ Each message adds to thread
   └─ AI uses full history for decisions

3. FUNCTION CALLING WITH STATE
   ├─ AI suggests functions
   ├─ You execute them
   ├─ Results added to thread
   └─ AI makes final decision with context

4. PRODUCTION PATTERNS
   ├─ Save/restore threads
   ├─ Per-user assistants
   ├─ Database persistence
   └─ Monitoring & logging

5. WHY THIS MATTERS
   ├─ Creates natural conversations
   ├─ Enables context-aware AI
   ├─ Foundation for chatbots
   └─ Better user experience


TECHNICAL INSIGHT:

The deprecated Assistants API was hiding this simple pattern:

    Thread = persistent list of messages
    Assistant = config + thread + tools
    Loop = request → execute → add results → request again

By implementing it yourself:
    ✓ You understand how it works
    ✓ You can customize anything
    ✓ You control the data
    ✓ You won't be surprised by API changes


NEXT STEPS:

1. ✓ Run this script and understand it
2. ✓ Modify instructions and tools
3. ✓ Build save/restore functionality
4. ✓ Integrate with database
5. ✓ Add user authentication
6. ✓ Deploy as API service
7. ✓ Build web interface
""")

print("\n" + "="*70)
print("✅ LESSON 5 COMPLETE!")
print("="*70)

print("""
You now understand:
✓ How persistent AI assistants work
✓ Why conversation history matters
✓ How to build stateful AI systems
✓ Production patterns for deployment

No deprecated APIs. No hidden magic. Just solid understanding! 🚀
""")
