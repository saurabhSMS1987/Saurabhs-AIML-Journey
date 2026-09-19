# Lesson 3: Connecting to a SQL Database - Complete Code Guide 🗄️

**Author:** Saurabh Shirgaokar  
**Date:** Sep 19, 2026 
**Level:** Advanced  
**Topic:** Building an AI SQL Query Agent with LangChain and SQLite

---

## Table of Contents

1. [Overview](#overview)
2. [The Progression](#the-progression)
3. [Key Concepts](#key-concepts)
4. [Code Breakdown](#code-breakdown)
5. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
6. [Visual Architecture](#visual-architecture)
7. [SQL Agent Deep Dive](#sql-agent-deep-dive)
8. [Practical Examples](#practical-examples)
9. [Advanced Techniques](#advanced-techniques)
10. [Database Setup Guide](#database-setup-guide)

---

## Overview

### What This Lesson Teaches

This lesson takes you to **production-level data analysis** by teaching:
- ✅ Creating SQL databases from CSV data
- ✅ Building AI agents that understand SQL
- ✅ Asking natural language questions about database data
- ✅ Automatic SQL query generation
- ✅ Query verification and error handling
- ✅ Connecting to real databases (not just files)

### Why SQL? Why Now?

**CSV Approach (Lesson 2):**
- ✅ Good for medium datasets
- ✅ All data loaded into memory
- ❌ Slow with large datasets
- ❌ Can't scale to millions of rows

**SQL Database Approach (Lesson 3):**
- ✅ Works with huge datasets
- ✅ Only queries needed data
- ✅ Scales to billions of rows
- ✅ Industry standard
- ✅ Multi-user access
- ✅ Security built-in

### The Progression

```
Lesson 1: Translate text
   ↓
Lesson 2: Analyze CSV data with AI
   ↓
Lesson 3: Query databases with AI ← YOU ARE HERE
   ↓
Lesson 4+: Building production systems
```

---

## The Progression

### From Lesson 2 to Lesson 3

| Aspect | Lesson 2 (CSV) | Lesson 3 (SQL) |
|--------|---|---|
| **Data Source** | CSV file (in memory) | SQL Database (on disk) |
| **Data Size** | Millions of rows (limit) | Billions of rows (unlimited) |
| **Query Speed** | Slow (scan all data) | Fast (optimized queries) |
| **Language** | Pandas Python | SQL |
| **Agent Type** | Pandas Agent | SQL Agent |
| **Real-World Use** | Quick analysis | Production systems |
| **Scalability** | Limited | Unlimited |
| **Multi-user** | No | Yes |

### Conceptual Shift

**Lesson 2:**
```
Question → AI writes Pandas code → Loads all CSV → Filters → Calculates
```

**Lesson 3:**
```
Question → AI writes SQL query → Database fetches needed rows → Returns results
```

---

## Key Concepts

### 1. **SQL Basics (for the AI to use)**

SQL = Structured Query Language (the language databases speak)

**Basic SELECT query:**
```sql
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1
LIMIT 10;
```

**What it does:**
- `SELECT` → Which columns to get
- `FROM` → Which table
- `WHERE` → Filter conditions
- `ORDER BY` → Sort results
- `LIMIT` → How many rows

**Example with real data:**
```sql
SELECT date, state, hospitalized
FROM all_states_history
WHERE state = 'NY' AND date LIKE '2020-10%'
ORDER BY date
LIMIT 10;
```

Result:
```
date       | state | hospitalized
2020-10-01 | NY    | 1500
2020-10-02 | NY    | 1502
2020-10-03 | NY    | 1505
```

### 2. **Databases vs Files**

**CSV Files:**
- Stored on disk as text
- Read entire file into memory
- No query optimization
- Single user access

**SQL Database:**
- Structured, indexed storage
- Only needed data loaded
- Query optimization built-in
- Multi-user, secure access
- ACID compliance (data integrity)

**Example:**
```
CSV:    Need age > 30? Read 1 million rows, filter in memory
SQL:    Need age > 30? Database uses index, returns only matches
```

### 3. **SQLAlchemy: The Bridge**

SQLAlchemy is a Python library that:
- Connects to any SQL database
- Converts Python to SQL
- Handles connections safely
- Works with SQLite, PostgreSQL, MySQL, etc.

```python
# Using SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')
df.to_sql('table_name', con=engine)
```

### 4. **SQLite: Lightweight SQL**

SQLite is:
- Simple SQL database
- Stores in single file
- Perfect for learning
- Good for small-medium apps
- Used by mobile phones, browsers

**Creating SQLite database:**
```python
engine = create_engine('sqlite:///./db/test.db')
df.to_sql('all_states_history', con=engine, if_exists='replace')
```

This creates:
- Folder: `./db/`
- File: `test.db` (contains all data in SQL format)

### 5. **SQL Agent vs Pandas Agent**

**Pandas Agent (Lesson 2):**
```
Question → Python code → Execute → Get DataFrame → Answer
```

**SQL Agent (Lesson 3):**
```
Question → SQL query → Execute on database → Get results → Answer
```

**Key difference:**
- Pandas: Works with data in memory
- SQL: Works with data on disk (more efficient)

### 6. **Agent Prefixes and Instructions**

Lesson 3 introduces very detailed prompts:

**PREFIX:** Instructions for how to behave
```
"You are an agent designed to interact with a SQL database."
"Create syntactically correct SQL queries."
"Limit results to at most {top_k} rows."
"Never query all columns, only relevant ones."
"Check your query before executing."
"No INSERT/UPDATE/DELETE statements."
```

**FORMAT INSTRUCTIONS:** How to structure responses
```
Question: [what user asked]
Thought: [what to do]
Action: [which tool to use]
Action Input: [the actual SQL]
Observation: [what database returned]
...
Final Answer: [the answer]
```

This detailed instruction is crucial for:
- Preventing errors
- Ensuring security
- Consistent behavior
- Easy verification

---

## Code Breakdown

### **Step 1: Imports and Setup**

```python
import os
from IPython.display import Markdown, HTML, display
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_openai import AzureChatOpenAI
from sqlalchemy import create_engine
import pandas as pd
```

**What each import does:**

| Import | Purpose |
|--------|---------|
| `os` | Access environment variables |
| `IPython.display` | Format output in Jupyter |
| `AzureChatOpenAI` | Connect to GPT-4 |
| `create_sql_agent` | **NEW:** Create SQL agent |
| `SQLDatabaseToolkit` | **NEW:** Tools for SQL operations |
| `SQLDatabase` | **NEW:** SQL database connection |
| `create_engine` | **NEW:** SQLAlchemy connection |
| `pandas` | Data manipulation |

**Key new imports:**
- `create_sql_agent` → Makes SQL agents
- `SQLDatabaseToolkit` → Provides SQL tools to agent
- `SQLDatabase` → Connection to database
- `create_engine` → SQLAlchemy engine

---

### **Step 2: Load CSV Data (Same as Lesson 2)**

```python
df = pd.read_csv("./data/all-states-history.csv").fillna(value=0)
```

This is **identical to Lesson 2**:
- Reads CSV file
- Fills missing values with 0
- Creates a Pandas DataFrame

Nothing new here!

---

### **Step 3: Move Data to SQL Database (NEW!)**

```python
database_file_path = "./db/test.db"

engine = create_engine(f'sqlite:///{database_file_path}')

df.to_sql(
    'all_states_history',
    con=engine,
    if_exists='replace',
    index=False
)
```

**Breaking it down:**

#### Create SQLAlchemy Engine
```python
engine = create_engine(f'sqlite:///{database_file_path}')
```
- `create_engine()` → Create database connection
- `sqlite:///...` → Protocol: use SQLite at this path
- `./db/test.db` → Create database file here
- Returns: An engine (connection object)

#### Write DataFrame to Database
```python
df.to_sql(
    'all_states_history',  # Table name to create
    con=engine,            # Which database to use
    if_exists='replace',   # If table exists: replace it
    index=False            # Don't save index column
)
```

**Parameters explained:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Table name | `'all_states_history'` | What to call the SQL table |
| `con` | `engine` | Which database to write to |
| `if_exists` | `'replace'` | Recreate table if it exists |
| `index` | `False` | Don't save DataFrame index |

**What happens:**
```
Pandas DataFrame (in memory)
    ↓
SQLAlchemy translates to SQL
    ↓
SQL: CREATE TABLE all_states_history (...)
    ↓
Inserts all 20,780 rows
    ↓
Database saved to ./db/test.db
```

**Result:**
- File created: `./db/test.db` (SQLite database)
- Table created: `all_states_history`
- Rows inserted: 20,780
- Ready for SQL queries!

---

### **Step 4: Define Agent Prompts (NEW!)**

This is **much more detailed** than Lesson 2!

#### Prefix Instructions
```python
MSSQL_AGENT_PREFIX = """
You are an agent designed to interact with a SQL database.
## Instructions:
- Create syntactically correct {dialect} query
- Limit results to {top_k} rows
- Order results by relevant column
- Never query all columns, only relevant ones
- Double check query before executing
- No DML statements (INSERT, UPDATE, DELETE, DROP)
- Only use results from calculations
- Response in Markdown
- Include SQL query in explanation
- If not database-related, say "I don't know"
- Only use provided tools
- Don't make up table names
"""
```

**Why these instructions?**

| Instruction | Why |
|------------|-----|
| "Syntactically correct SQL" | Prevent errors |
| "Limit to top_k rows" | Prevent returning too much data |
| "Order by relevant column" | Get most interesting results first |
| "Never all columns" | Efficiency (only needed data) |
| "Double check query" | Catch errors before executing |
| "No DML statements" | Security (prevent data modification) |
| "Only use calculation results" | Accuracy (no hallucinations) |
| "Response in Markdown" | Better formatting |
| "Include SQL in explanation" | Transparency |
| "Only use provided tools" | Safety (no unknown operations) |

#### Format Instructions
```python
MSSQL_AGENT_FORMAT_INSTRUCTIONS = """
## Format:
Question: the input question
Thought: what to do
Action: which tool [query_sql_db]
Action Input: the SQL query (no backticks)
Observation: database result
... (repeat as needed)
Thought: I now know final answer
Final Answer: the answer

Example:
Action: query_sql_db
Action Input: SELECT TOP (10) [death] FROM covidtracking 
WHERE state = 'TX' AND date LIKE '2020%'
Observation: [(27437.0,), (27088.0,), ...]
Thought: I now know final answer
Final Answer: There were 27437 deaths in Texas in 2020.

Explanation:
I queried the covidtracking table for deaths where 
state is TX and year is 2020...
"""
```

**Why this structure?**
- **Question** → What user asked
- **Thought** → AI's reasoning
- **Action** → Which tool to use
- **Action Input** → The SQL query
- **Observation** → Database result
- **Final Answer** → The response to user
- **Explanation** → How it got the answer

This is the **Chain of Thought** pattern that makes AI reasoning transparent!

---

### **Step 5: Create SQL Agent**

```python
llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0,
    max_tokens=500
)

db = SQLDatabase.from_uri(f'sqlite:///{database_file_path}')
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor_SQL = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,
    format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,
    llm=llm,
    toolkit=toolkit,
    top_k=30,
    verbose=True
)
```

**Breaking it down:**

#### Create LLM Connection
```python
llm = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0,       # Deterministic (no randomness)
    max_tokens=500       # Limit response length
)
```

**New parameters:**
- `temperature=0` → No randomness (exact same answer each time)
- `max_tokens=500` → Keep responses concise

#### Connect to Database
```python
db = SQLDatabase.from_uri(f'sqlite:///{database_file_path}')
```
- `SQLDatabase.from_uri()` → Connect to SQL database
- Takes: Database URI (location/connection string)
- Returns: SQLDatabase object (can query)

#### Create Toolkit
```python
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
```
- Combines database + LLM
- Provides tools like:
  - `query_sql_db` → Execute SQL
  - `get_schema` → See table structure
  - `get_table_info` → See column info

#### Create Agent
```python
agent_executor_SQL = create_sql_agent(
    prefix=MSSQL_AGENT_PREFIX,           # Instructions
    format_instructions=MSSQL_AGENT_FORMAT_INSTRUCTIONS,  # Response format
    llm=llm,                             # The AI model
    toolkit=toolkit,                     # SQL tools
    top_k=30,                            # Limit 30 rows
    verbose=True                         # Show thinking
)
```

**What this does:**
- Takes all parts (instructions, model, tools)
- Creates an agent that can:
  - Read natural language questions
  - Write SQL queries
  - Execute on database
  - Return formatted answers

---

### **Step 6: Invoke the Agent**

```python
QUESTION = """How many patients were hospitalized during October 2020
in New York, and nationwide as the total of all states?
Use the hospitalizedIncrease column"""

result = agent_executor_SQL.invoke(QUESTION)
print(result)
```

**What happens:**

1. Agent receives question
2. Agent reads PREFIX (setup instructions)
3. Agent reads FORMAT INSTRUCTIONS (response format)
4. Agent thinks: "I need to query database"
5. Agent writes SQL:
   ```sql
   SELECT state, SUM(hospitalizedIncrease) as total
   FROM all_states_history
   WHERE date LIKE '2020-10%'
   GROUP BY state
   ```
6. Database executes query
7. Results returned to agent
8. Agent formats response with Markdown
9. Agent includes explanation with SQL query
10. User gets detailed answer

---

## Step-by-Step Walkthrough

### The Question
```
"How many patients were hospitalized during October 2020 
in New York, and nationwide?"
```

### What the Agent Does

#### Step 1: Understand the Question
```
Needs:
- Table: all_states_history
- Column: hospitalizedIncrease
- Filter: October 2020 (date LIKE '2020-10%')
- States: NY (specific) + all states (total)
```

#### Step 2: Plan the Query
```
Two separate queries needed:
1. For New York:
   SELECT SUM(hospitalizedIncrease)
   FROM all_states_history
   WHERE state = 'NY' AND date LIKE '2020-10%'

2. For all states:
   SELECT SUM(hospitalizedIncrease)
   FROM all_states_history
   WHERE date LIKE '2020-10%'
```

#### Step 3: Check Query Before Executing
```
SQL syntax check:
- Table name correct? ✓
- Column names correct? ✓
- Date filter correct? ✓
- Aggregation correct? ✓
```

#### Step 4: Execute Query 1 (New York)
```sql
SELECT SUM(hospitalizedIncrease)
FROM all_states_history
WHERE state = 'NY' AND date LIKE '2020-10%'
```

**Result:** 50,000 hospitalizations

#### Step 5: Execute Query 2 (All States)
```sql
SELECT SUM(hospitalizedIncrease)
FROM all_states_history
WHERE date LIKE '2020-10%'
```

**Result:** 500,000 hospitalizations (nationwide)

#### Step 6: Format Response
```markdown
# Hospitalization Data for October 2020

**New York:** 50,000 patients
**Nationwide Total:** 500,000 patients

## Explanation:
I queried the all_states_history table using the 
hospitalizedIncrease column for dates in October 2020.

For New York specifically, the sum of hospitalizedIncrease 
was 50,000.

For all states combined, the sum was 500,000.

### SQL Queries Used:
```sql
-- New York only
SELECT SUM(hospitalizedIncrease)
FROM all_states_history
WHERE state = 'NY' AND date LIKE '2020-10%'

-- All states
SELECT SUM(hospitalizedIncrease)
FROM all_states_history
WHERE date LIKE '2020-10%'
```
```

#### Step 7: Return to User
User sees formatted, explained response with confidence!

---

## Visual Architecture

### Complete Data Flow

```
STEP 1: Natural Language Question
   Input: "Hospitalizations in October 2020?"
                    ↓
STEP 2: SQL Agent Receives Question
   - Reads PREFIX (behavior instructions)
   - Reads FORMAT INSTRUCTIONS
   - Understands task
                    ↓
STEP 3: Agent Analyzes Query Requirements
   - Need table: all_states_history
   - Need column: hospitalizedIncrease
   - Need filter: October 2020
   - Need to group by state
                    ↓
STEP 4: Agent Writes SQL Query
   SELECT SUM(hospitalizedIncrease)
   FROM all_states_history
   WHERE date LIKE '2020-10%'
   GROUP BY state
                    ↓
STEP 5: Agent Validates Query
   ✓ Syntax valid
   ✓ Safe (no INSERT/UPDATE/DELETE)
   ✓ Limits applied
   ✓ Ready to execute
                    ↓
STEP 6: SQLAlchemy Executes on SQLite
   Database receives validated query
                    ↓
STEP 7: Database Returns Results
   NY: 50,000 hospitalizations
   CA: 45,000 hospitalizations
   TX: 40,000 hospitalizations
   ... (all states)
                    ↓
STEP 8: Agent Formats Response
   - Creates Markdown formatting
   - Includes SQL query used
   - Explains methodology
   - Shows results clearly
                    ↓
STEP 9: User Receives Answer
   Complete, verified, well-explained response
```

Columns:
- date (e.g., 2020-10-01)
- state (e.g., NY, CA, TX)
- hospitalized (numeric)
- hospitalizedCumulative (numeric)
- cases (numeric)
- death (numeric)
- ... (other columns)

Total Rows: 20,780

Sample Data:
date       | state | hospitalized | cases  | death
-----------|-------|--------------|--------|-------
2020-10-01 | NY    | 1500         | 15000  | 150
2020-10-01 | CA    | 2000         | 20000  | 200
2020-10-02 | NY    | 1502         | 15200  | 152
2020-10-02 | CA    | 2050         | 20500  | 205
... (20,776 more rows)
```

---

## SQL Agent Deep Dive

### How SQL Agent is Different from Pandas Agent

**Pandas Agent (Lesson 2):**
```
1. Load entire CSV into DataFrame
2. Write Pandas code
3. Execute Python
4. Reason about results
5. Return answer

Issues:
- All data in memory (slow)
- Can't scale to big data
- Limited to available RAM
```

**SQL Agent (Lesson 3):**
```
1. Connect to database
2. Write SQL query
3. Database executes (optimized)
4. Returns only needed rows
5. Reason about results
6. Return answer

Advantages:
- Only needed data loaded
- Scales to huge datasets
- Leverages database optimization
- Can handle millions/billions rows
```

### Agent Reasoning Loop

The agent follows this thinking pattern:

**Step 1: Receive Question**
   Question: "How many patients hospitalized in October 2020?"
   ↓
**Step 2: Analyze Question**
   Think: "What does this mean?"
   Think: "Which table has this data?"
   ↓
**Step 3: Query Database Schema**
   Action: Query database metadata
   Observe: Get table and column information
   ↓
**Step 4: Plan SQL Query**
   Think: "How to construct the SQL?"
   Think: "What columns do I need?"
   Think: "How to filter by date?"
   Think: "What aggregation to use?"
   ↓
**Step 5: Write SQL Query**
   Action: Create SQL query
   Query: SELECT SUM(hospitalized) FROM ... WHERE ...
   ↓
**Step 6: Validate Query**
   Think: "Is this SQL syntactically valid?"
   Think: "Is it safe (no INSERT/DELETE)?"
   Check: Does it follow all safety rules?
   ↓
**Step 7: Execute Query**
   Action: Execute query on SQLite database
   ↓
**Step 8: Receive Results**
   Observe: Get database results
   Results: 50,000 (NY), 500,000 (Nationwide)
   ↓
**Step 9: Verify Answer**
   Think: "Does this answer the question?"
   Think: "Do the numbers make sense?"
   ↓
**Step 10: Format Response**
   Action: Create beautiful Markdown response
   Include: SQL query used
   Include: Explanation section
   ↓
**Step 11: Return Answer**
   Output: Complete, verified response to user

### Error Handling

The agent is built to handle errors:

```python
# If query fails...
try:
    Execute SQL query
except SyntaxError:
    Agent thinks: "Query has syntax error"
    Agent rewrites query
    Retry execution
except OtherError:
    Agent thinks: "Different issue"
    Agent tries alternative approach
    Retry execution
```

This is why the PREFIX says: "If you get an error, rewrite and try again"

---

## Practical Examples

### Example 1: State Comparison

**Question:**
```
"Which state had the most COVID deaths in 2020?"
```

**Agent's SQL:**
```sql
SELECT TOP 1 state, SUM(death) as total_deaths
FROM all_states_history
WHERE date LIKE '2020%'
GROUP BY state
ORDER BY total_deaths DESC
```

**Result:**
```
state: NY
total_deaths: 35,000
```

---

### Example 2: Time Series Analysis

**Question:**
```
"Show me the progression of cases week by week in Texas during 2020"
```

**Agent's SQL:**
```sql
SELECT 
    strftime('%Y-W%W', date) as week,
    SUM(cases) as weekly_cases
FROM all_states_history
WHERE state = 'TX' AND date LIKE '2020%'
GROUP BY week
ORDER BY week
```

**Result:**
```
Week   | Cases
2020-01| 100
2020-02| 150
2020-03| 200
... (increases over time)
```

---

### Example 3: Multi-State Comparison

**Question:**
```
"Compare hospitalization rates across CA, TX, and NY in Q3 2020"
```

**Agent's SQL:**
```sql
SELECT 
    state,
    SUM(hospitalized) as total_hospitalized,
    COUNT(*) as days
FROM all_states_history
WHERE state IN ('CA', 'TX', 'NY') 
  AND date LIKE '2020-07%' OR date LIKE '2020-08%' OR date LIKE '2020-09%'
GROUP BY state
```

**Result:**
```
state | total_hospitalized | days
CA    | 50,000            | 92
TX    | 40,000            | 92
NY    | 35,000            | 92
```

---

## Advanced Techniques

### 1. **Joins (Combining Multiple Tables)**

If you had multiple tables:

```python
# Create another table
demographics_df.to_sql('state_demographics', con=engine)

# Agent can write queries like:
SELECT 
    h.state,
    h.date,
    h.cases,
    d.population
FROM all_states_history h
JOIN state_demographics d ON h.state = d.state
WHERE h.date LIKE '2020-10%'
```

### 2. **Complex Aggregations**

Agent can write sophisticated SQL:

```sql
SELECT 
    state,
    DATE(date) as day,
    AVG(hospitalized) as avg_daily,
    MAX(hospitalized) as peak,
    MIN(hospitalized) as low
FROM all_states_history
WHERE date LIKE '2020-10%'
GROUP BY state, DATE(date)
HAVING AVG(hospitalized) > 100
ORDER BY avg_daily DESC
```

### 3. **Window Functions (Advanced)**

```sql
SELECT 
    state,
    date,
    cases,
    SUM(cases) OVER (
        PARTITION BY state 
        ORDER BY date
    ) as running_total
FROM all_states_history
WHERE date LIKE '2020%'
```

### 4. **Indexing for Performance**

For large databases:

```python
# Create index on frequently-queried columns
from sqlalchemy import Index

# This would be done on large production databases
# to speed up queries
```

### 5. **Query Optimization**

The agent benefits from:
- Database indexes (fast lookups)
- Query optimization (database side)
- Limiting results (reduce data transfer)
- Selecting only needed columns (reduce bandwidth)

---

## Database Setup Guide

### Creating a SQLite Database from Scratch

#### Step 1: Install required packages
```bash
pip install sqlalchemy pandas openpyxl
```

#### Step 2: Create database from CSV
```python
from sqlalchemy import create_engine
import pandas as pd

# Read CSV
df = pd.read_csv("data.csv")

# Create engine (creates DB if doesn't exist)
engine = create_engine('sqlite:///my_database.db')

# Write to database
df.to_sql('my_table', con=engine, if_exists='replace', index=False)
```

#### Step 3: Verify database was created
```python
# Check tables in database
from sqlalchemy import inspect

inspector = inspect(engine)
print(inspector.get_table_names())  # Should show ['my_table']

# Check columns
print(inspector.get_columns('my_table'))
```

#### Step 4: Query the database
```python
# Simple query
result = engine.execute("SELECT * FROM my_table LIMIT 5")
for row in result:
    print(row)
```

### Connecting to Existing Database

```python
# SQLite
engine = create_engine('sqlite:///./path/to/database.db')

# PostgreSQL
engine = create_engine('postgresql://user:password@localhost/dbname')

# MySQL
engine = create_engine('mysql+pymysql://user:password@localhost/dbname')

# SQL Server
engine = create_engine('mssql+pyodbc://user:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server')
```

---

## Key Takeaways

### What You Learned

1. **SQL Databases**
   - Superior to CSV for large data
   - Scalable to billions of rows
   - Optimized query execution
   - Multi-user access

2. **SQL Agents**
   - AI that writes SQL automatically
   - Understands natural language
   - Executes database queries
   - Returns formatted results

3. **SQLAlchemy**
   - Python-to-SQL bridge
   - Supports multiple databases
   - Simple API for database operations
   - Connection pooling and safety

4. **Detailed Prompting**
   - PREFIX for instructions
   - FORMAT for response structure
   - Safety constraints (no DML)
   - Verification requirements

5. **Agent Reasoning**
   - Chain of Thought visible
   - Transparent decision-making
   - Error handling and retries
   - Verification of results

### Why This Matters

**Before AI SQL agents:**
- Needed database expertise
- Required SQL knowledge
- Manual query writing
- Error-prone process

**With AI SQL agents:**
- Ask in natural language
- AI writes SQL
- Automatic verification
- Production-ready responses

### Skills You Now Have

1. ✅ Load CSV into SQL database
2. ✅ Connect to databases with LangChain
3. ✅ Create SQL agents
4. ✅ Ask complex database questions
5. ✅ Get verified, detailed answers
6. ✅ Build scalable data systems

---

## Comparison: All Three Lessons

**Progression Overview:**

| Feature | Lesson 1 | Lesson 2 | Lesson 3 |
|:--------|:--------:|:--------:|:--------:|
| Input Type | Text | CSV File | SQL Database |
| Data Size Limit | N/A | Millions | Billions |
| Agent Type | Simple Text | Pandas Code | SQL Query |
| Execution Speed | Instant | Seconds | Milliseconds |
| Scalability | N/A | Limited | Unlimited |
| Real-World Use | Translation | Quick analysis | Production Systems |
| Complexity Level | Beginner | Intermediate | Advanced |

**Data Processing Comparison:**

```
Lesson 1: Text Processing
─────────────────────────
Question → AI → Answer
(Simple, direct)

Lesson 2: CSV Analysis
─────────────────────────
Question → AI writes Pandas → Load CSV → Filter → Calculate → Answer
(Medium complexity, file-based)

Lesson 3: Database Queries
─────────────────────────
Question → AI writes SQL → Query DB → Fetch rows → Format → Answer
(Advanced, production-grade)
```

---

## Next Steps

### Challenge 1: Different Database
```python
# Use a different CSV file
df = pd.read_csv("your_data.csv")
engine = create_engine('sqlite:///your_db.db')
df.to_sql('your_table', con=engine)
```

### Challenge 2: Multiple Tables
```python
# Create multiple tables in same database
table1_df.to_sql('table1', con=engine)
table2_df.to_sql('table2', con=engine)

# Agent can write JOINs between them
```

### Challenge 3: Production Database
```python
# Connect to PostgreSQL or MySQL
engine = create_engine('postgresql://user:pass@host/db')

# Much larger datasets
# Real-world application
```

### Challenge 4: Automated Queries
```python
# Schedule regular queries
# Export results
# Build dashboards
# Real production pipeline
```

---

## Resources

- 📖 [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- 📖 [SQLite Documentation](https://www.sqlite.org/docs.html)
- 📖 [LangChain SQL Agent](https://python.langchain.com/docs/modules/agents/toolkits/sql_database/)
- 📖 [SQL Tutorial](https://www.w3schools.com/sql/)
- 📖 [Database Design](https://en.wikipedia.org/wiki/Database_design)

---

## Summary

**Lesson 3 unlocks enterprise-level data analysis:**

You can now:
1. ✅ Create SQL databases from data
2. ✅ Build AI agents that query databases
3. ✅ Ask complex questions in English
4. ✅ Get intelligent SQL queries generated
5. ✅ Scale to massive datasets
6. ✅ Build production systems

This foundation supports:
- 🚀 **Advanced topics:** Optimization, scaling, security
- 🚀 **Production deployment:** Real databases, real users
- 🚀 **Complex analysis:** Advanced SQL, multiple tables
- 🚀 **Career growth:** Database engineer, data specialist

---

**You're now ready to build professional data systems! 🗄️🚀**
