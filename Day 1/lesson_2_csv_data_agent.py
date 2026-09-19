"""
Lesson 2: Interacting with CSV Data
====================================

Learn how to build an AI agent that analyzes data from CSV files.

This script demonstrates:
- Loading CSV data with Pandas
- Creating an AI data agent
- Asking natural language questions about data
- Automatic verification and reasoning
- Creating thorough, verified responses

Author: Saurabh Shirgaokar
Date: 2026
Level: Intermediate

What This Does:
- Loads COVID tracking data (CSV file)
- Creates an AI agent that understands the data
- Asks complex questions in natural language
- AI analyzes data using Pandas
- AI verifies results using multiple methods
- Returns detailed, accurate answers
"""

# ============================================================================
# STEP 1: SETUP & IMPORTS
# ============================================================================
"""
Import all necessary libraries.
Key additions from Lesson 1:
- pandas: For working with data tables (CSV files)
- LangChain experimental agents: For creating data analysis agents
"""

import os
import pandas as pd
from IPython.display import Markdown, HTML, display

# Import LangChain components (from Lesson 1)
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

# NEW: Import agent creation tools
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


# ============================================================================
# STEP 2: CONNECT TO AZURE OPENAI (SAME AS LESSON 1)
# ============================================================================
"""
Create connection to GPT-4 model.
This is identical to Lesson 1 - we're using the same AI model.
The difference is HOW we use it (simple messages vs agents).
"""

model = AzureChatOpenAI(
    # API version
    openai_api_version="2023-05-15",
    # Which model to use
    azure_deployment="gpt-4-1106",
    # Where the model lives (from environment)
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

"""
At this point:
- We have connected to GPT-4
- The model is ready to use
- Same as Lesson 1, but we'll use it differently
"""


# ============================================================================
# STEP 3: LOAD THE CSV DATA
# ============================================================================
"""
Load data from a CSV file into a Pandas DataFrame.

CSV = Comma-Separated Values (a simple table format)
File: all-states-history.csv (COVID-19 tracking data)

Before running this, make sure the file exists:
1. Create 'data' folder in your project
2. Download or place the CSV file there
"""

# Read CSV and fill missing values
df = pd.read_csv("./data/all-states-history.csv").fillna(value=0)

"""
WHAT THIS DOES:

pd.read_csv("./data/all-states-history.csv")
    └─ Reads the CSV file
    └─ Converts it to a DataFrame (table structure)
    └─ Example structure:
        date       state  hospitalized  hospitalizedCumulative
        2020-07-01  AL     2803.0        2803.0
        2020-07-02  AL     2835.0        2835.0
        ...

.fillna(value=0)
    └─ Replaces missing values (NaN) with 0
    └─ Why? AI prefers clean data without gaps
    └─ Prevents errors during analysis

Result: DataFrame with 20,780 rows and multiple columns
"""

# Optional: Explore the data
print("Dataset shape (rows, columns):", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())


# ============================================================================
# STEP 4: CREATE THE PANDAS DATAFRAME AGENT
# ============================================================================
"""
THIS IS THE MAGIC STEP!

Here we create a special AI agent that:
1. Understands Pandas DataFrames
2. Can write Python code
3. Can execute code on your data
4. Can reason about the results
5. Can verify answers

This is MUCH more powerful than simple text processing!
"""

agent = create_pandas_dataframe_agent(
    # The AI model to use
    llm=model,
    # The DataFrame to analyze
    df=df,
    # Show all thinking steps (helpful for learning)
    verbose=True,
)

"""
WHAT JUST HAPPENED:

We created an 'agent' - an AI that can:

1. Receive questions in natural language
2. Understand what data operations are needed
3. Write Pandas/Python code automatically
4. Execute the code safely
5. Get results and reason about them
6. Provide detailed responses

This is unlike Lesson 1:
- Lesson 1: Question → AI → Direct Answer
- Lesson 2: Question → AI → Write Code → Run Code → Analyze → Answer

The agent is now ready to answer data questions!
"""


# ============================================================================
# STEP 5: TEST WITH A SIMPLE QUESTION
# ============================================================================
"""
Let's start simple: ask how many rows are in the data.
"""

print("\n" + "="*70)
print("SIMPLE EXAMPLE: Counting rows")
print("="*70)

response = agent.invoke("how many rows are there?")

# Extract the answer
print("\nQuestion: how many rows are there?")
print("Answer:", response['output'])

"""
WHAT HAPPENS INTERNALLY (when verbose=True):

1. Agent reads: "how many rows are there?"
2. Agent thinks: "I need to use df.shape[0]"
3. Agent writes: Python code
4. Agent executes: Runs df.shape[0]
5. Agent observes: 20780
6. Agent answers: "The dataframe has 20,780 rows."

The verbose output shows this entire process!
"""


# ============================================================================
# STEP 6: COMPLEX QUERY WITH VERIFICATION
# ============================================================================
"""
Now for the powerful part!

We'll ask a complex data question with instructions for:
1. Understanding the data
2. Trying multiple methods
3. Verifying the answer
4. Explaining the result

This is where AI reasoning shines!
"""

# Build the prompt with PREFIX, QUESTION, SUFFIX
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

QUESTION = """How many patients were hospitalized during July 2020 in Alabama?"""

# Combine all parts
full_prompt = CSV_PROMPT_PREFIX + QUESTION + CSV_PROMPT_SUFFIX

print("\n" + "="*70)
print("COMPLEX EXAMPLE: Data Analysis with Verification")
print("="*70)
print("\nQuestion:", QUESTION)
print("\nAgent processing (verbose output below):\n")

# Send to agent
result = agent.invoke(full_prompt)

# Display the result
print("\n" + "="*70)
print("FINAL RESPONSE:")
print("="*70)
display(Markdown(result['output']))


# ============================================================================
# STEP 7: UNDERSTANDING THE VERBOSE OUTPUT
# ============================================================================
"""
When verbose=True, you see the agent's reasoning process:

Example output:
> Entering new AgentExecutor chain...
Thought: I need to understand the data structure
Action: python_repl_ast
Action Input: pd.set_option('display.max_columns', None); df.columns
Observation: ['date', 'state', 'hospitalized', ...]
Thought: Now I understand the columns. Let me filter for July 2020 and Alabama
Action: python_repl_ast
Action Input: df['date'] = pd.to_datetime(df['date']); july_al = df[(df['state'] == 'AL') & (df['date'] >= '2020-07-01') & (df['date'] <= '2020-07-31')]; july_al['hospitalized'].sum()
Observation: 206707.0
Thought: Good! Now let me verify with another method
Action: python_repl_ast
Action Input: july_al['hospitalizedCumulative'].iloc[-1] - july_al['hospitalizedCumulative'].iloc[0]
Observation: -7718.0
Thought: Methods don't match. Let me investigate...
... (continues until consistent)
Final Answer: 206,707.0 patients were hospitalized...

Key terms:
- Thought: What the AI is thinking
- Action: What tool/code to use
- Action Input: The actual code
- Observation: The result of running the code
- Final Answer: The conclusion
"""


# ============================================================================
# STEP 8: BUILDING A REUSABLE FUNCTION
# ============================================================================
"""
Instead of repeating the same prompt structure,
create a reusable function for data analysis questions.
"""

def ask_data_question(agent, question, show_steps=True):
    """
    Ask a data analysis question using the AI agent.
    
    Args:
        agent: The Pandas dataframe agent
        question: The question to ask (in natural language)
        show_steps: Whether to show the agent's reasoning
    
    Returns:
        str: The AI's detailed response with explanation
    
    Example:
        >>> response = ask_data_question(agent, "What state has the most cases?")
        >>> print(response)
    """
    
    # Build the prompt
    prefix = "First, examine the data structure. Then answer the question:"
    
    suffix = """
    - Verify your answer using at least two different methods
    - Compare the results to ensure consistency
    - Only provide answers based on your calculations
    - Include an explanation section with column names used
    """
    
    full_prompt = prefix + question + suffix
    
    # Set verbose if showing steps
    # Note: This would require recreating the agent with verbose setting
    
    # Get the response
    result = agent.invoke(full_prompt)
    
    return result['output']


# Test the function
print("\n" + "="*70)
print("USING THE REUSABLE FUNCTION:")
print("="*70)

answer = ask_data_question(
    agent,
    "How many total hospitalizations were reported across all states in July 2020?"
)
display(Markdown(answer))


# ============================================================================
# STEP 9: MULTIPLE QUESTIONS FOR DEEPER ANALYSIS
# ============================================================================
"""
You can ask follow-up questions to dig deeper into the data.
The agent learns from context and can build on previous answers.
"""

follow_up_questions = [
    "Which state had the highest number of hospitalizations in July 2020?",
    "What was the trend - did hospitalizations increase or decrease during July?",
    "Compare Texas and California's hospitalization rates during July 2020",
]

print("\n" + "="*70)
print("FOLLOW-UP QUESTIONS:")
print("="*70)

for i, question in enumerate(follow_up_questions, 1):
    print(f"\n--- Question {i} ---")
    print(f"Q: {question}")
    print("(Processing...)\n")
    
    response = agent.invoke(question)
    print(f"A: {response['output'][:200]}...\n")  # Show first 200 chars


# ============================================================================
# STEP 10: ADVANCED TECHNIQUES
# ============================================================================
"""
You can ask the agent to perform more advanced analyses.
"""

advanced_questions = {
    "Summary": "Give me a statistical summary of hospitalization numbers",
    "Anomalies": "Identify dates with unusual spikes in hospitalizations",
    "Trends": "What's the month-by-month trend for the entire dataset?",
    "Data Quality": "Check for any missing values or data inconsistencies",
}

print("\n" + "="*70)
print("ADVANCED ANALYSES:")
print("="*70)

for analysis_type, question in advanced_questions.items():
    print(f"\n{analysis_type}:")
    response = agent.invoke(question)
    # Display response (truncated for clarity)
    print(response['output'][:300] + "...\n")


# ============================================================================
# STEP 11: EXPORTING RESULTS
# ============================================================================
"""
Save analysis results for later use.
"""

def save_analysis(question, response, filename="analysis_result.md"):
    """
    Save analysis results to a file.
    
    Args:
        question (str): The question asked
        response (str): The AI's response
        filename (str): Where to save
    """
    
    with open(filename, 'w') as f:
        f.write(f"# Data Analysis Result\n\n")
        f.write(f"## Question\n{question}\n\n")
        f.write(f"## Answer\n{response}\n")
    
    print(f"✅ Analysis saved to {filename}")


# Save an example analysis
print("\n" + "="*70)
print("SAVING RESULTS:")
print("="*70)

save_analysis(
    QUESTION,
    result['output'],
    "alabama_july_2020_analysis.md"
)


# ============================================================================
# KEY CONCEPTS & TAKEAWAYS
# ============================================================================
"""
WHAT YOU LEARNED IN LESSON 2:

1. CSV FILES & PANDAS
   - CSV files store data in table format
   - Pandas converts CSVs to DataFrames (in-memory tables)
   - DataFrames can be filtered, grouped, and analyzed

2. AI DATA AGENTS
   - Specialized agents for working with data
   - Can write and execute Python code
   - Can reason about results

3. PROMPT STRUCTURE
   - PREFIX: Setup and context
   - QUESTION: What you want to know
   - SUFFIX: Quality control instructions

4. VERIFICATION
   - Always try multiple methods
   - Compare results
   - Investigate discrepancies

5. NATURAL LANGUAGE TO CODE
   - Ask in English
   - AI writes Python
   - AI executes and explains

WHY THIS MATTERS:

Before AI data agents:
- Required SQL expertise
- Required Python/Pandas knowledge
- Manual verification needed
- Slow analysis process

With AI data agents:
- Ask in natural language
- No coding required
- Automatic verification
- Fast analysis

NEXT STEPS:

1. Try with your own CSV file
2. Ask progressively more complex questions
3. Explore the agent's reasoning (verbose=True)
4. Build a library of useful prompts
5. Integrate into automated pipelines
"""


# ============================================================================
# BONUS: TROUBLESHOOTING GUIDE
# ============================================================================
"""
Common Issues & Solutions:

Issue 1: "FileNotFoundError: ./data/all-states-history.csv"
Solution: 
    - Create a 'data' folder in your project
    - Download the CSV file to that folder
    - Or adjust the path: df = pd.read_csv("path/to/your/file.csv")

Issue 2: "Column not found" error
Solution:
    - Check column names: print(df.columns)
    - Use exact column names in your questions
    - Mention column names in PREFIX

Issue 3: Date filtering not working
Solution:
    - Convert to datetime: df['date'] = pd.to_datetime(df['date'])
    - Ask agent to do this in the PREFIX

Issue 4: Agent gives wrong answer
Solution:
    - Use the SUFFIX strategy: ask for multiple verification methods
    - The agent will automatically investigate inconsistencies
    - Ask follow-up questions

Issue 5: Too much output
Solution:
    - Set verbose=False when creating agent
    - agent = create_pandas_dataframe_agent(llm=model, df=df, verbose=False)

Issue 6: Slow response
Solution:
    - Filter data before creating agent
    - Ask specific questions (not "analyze everything")
    - Use smaller datasets for testing
"""


print("\n" + "="*70)
print("✅ Lesson 2 Complete!")
print("="*70)
print("""
You've learned how to:
1. Load CSV data with Pandas
2. Create AI data agents
3. Ask complex data questions
4. Verify results automatically
5. Get thorough, explained answers

Next: Try with your own data!
""")
