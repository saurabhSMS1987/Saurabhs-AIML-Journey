"""
Lesson 3: Connecting to a SQL Database
=======================================

Learn how to build an AI agent that analyzes data from SQL databases.

This script demonstrates:
- Loading CSV data and converting to SQL database
- Connecting to SQLite databases
- Creating AI SQL agents
- Writing SQL queries through natural language
- Automatic query verification and error handling
- Building production-ready data analysis systems

Author: Saurabh Shirgaokar
Date: 2026
Level: Advanced

What This Does:
- Loads COVID tracking data (CSV file)
- Creates SQLite database from CSV
- Creates an AI agent that understands SQL
- Asks complex questions in natural language
- AI writes and executes SQL queries
- AI verifies results and explains methodology
- Returns production-ready responses

Real-world Use Cases:
- Enterprise data analysis
- Business intelligence queries
- Large-scale data exploration
- Production data pipelines
- Multi-user database systems
"""

# ============================================================================
# STEP 1: IMPORTS AND SETUP
# ============================================================================
"""
Import all necessary libraries.

Key additions from Lesson 2:
- sqlalchemy: Database connection and ORM
- SQLDatabase: LangChain's database wrapper
- create_sql_agent: Special agent for SQL
- SQLDatabaseToolkit: Tools for SQL operations
"""

import os
from IPython.display import Markdown, HTML, display

# Core LangChain imports (from Lessons 1-2)
from langchain_openai import AzureChatOpenAI

# NEW: SQL-specific imports
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase

# Data processing
from sqlalchemy import create_engine
import pandas as pd

print("✓ All imports successful")


# ============================================================================
# STEP 2: LOAD DATA FROM CSV (SAME AS LESSON 2)
# ============================================================================
"""
Load data from CSV file.
This is identical to Lesson 2 - we start with the same data source.
"""

print("\n" + "="*70)
print("STEP 1: LOAD DATA FROM CSV")
print("="*70)

# Read CSV file and fill missing values
file_url = "./data/all-states-history.csv"
df = pd.read_csv(file_url).fillna(value=0)

print(f"✓ Loaded CSV: {file_url}")
print(f"✓ Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"✓ Columns: {', '.join(df.columns.tolist()[:5])}...")
print(f"\nFirst few rows:")
print(df.head())


# ============================================================================
# STEP 3: CREATE SQL DATABASE FROM CSV (NEW!)
# ============================================================================
"""
Convert the CSV data into a SQL database.

This is the KEY step that makes data analysis scalable!

Why SQL?
- Handles billions of rows efficiently
- Only loads needed data
- Built-in query optimization
- Multi-user access
- Industry standard
"""

print("\n" + "="*70)
print("STEP 2: CREATE SQL DATABASE")
print("="*70)

# Define database file path
database_file_path = "./db/test.db"

# Create SQLAlchemy engine
# This engine is the connection to our database
engine = create_engine(f'sqlite:///{database_file_path}')

print(f"✓ Created SQLAlchemy engine")
print(f"✓ Database will be stored at: {database_file_path}")

# Write DataFrame to SQL database
# This converts our CSV data into SQL format
row_count = df.to_sql(
    'all_states_history',  # Name of the table in database
    con=engine,            # Which database/engine to use
    if_exists='replace',   # Replace table if it exists
    index=False            # Don't save DataFrame index
)

print(f"✓ Wrote {row_count} rows to database")
print(f"✓ Table name: 'all_states_history'")
print(f"✓ Database ready for SQL queries!")

"""
WHAT JUST HAPPENED:

CSV File (all-states-history.csv)
    ↓
Pandas reads CSV into DataFrame
    ↓
SQLAlchemy translates to SQL
    ↓
SQL CREATE TABLE statement executed
    ↓
20,780 rows inserted into database
    ↓
SQLite database created: ./db/test.db
    ↓
Ready for intelligent queries!

Database Structure:
- File: ./db/test.db (SQLite database)
- Table: all_states_history
- Rows: 20,780
- Columns: date, state, hospitalized, hospitalizedCumulative, etc.
"""


# ============================================================================
# STEP 4: CONNECT TO DATABASE WITH LANGCHAIN
# ============================================================================
"""
Set up LangChain's database connection.
This allows the AI to understand and query the database.
"""

print("\n" + "="*70)
print("STEP 3: CONNECT LANGCHAIN TO DATABASE")
print("="*70)

# Create LangChain's SQL database wrapper
# This wraps SQLite and makes it compatible with agents
db = SQLDatabase.from_uri(f'sqlite:///{database_file_path}')

print("✓ Created LangChain SQLDatabase connection")
print(f"✓ Database tables: {db.get_table_names()}")
print(f"✓ Can now query using natural language!")

# Optionally: Explore what tables and columns are available
print(f"\nDatabase schema:")
print(db.get_table_info())


# ============================================================================
# STEP 5: CREATE AZURE OPENAI CONNECTION
# ============================================================================
"""
Connect to GPT-4 model.
This is the "brain" that will write SQL queries.

Note: We set temperature=0 for deterministic (reproducible) results
"""

print("\n" + "="*70)
print("STEP 4: CONNECT TO GPT-4")
print("="*70)

llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0,      # No randomness (same answer every time)
    max_tokens=500      # Keep responses concise
)

print("✓ Connected to Azure OpenAI GPT-4")
print("✓ Temperature: 0 (deterministic)")
print("✓ Max tokens: 500 (concise responses)")


# ============================================================================
# STEP 6: CREATE SQL DATABASE TOOLKIT
# ============================================================================
"""
Combine the database and LLM into a toolkit.
This provides the agent with SQL tools.
"""

print("\n" + "="*70)
print("STEP 5: CREATE SQL TOOLKIT")
print("="*70)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

print("✓ Created SQLDatabaseToolkit")
print("✓ Toolkit provides these tools to the agent:")
print("  - query_sql_db: Execute SQL queries")
print("  - get_schema: See table structure")
print("  - get_table_info: See column information")
print("  - list_tables: See all tables")


# ============================================================================
# STEP 7: DEFINE AGENT INSTRUCTIONS (PREFIX)
# ============================================================================
"""
Create detailed instructions for how the SQL agent should behave.

This PREFIX sets up:
- What the agent is designed for
- How to write SQL queries
- Safety constraints (no INSERT/UPDATE/DELETE)
- Quality requirements (verify, explain, etc.)
"""

print("\n" + "="*70)
print("STEP 6: DEFINE AGENT INSTRUCTIONS")
print("="*70)

MSSQL_AGENT_PREFIX = """

You are an agent designed to interact with a SQL database.

## Instructions:
- Given an input question, create a syntactically correct SQL query
to run, then look at the results of the query and return the answer.
- Unless the user specifies a specific number of examples they wish to
obtain, **ALWAYS** limit your query to at most {top_k} results.
- You can order the results by a relevant column to return the most
interesting examples in the database.
- Never query for all the columns from a specific table, only ask for
the relevant columns given the question.
- You have access to tools for interacting with the database.
- You MUST double check your query before executing it. If you get an error
while executing a query, rewrite the query and try again.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.)
to the database.
- DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE, ONLY USE THE RESULTS
OF THE CALCULATIONS YOU HAVE DONE.
- Your response should be in Markdown. However, when running a SQL Query
in "Action Input", do not include the markdown backticks.
Those are only for formatting the response, not for executing the command.
- ALWAYS, as part of your final answer, explain how you got to the answer
on a section that starts with: "Explanation:". Include the SQL query as
part of the explanation section.
- If the question does not seem related to the database, just return
"I don't know" as the answer.
- Only use the below tools. Only use the information returned by the
below tools to construct your query and final answer.
- Do not make up table names, only use the tables returned by any of the
tools below.

## Tools:

"""

print("✓ Created agent PREFIX instructions")
print("\nKey instructions:")
print("  - Limit queries to top_k results")
print("  - Only select relevant columns")
print("  - Double check query before executing")
print("  - No DML statements (INSERT/UPDATE/DELETE)")
print("  - Only use calculation results (no hallucination)")
print("  - Include explanation with SQL query")


# ============================================================================
# STEP 8: DEFINE RESPONSE FORMAT
# ============================================================================
"""
Create instructions for how the agent should format its response.

This FORMAT specifies:
- Question: What user asked
- Thought: Agent's reasoning
- Action: Which tool to use
- Action Input: The actual SQL
- Observation: Database result
- Final Answer: Response to user
- Explanation: How it got there

This is the "Chain of Thought" pattern - makes reasoning transparent!
"""

print("\n" + "="*70)
print("STEP 7: DEFINE RESPONSE FORMAT")
print("="*70)

MSSQL_AGENT_FORMAT_INSTRUCTIONS = """

## Use the following format:

Question: the input question you must answer.
Thought: you should always think about what to do.
Action: the action to take, should be one of [query_sql_db].
Action Input: the input to the action.
Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: the final answer to the original input question.

## Example of Final Answer:

Action: query_sql_db
Action Input: SELECT date, state, hospitalized FROM all_states_history 
WHERE state = 'TX' AND date LIKE '2020-10%' ORDER BY date LIMIT 10

Observation: [(2020-10-01, TX, 1500), (2020-10-02, TX, 1502), ...]

Thought: I now know the final answer

Final Answer: In October 2020, Texas reported the following daily 
hospitalizations...

Explanation:
I queried the all_states_history table for Texas (TX) records from October 2020.
The query returned daily hospitalization numbers for each day of the month.

SQL Query Used:
```sql
SELECT date, state, hospitalized 
FROM all_states_history 
WHERE state = 'TX' AND date LIKE '2020-10%' 
ORDER BY date 
LIMIT 10
```

"""

print("✓ Created agent FORMAT INSTRUCTIONS")
print("\nResponse format includes:")
print("  - Question: What user asked")
print("  - Thought: Agent's reasoning")
print("  - Action: Which tool to use")
print("  - Action Input: The actual SQL")
print("  - Observation: Database result")
print("  - Final Answer: Response to user")
print("  - Explanation: How it got there (with SQL)")


# ============================================================================
# STEP 9: CREATE THE SQL AGENT
# ============================================================================
"""
Combine everything into a working SQL agent!

This agent can:
1. Understand natural language questions
2. Generate SQL queries
3. Execute queries safely
4. Verify results
5. Format responses with explanations
"""

print("\n" + "="*70)
print("STEP 8: CREATE SQL AGENT")
print("="*70)

agent_executor_SQL = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,               # Behavior instructions
    format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,  # Response format
    llm=llm,                                 # The AI model (GPT-4)
    toolkit=toolkit,                         # Database tools
    top_k=30,                                # Limit to 30 rows
    verbose=True                             # Show thinking process
)

print("✓ Created SQL Agent successfully!")
print("\nAgent capabilities:")
print("  - Reads natural language questions")
print("  - Analyzes database schema")
print("  - Writes SQL queries")
print("  - Executes queries safely")
print("  - Verifies results")
print("  - Formats responses")
print("  - Includes explanations")
print("  - Shows SQL used")


# ============================================================================
# STEP 10: DEFINE AND ASK A QUESTION
# ============================================================================
"""
Now we can ask the agent questions!

The agent will:
1. Read the question
2. Decide what query to write
3. Check the query
4. Execute on database
5. Return formatted answer
"""

print("\n" + "="*70)
print("STEP 9: ASK A QUESTION")
print("="*70)

QUESTION = """How many patients were hospitalized during October 2020 
in New York, and nationwide as the total of all states? 
Use the hospitalizedIncrease column"""

print(f"Question: {QUESTION}\n")
print("Agent processing (verbose output):\n")

# Invoke the agent
result = agent_executor_SQL.invoke(QUESTION)

# Display the result
print("\n" + "="*70)
print("FINAL RESPONSE:")
print("="*70)
display(Markdown(result['output']))


# ============================================================================
# STEP 11: ASK MULTIPLE QUESTIONS
# ============================================================================
"""
You can ask follow-up questions to dig deeper.
The agent can handle any data question!
"""

print("\n" + "="*70)
print("STEP 10: ASK FOLLOW-UP QUESTIONS")
print("="*70)

follow_up_questions = [
    "Which state had the highest number of hospitalizations in October 2020?",
    "What was the total number of COVID deaths nationwide in October 2020?",
    "Show me the top 5 states by hospitalizations in October 2020",
]

for i, question in enumerate(follow_up_questions, 1):
    print(f"\nQuestion {i}: {question}")
    print("Processing...")
    
    response = agent_executor_SQL.invoke(question)
    
    # Show just the answer (not full verbose output)
    print(f"Answer: {response['output'][:300]}...\n")


# ============================================================================
# STEP 12: QUERYING DATABASE DIRECTLY (WITHOUT AGENT)
# ============================================================================
"""
Sometimes you might want to query the database directly
without using the AI agent.

This is useful for:
- Quick checks
- Learning SQL
- Verifying results
- Debugging
"""

print("\n" + "="*70)
print("BONUS: DIRECT DATABASE QUERIES")
print("="*70)

# Query database directly using SQLAlchemy
from sqlalchemy import text

print("\nDirect Query 1: How many rows in database?")
with engine.connect() as connection:
    result = connection.execute(text("SELECT COUNT(*) FROM all_states_history"))
    row_count = result.fetchone()[0]
    print(f"Answer: {row_count} rows")

print("\nDirect Query 2: Which states are in the database?")
with engine.connect() as connection:
    result = connection.execute(text(
        "SELECT DISTINCT state FROM all_states_history ORDER BY state"
    ))
    states = [row[0] for row in result.fetchall()]
    print(f"States: {', '.join(states)}")

print("\nDirect Query 3: Date range of data?")
with engine.connect() as connection:
    result = connection.execute(text(
        "SELECT MIN(date), MAX(date) FROM all_states_history"
    ))
    min_date, max_date = result.fetchone()
    print(f"Date range: {min_date} to {max_date}")


# ============================================================================
# STEP 13: BUILDING A REUSABLE FUNCTION
# ============================================================================
"""
Create a reusable function for asking database questions.
This makes it easy to integrate into applications.
"""

print("\n" + "="*70)
print("BONUS: REUSABLE QUESTION FUNCTION")
print("="*70)

def ask_database_question(agent, question, show_verbose=False):
    """
    Ask a question about the database using the SQL agent.
    
    Args:
        agent: The SQL agent (agent_executor_SQL)
        question (str): Natural language question
        show_verbose (bool): Show agent thinking (default: False)
    
    Returns:
        str: The agent's detailed response with explanation
    
    Example:
        >>> answer = ask_database_question(
        ...     agent_executor_SQL,
        ...     "How many total cases in 2020?"
        ... )
        >>> print(answer)
    """
    
    # Set verbose mode
    agent.verbose = show_verbose
    
    # Get response
    response = agent.invoke(question)
    
    # Return the output (formatted response)
    return response['output']


# Test the function
print("\nUsing the reusable function:\n")

answer = ask_database_question(
    agent_executor_SQL,
    "What was the total number of cases in New York during 2020?",
    show_verbose=False
)

print(answer[:500] + "...")  # Show first 500 chars


# ============================================================================
# STEP 14: SAVING RESULTS
# ============================================================================
"""
Save analysis results for later use or sharing.
"""

print("\n" + "="*70)
print("BONUS: SAVING RESULTS")
print("="*70)

def save_database_analysis(question, response, filename="analysis.md"):
    """
    Save database analysis to a file.
    
    Args:
        question (str): The question asked
        response (str): The AI's response
        filename (str): Where to save
    """
    
    with open(filename, 'w') as f:
        f.write(f"# Database Analysis\n\n")
        f.write(f"## Question\n{question}\n\n")
        f.write(f"## Response\n{response}\n\n")
        f.write(f"## Metadata\n")
        f.write(f"- Database: all-states-history (SQLite)\n")
        f.write(f"- Total rows: 20,780\n")
        f.write(f"- Generated: {pd.Timestamp.now()}\n")
    
    print(f"✓ Analysis saved to {filename}")


# Save an example
save_database_analysis(
    "How many patients were hospitalized in October 2020?",
    result['output'],
    "database_analysis_result.md"
)


# ============================================================================
# STEP 15: KEY CONCEPTS SUMMARY
# ============================================================================
"""
WHAT YOU LEARNED IN LESSON 3:

1. SQL DATABASES
   - Superior to CSV for large data
   - Scales to billions of rows
   - Query optimization built-in
   - Multi-user access possible

2. SQLALCHEMY
   - Python-to-SQL bridge
   - Create engines for connection
   - Read/write data easily
   - Support for multiple databases

3. SQL AGENTS
   - AI writes SQL queries
   - Understands natural language
   - Executes safely
   - Returns formatted results

4. SAFETY FIRST
   - No DML statements (no modifications)
   - Verify queries before executing
   - Error handling and retries
   - Only use calculation results

5. CHAIN OF THOUGHT
   - Show reasoning transparently
   - Include SQL in explanation
   - Explain methodology
   - Build trust in results

PROGRESSION:
Lesson 1: Text → Direct Answer
Lesson 2: CSV → Pandas code → Answer
Lesson 3: Database → SQL query → Answer

NEXT STEPS:
1. Try with your own database
2. Ask progressively complex questions
3. Explore agent's reasoning (verbose=True)
4. Connect to production databases
5. Build automated pipelines
"""

print("\n" + "="*70)
print("LESSON 3 COMPLETE!")
print("="*70)
print("""
You've learned:
1. ✓ Create SQL databases from CSV
2. ✓ Connect databases with LangChain
3. ✓ Build AI SQL agents
4. ✓ Ask natural language database questions
5. ✓ Get verified, explained answers
6. ✓ Build production systems

Key Skills Developed:
- Database creation and management
- SQL query understanding
- Natural language to SQL translation
- Prompt engineering for SQL
- Result verification and explanation

You can now:
- Analyze large datasets efficiently
- Build scalable data systems
- Explain data insights clearly
- Create production pipelines
- Query multi-user databases

NEXT: Try with your own data!
""")

# ============================================================================
# STEP 16: TROUBLESHOOTING GUIDE
# ============================================================================
"""
Common Issues & Solutions:

Issue 1: "No such table: all_states_history"
Solution:
    - Make sure CSV file is loaded and written to database
    - Check database_file_path exists
    - Verify df.to_sql() completed successfully

Issue 2: "sqlite3.OperationalError: database is locked"
Solution:
    - Close other connections to database
    - Restart Python kernel
    - Or use different database (PostgreSQL, MySQL)

Issue 3: "Agent returns wrong answer"
Solution:
    - Use verbose=True to see reasoning
    - Check the SQL query in explanation
    - Ask follow-up clarifying questions
    - Verify database has correct data

Issue 4: "Query execution timeout"
Solution:
    - Reduce top_k (return fewer rows)
    - Add WHERE clause to filter data
    - Create database indexes on frequent columns
    - Use larger database (PostgreSQL, SQL Server)

Issue 5: "Not enough memory"
Solution:
    - This shouldn't happen with SQL (unlike Pandas)
    - But if it does, check database size
    - Consider splitting into multiple tables
    - Use streaming/pagination

Issue 6: "SQL syntax error"
Solution:
    - Agent will detect and retry
    - Check verbose output to see error
    - The agent's prompt recovery often fixes it
    - Verify table/column names are correct
"""

print("\n" + "="*70)
print("✅ All steps complete! Your SQL agent is ready!")
print("="*70)
