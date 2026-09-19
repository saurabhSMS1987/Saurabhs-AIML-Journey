# Day 1 Summary: Lessons 1-5

**Author:** Saurabh Shirgaokar  
**Date:** Sep 19, 2026

---

## Lesson 1: Your First AI Agent

**Learned:** How to connect to Azure OpenAI and make basic API calls with text input/output.

```python
message = HumanMessage(content="Translate to French: Hello")
model = AzureChatOpenAI(...)
response = model.invoke([message])
```

---

## Lesson 2: Interacting with CSV Data

**Learned:** How to use LangChain's Pandas agent to analyze CSV data with natural language queries.

```python
df = pd.read_csv("data.csv").fillna(0)
agent = create_pandas_dataframe_agent(llm, df)
result = agent.invoke(question)
```

**Key:** AI can understand CSV structure and answer questions without writing code.

---

## Lesson 3: Connecting to SQL Database

**Learned:** How to scale beyond CSV by connecting to real databases. AI writes SQL queries based on natural language questions.

```python
db = SQLDatabase.from_uri("sqlite:///db.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(llm, toolkit)
result = agent.invoke(question)
```

**Key:** AI can handle billions of rows, safety features prevent data damage.

---

## Lesson 4: Function Calling

**Learned:** How native OpenAI function calling works. You define functions as JSON schemas, AI decides when to call them, you execute them.

```
Round 1: Send messages + tools to AI
         → AI suggests functions

Round 2: Execute functions, add results to messages
         → AI synthesizes final answer
```

**Key:** This is how agents work under the hood. You have full control and transparency.

---

## Lesson 5: Persistent AI Assistants

**Learned:** How to build stateful assistants that remember conversations. Each turn adds to message history, so AI has context from previous questions.

```python
class PersistentAssistant:
    self.messages = []  # Conversation history
    
# Turn 1: Q1 → Answer 1 (remembered)
# Turn 2: Q2 → AI considers Q1 → Answer 2
# Turn 3: Q3 → AI considers Q1, Q2 → Answer 3
```

**Key:** Persistence + context = intelligent multi-turn conversations.

---

## Overall Progression

```
Lesson 1: Text → AI → Text (Foundation)
Lesson 2: CSV Analysis (Use AI without code)
Lesson 3: SQL Queries (Production databases)
Lesson 4: Function Calling (Understand the mechanism)
Lesson 5: Persistent Assistants (Multi-turn conversations)
```

**Biggest Insight:** Understanding how function calling works (Lesson 4) makes you a better engineer. You can build anything without being limited by frameworks.
