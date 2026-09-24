# Lesson 2: Interacting with CSV Data - Complete Code Guide 📊

**Author:** Saurabh Shirgaokar  
**Date:** Sep 19, 2026  
**Level:** Intermediate  
**Topic:** Building an AI Data Analyst Agent with LangChain and Pandas

---

## Table of Contents

1. [Overview](#overview)
2. [Key Concepts](#key-concepts)
3. [Code Breakdown](#code-breakdown)
4. [Step-by-Step Walkthrough](#step-by-step-walkthrough)
5. [Visual Flow](#visual-flow)
6. [How the AI Thinks](#how-the-ai-thinks)
7. [Practical Examples](#practical-examples)
8. [Common Use Cases](#common-use-cases)
9. [Advanced Techniques](#advanced-techniques)

---

## Overview

### The Leap from Lesson 1

| Lesson 1 | Lesson 2 |
|----------|----------|
| Simple text translation | Complex data analysis |
| Single question-answer | Multi-step reasoning |
| Basic LangChain usage | Advanced agent creation |
| No data processing | Full data querying with Pandas |
| Static content | Dynamic data exploration |

### What Problem Does This Solve?

Imagine you have a CSV file with millions of rows. Normally you'd need to:
1. Open the file in Excel (might crash with too much data)
2. Write complex SQL queries
3. Use Python with Pandas expertise
4. Verify calculations manually

**With this lesson:** You can just ask the AI in natural language and it does all the work!

```
"How many patients were hospitalized in Texas during July 2020?"
↓
AI reads the question
↓
AI queries the data
↓
AI verifies the answer using multiple methods
↓
You get a detailed, accurate response
```

---

## Key Concepts

### 1. **Pandas DataFrame**

A DataFrame is like a table (spreadsheet) in Python:

```
       date   state  hospitalized  hospitalizedCumulative
    0  2020-07-01  AL      2803.0              2803.0
    1  2020-07-02  AL      2835.0              2835.0
    2  2020-07-03  AL      2883.0              2883.0
    3  2020-07-04  AL      2906.0              2906.0
```

**Key features:**
- Rows = individual records (each date-state combination)
- Columns = attributes (date, state, numbers)
- Can be filtered, grouped, and analyzed
- Integrates perfectly with AI agents

### 2. **CSV Files**

CSV = Comma-Separated Values

```csv
date,state,hospitalized,hospitalizedCumulative
2020-07-01,AL,2803.0,2803.0
2020-07-02,AL,2835.0,2835.0
2020-07-03,AL,2883.0,2883.0
```

Why CSV?
- Human-readable
- Excel-compatible
- Works with databases
- Universal format

### 3. **Pandas Dataframe Agent**

A special LangChain agent that:
- Understands Pandas DataFrames
- Can write Python code automatically
- Executes code safely
- Returns results

**How it works:**
```
User Question
    ↓
Agent (AI) reads the question
    ↓
Agent decides what operations to do
    ↓
Agent writes Python code (using Pandas)
    ↓
Code executes on your data
    ↓
Agent gets results and reasons about them
    ↓
Agent provides final answer
```

### 4. **Agents vs Simple Models**

**Simple Model (Lesson 1):**
```
Question → AI → Answer
(No reasoning, no tools, just text processing)
```

**Agent (Lesson 2):**
```
Question → AI → Write Code → Run Code → Analyze → Reason → Answer
(Can use tools, can execute code, can verify results)
```

### 5. **Prompting Techniques**

Notice the prompt in Lesson 2 has PREFIX and SUFFIX sections:

```python
PREFIX = "First set pandas options, get column names..."
QUESTION = "How many patients were hospitalized?"
SUFFIX = "ALWAYS verify with another method. Don't make up answers..."
```

Why?
- **PREFIX:** Setup instructions
- **QUESTION:** Your actual question
- **SUFFIX:** Quality control instructions (verify, check, explain)

This is called "Prompt Engineering" - designing prompts for better results!

---

## Code Breakdown

### **Chunk 1: Setup and Connect to Azure OpenAI**

```python
import os 
import pandas as pd
from IPython.display import Markdown, HTML, display
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
```

**Line-by-line breakdown:**

| Code | Purpose |
|------|---------|
| `import os` | Access environment variables (API keys) |
| `import pandas as pd` | **NEW:** Import Pandas for data manipulation |
| `from IPython.display...` | Format output in Jupyter notebooks |
| `from langchain.schema...` | Import message format |
| `from langchain_openai...` | **SAME AS LESSON 1:** Import AI model |
| `model = AzureChatOpenAI(...)` | **SAME AS LESSON 1:** Connect to AI |

**What's new?** The Pandas import is key - we'll use it to load and analyze data!

---

### **Chunk 2: Load the Dataset**

```python
df = pd.read_csv("./data/all-states-history.csv").fillna(value=0)
```

**Breaking it down:**

```python
pd.read_csv("./data/all-states-history.csv")
```
- `pd.read_csv()` → Pandas function to read CSV file
- `"./data/all-states-history.csv"` → Path to file
- Returns: A DataFrame with all the CSV data

```python
.fillna(value=0)
```
- `fillna()` → Replace missing values (NaN) with something
- `value=0` → Replace with 0 (instead of blank or error)
- Why? AI works better with clean data, no NaN values

**Complete flow:**
```
CSV File → Pandas reads it → Creates DataFrame → 
Replace empty values → Ready for analysis
```

**What the data looks like:**
```
         date state  hospitalized  hospitalizedCumulative
0    2020-07-01    AL       2803.0                 2803.0
1    2020-07-02    AL       2835.0                 2835.0
2    2020-07-03    AL       2883.0                 2883.0
... (20,780 rows total)
```

---

### **Chunk 3: Prepare the LangChain Dataframe Agent**

This is the **most important part** - where AI learns to analyze data!

```python
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

agent = create_pandas_dataframe_agent(llm=model, df=df, verbose=True)

agent.invoke("how many rows are there?")
```

**Breaking it down:**

#### Import statements
```python
from langchain.agents.agent_types import AgentType
```
- Imports agent types (different kinds of reasoning strategies)

```python
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
```
- **EXPERIMENTAL:** This is a newer LangChain feature
- `create_pandas_dataframe_agent` → Factory function to create a data agent
- Special feature: Designed specifically for Pandas DataFrames

#### Create the agent
```python
agent = create_pandas_dataframe_agent(
    llm=model,           # Which AI model to use (our GPT-4)
    df=df,               # The DataFrame to analyze
    verbose=True         # Show thinking process (helpful for learning)
)
```

**Parameters explained:**

| Parameter | What it does | Example |
|-----------|------------|---------|
| `llm=model` | The AI brain to use | GPT-4 from Azure |
| `df=df` | The data to analyze | COVID tracking data (20,780 rows) |
| `verbose=True` | Show all thinking steps | Prints "Thought", "Action", "Observation" |

#### Invoke the agent
```python
agent.invoke("how many rows are there?")
```

- `invoke()` → Send a question to the agent
- The agent uses Python to answer: `df.shape[0]` (gets 20,780)
- **Output:**
```
{
    'input': 'how many rows are there?',
    'output': 'The dataframe has 20,780 rows.'
}
```

**When verbose=True, you see the thinking:**
```
> Entering new AgentExecutor chain...
Thought: To determine rows, I'll use df.shape[0]
Action: python_repl_ast
Action Input: df.shape[0]
Observation: 20780
Thought: I now know the final answer
Final Answer: The dataframe has 20,780 rows.
> Finished chain.
```

---

### **Chunk 4: Design Your Prompt and Ask Questions**

This is where the **real power** emerges!

```python
CSV_PROMPT_PREFIX = """
First set the pandas display options to show all the columns,
get the column names, then answer the question.
"""

CSV_PROMPT_SUFFIX = """
- **ALWAYS** before giving the Final Answer, try another method.
Then reflect on the answers of the two methods you did and ask yourself
if it answers correctly the original question.
If you are not sure, try another method.
- If the methods tried do not give the same result, reflect and
try again until you have two methods that have the same result.
- If you still cannot arrive to a consistent result, say that
you are not sure of the answer.
- If you are sure of the correct answer, create a beautiful
and thorough response using Markdown.
- **DO NOT MAKE UP AN ANSWER OR USE PRIOR KNOWLEDGE,
ONLY USE THE RESULTS OF THE CALCULATIONS YOU HAVE DONE**.
- **ALWAYS**, as part of your "Final Answer", explain how you got
to the answer on a section that starts with: "\n\nExplanation:\n".
In the explanation, mention the column names that you used to get
to the final answer.
"""

QUESTION = "How many patients were hospitalized during July 2020 in Texas?"

agent.invoke(CSV_PROMPT_PREFIX + QUESTION + CSV_PROMPT_SUFFIX)
```

**Understanding the prompt structure:**

```
PREFIX (Setup instructions)
    ↓
QUESTION (Your actual question)
    ↓
SUFFIX (Quality control + verification instructions)
```

**Why this structure?**

1. **PREFIX:** Tells AI to prepare (show columns, understand data structure)
2. **QUESTION:** The actual question you want answered
3. **SUFFIX:** Instructions for accuracy (verify, don't make up, explain)

**Key SUFFIX instructions:**

| Instruction | Why? | Example |
|------------|------|---------|
| "Try another method" | Catch errors by cross-checking | Use 2 different Pandas operations |
| "Don't make up answers" | Prevent hallucinations | Only report what data shows |
| "Include explanation" | Transparency | Explain which columns were used |

**AI's reasoning process:**

```
1. Read PREFIX → Understand data structure
2. Read QUESTION → Identify the task
3. Read SUFFIX → Remember quality rules
4. Write Python code → Use Pandas to query data
5. Run code → Get results
6. Try another method → Verify answer
7. Compare results → Are they the same?
8. Create response → With explanation
9. Check against SUFFIX → Does it follow all rules?
10. Return final answer
```

---

## Step-by-Step Walkthrough

Let's trace through a real example from the notebook:

### The Question
```
"How many patients were hospitalized during July 2020 in Alabama?"
```

### What the AI Does (Step by Step)

#### Step 1: Understand the Data
```python
# AI thinks: "I need to know what columns exist"
# AI does:
df.columns  # Lists all column names
# AI learns:
# - 'date' column exists (so can filter by July 2020)
# - 'state' column exists (so can filter by Alabama)
# - 'hospitalized' column exists (the number we need!)
```

#### Step 2: Filter for July 2020
```python
# AI thinks: "I need only July 2020 data"
# AI does:
df['date'] = pd.to_datetime(df['date'])  # Convert to date format
july_data = df[(df['date'] >= '2020-07-01') & 
               (df['date'] <= '2020-07-31')]
# Result: Only rows where date is in July 2020
```

#### Step 3: Filter for Alabama
```python
# AI thinks: "I need only Alabama (AL) data"
# AI does:
alabama_july = july_data[july_data['state'] == 'AL']
# Result: Only Alabama records in July 2020
```

#### Step 4: Sum the Hospitalized Column
```python
# AI thinks: "I need to total the hospitalizations"
# AI does:
alabama_july['hospitalized'].sum()
# Result: 206,707.0
```

#### Step 5: Verify with Another Method
```python
# AI thinks: "Let me double-check using cumulative data"
# AI does:
alabama_july['hospitalizedCumulative'].iloc[-1] - \
alabama_july['hospitalizedCumulative'].iloc[0]
# Result: -7,718.0 (Wait, this is different!)
```

#### Step 6: Investigate the Discrepancy
```python
# AI thinks: "The methods gave different results. Let me investigate."
# AI does:
alabama_july[['date', 'hospitalized', 'hospitalizedCumulative']]
# AI observes: The data shows daily hospitalizations, not cumulative
# AI realizes: First method is correct!
```

#### Step 7: Final Verification
```python
# AI thinks: "Let me confirm the first method one more time"
# AI does:
alabama_july['hospitalized'].sum()
# Result: 206,707.0 ✓ (Same as before)
```

#### Step 8: Create Final Answer
```markdown
The total number of patients hospitalized in Alabama during July 2020 is **206,707.0**.

Explanation:
1. **Relevant Columns:** The 'hospitalized' column represents daily hospitalizations
2. **Method Used:** Filtered for July 2020 and Alabama, then summed the column
3. **Verification:** Confirmed using inspection of the data
```

---

## Visual Flow

### Complete Data Analysis Flow

```
┌─────────────────────────────────────────────┐
│  User Question                              │
│  "How many patients in July 2020 in AL?"    │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Receives Question                       │
│  Reads PREFIX, QUESTION, SUFFIX             │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Understands Task                        │
│  - Need date filtering (July 2020)          │
│  - Need state filtering (AL)                │
│  - Need to sum 'hospitalized' column        │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Writes & Executes Pandas Code           │
│  METHOD 1: df[...].sum() = 206,707.0        │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Verifies (METHOD 2)                     │
│  Cumulative approach = -7,718.0             │
│  MISMATCH! Investigate...                   │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Investigates Discrepancy                │
│  Inspects actual data values                │
│  Understands column meanings                │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Retries Verification (METHOD 3)         │
│  Confirms METHOD 1: 206,707.0 ✓             │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  AI Creates Detailed Response               │
│  - Final Answer: 206,707.0                  │
│  - How columns were used                    │
│  - Why this method was chosen               │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│  Response to User (with Markdown)           │
│  Beautiful, thorough, well-explained        │
└─────────────────────────────────────────────┘
```

### Data Processing Pipeline

```
CSV File (all-states-history.csv)
    │
    ↓
Pandas reads CSV
    │
    ↓
DataFrame created (20,780 rows)
    │
    ↓
Missing values filled with 0
    │
    ↓
DataFrame Agent created
    │
    ├→ AI can now query data
    ├→ AI can write Pandas code
    ├→ AI can reason about results
    └→ AI can verify answers
```

---

## How the AI Thinks

### The AI's Internal Reasoning Loop

When you ask: **"How many patients were hospitalized in July 2020?"**

The AI follows this pattern:

```
1. UNDERSTAND
   ├─ Read the question carefully
   ├─ Identify what data is needed
   └─ Recall column names from PREFIX

2. PLAN
   ├─ Decide what Pandas operations to use
   ├─ Think about filtering (date, state)
   └─ Think about aggregation (sum, mean, etc.)

3. EXECUTE (Method 1)
   ├─ Write Python code
   ├─ Run the code
   └─ Get first result

4. VERIFY (Method 2)
   ├─ Try a different approach
   ├─ Run the code
   └─ Get second result

5. COMPARE
   ├─ Do methods agree?
   ├─ If NO: Investigate why
   └─ If YES: Proceed to answer

6. EXPLAIN
   ├─ Document what columns were used
   ├─ Explain the method
   ├─ Format nicely with Markdown
   └─ Include the explanation

7. VALIDATE (Against SUFFIX)
   ├─ Did I verify with 2 methods?
   ├─ Did I only use calculated results?
   ├─ Did I include explanation?
   └─ Is it thorough and beautiful?

8. RESPOND
   └─ Return final answer with confidence
```

### Why Multiple Methods?

The SUFFIX specifically asks for multiple methods:

**Method 1:** `sum(hospitalized)` = 206,707
**Method 2:** `cumulative difference` = -7,718
**Mismatch!** → Investigate

This is intelligent because:
- Catches errors (what if Method 1 was wrong?)
- Ensures accuracy (only trust if methods agree)
- Shows reasoning (AI isn't just guessing)
- Builds confidence (multiple confirmations)

---

## Practical Examples

### Example 1: Simple Count

**Question:** "How many total COVID cases in the dataset?"

**AI's approach:**
```python
# Method 1:
df['cases'].sum()  # Result: 100,000,000

# Method 2:
df.groupby('state')['cases'].sum().sum()  # Result: 100,000,000 ✓ (Match!)
```

**Answer:** 100,000,000 confirmed by two methods

---

### Example 2: Filtering by Date

**Question:** "What was the death toll in March 2020?"

**AI's approach:**
```python
# Method 1:
march_data = df[df['date'].dt.month == 3]
march_data[df['date'].dt.year == 2020]['deaths'].sum()  # Result: 50,000

# Method 2:
df[(df['date'] >= '2020-03-01') & 
   (df['date'] <= '2020-03-31')]['deaths'].sum()  # Result: 50,000 ✓
```

**Answer:** 50,000 deaths in March 2020

---

### Example 3: State-Level Analysis

**Question:** "Which state had the most hospitalizations?"

**AI's approach:**
```python
# Method 1:
df.groupby('state')['hospitalized'].sum().idxmax()  # Result: CA

# Method 2:
df.groupby('state')['hospitalized'].sum().sort_values(ascending=False).iloc[0]  # Result: CA ✓
```

**Answer:** California had the most hospitalizations

---

## Common Use Cases

### 1. **Quick Data Exploration**
```
Question: "Give me a summary of the data"
AI Response: Shows row count, columns, date range, states covered
```

### 2. **Time-Series Analysis**
```
Question: "How did hospitalizations trend from June to August 2020?"
AI Response: Shows month-by-month changes, calculates percentages
```

### 3. **Geographic Comparison**
```
Question: "Compare hospitalization rates between Texas and California"
AI Response: Calculates per-capita rates, creates comparison
```

### 4. **Anomaly Detection**
```
Question: "Were there any unusual spikes in cases?"
AI Response: Identifies dates with unusual patterns
```

### 5. **Data Validation**
```
Question: "Are there any missing values or inconsistencies?"
AI Response: Checks data quality, reports issues
```

---

## Advanced Techniques

### 1. **Prompt Engineering Best Practices**

**Good prompt:**
```
PREFIX: "First understand the data structure"
QUESTION: "Specific, measurable question"
SUFFIX: "Verify with multiple methods, explain your reasoning"
```

**Bad prompt:**
```
"What's in the data?"  # Vague
```

### 2. **Handling Disagreement**

If Method 1 and Method 2 don't match:
1. AI investigates why
2. Inspects actual values
3. Understands the data better
4. Retries with correct understanding
5. Gets agreement

This is **intelligent reasoning**, not just calling a function!

### 3. **Chaining Questions**

You can ask follow-ups:

```python
# First question
response1 = agent.invoke("What was peak hospitalization in 2020?")

# Follow-up question (agent remembers context)
response2 = agent.invoke("What date did that occur?")
```

### 4. **Custom Column Creation**

AI can create new columns for analysis:

```python
# AI can write:
df['hospitalization_rate'] = df['hospitalized'] / df['population']
df['daily_increase'] = df['cases'].diff()
```

### 5. **Statistical Analysis**

AI can compute statistics:

```python
# Mean, median, std deviation
df['hospitalized'].describe()

# Correlation between columns
df[['cases', 'deaths']].corr()
```

---

## Key Takeaways

### From This Lesson, You Learned:

1. **CSV Loading**
   - `pd.read_csv()` reads CSV files
   - `.fillna()` handles missing data
   - DataFrames are table-like structures

2. **AI Data Agents**
   - Special agents designed for Pandas
   - Can write and execute Python code
   - Can reason about results

3. **Prompt Engineering**
   - PREFIX sets up context
   - QUESTION states the task
   - SUFFIX ensures quality

4. **Verification**
   - Always try multiple methods
   - Compare results
   - Investigate discrepancies

5. **Natural Language to Code**
   - Ask in English
   - AI writes Python
   - AI executes and analyzes

### Why This Matters

Before AI data agents:
- ❌ Required SQL expertise
- ❌ Required Python/Pandas knowledge
- ❌ Manual verification needed
- ❌ Slow analysis process

With AI data agents:
- ✅ Ask in natural language
- ✅ No coding required
- ✅ Automatic verification
- ✅ Fast analysis

---

## Comparison: Lesson 1 vs Lesson 2

| Aspect | Lesson 1 | Lesson 2 |
|--------|----------|----------|
| **Input** | Text | CSV Data |
| **AI Capability** | Text processing | Code execution + reasoning |
| **Complexity** | Simple | Complex |
| **Verification** | None | Multiple methods |
| **Output** | Direct response | Verified analysis |
| **Use Case** | Translation | Data analysis |
| **Tools Used** | LangChain, Azure | LangChain, Pandas, Azure |

---

## Next Steps & Challenges

### Challenge 1: Different Dataset
Use a different CSV file and ask data questions:
```python
df = pd.read_csv("your_data.csv")
agent = create_pandas_dataframe_agent(llm=model, df=df, verbose=True)
agent.invoke("Your question here")
```

### Challenge 2: Complex Queries
```python
question = """
Compare hospitalization rates across states for the first quarter of 2020.
Show which states had the highest and lowest rates.
"""
agent.invoke(question)
```

### Challenge 3: Visualization
```python
# Ask AI to prepare data for visualization
response = agent.invoke("Prepare monthly totals for plotting")
# Then visualize with matplotlib
```

### Challenge 4: Production Pipeline
```python
# Process multiple files
# Automate regular analysis
# Export results
# Schedule queries
```

---

## Troubleshooting

### Issue: "Column not found" error
**Solution:** Check column names with PREFIX
```python
# AI needs to know exact column names
df.columns
```

### Issue: Date filtering not working
**Solution:** Convert to datetime first
```python
df['date'] = pd.to_datetime(df['date'])
```

### Issue: Results don't match
**Solution:** Use the SUFFIX strategy - try another method
The AI will automatically investigate!

### Issue: Too much output
**Solution:** Set `verbose=False`
```python
agent = create_pandas_dataframe_agent(
    llm=model, df=df, verbose=False
)
```

---

## Resources

- 📖 [Pandas Documentation](https://pandas.pydata.org/)
- 📖 [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- 📖 [Agent Types & Tools](https://python.langchain.com/docs/modules/agents/agent_types/)
- 📖 [CSV Format Guide](https://en.wikipedia.org/wiki/Comma-separated_values)

