# Your First AI Agent: Complete Code Guide 🚀

**Author:** Saurabh Shirgaokar  
**Date:** 2026  
**Level:** Beginner  
**Topic:** Building Your First AI Application with LangChain and Azure OpenAI

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation & Setup](#installation--setup)
4. [Code Breakdown](#code-breakdown)
5. [Visual Flow](#visual-flow)
6. [How to Run](#how-to-run)
7. [Key Concepts](#key-concepts)
8. [What You Learned](#what-you-learned)
9. [Next Steps](#next-steps)

---

## Overview

This project is your **first step into AI development**. You'll learn how to:
- ✅ Connect to Azure OpenAI's GPT-4 model
- ✅ Send questions to an AI service
- ✅ Receive intelligent responses
- ✅ Build the foundation for more complex AI applications

### What Does This Code Do?

This notebook demonstrates a simple translation task using AI. You ask the model to translate a sentence from English to French and Spanish, and it delivers perfectly formatted translations.

**Input:**
```
"Translate this sentence from English to French and Spanish. 
I like red cars and blue houses, but my dog is yellow."
```

**Output:**
```
French: J'aime les voitures rouges et les maisons bleues, mais mon chien est jaune.
Spanish: Me gustan los coches rojos y las casas azules, pero mi perro es amarillo.
```

---

## Prerequisites

Before you start, make sure you have:

- ✅ Python 3.8 or higher installed
- ✅ An Azure account with OpenAI access
- ✅ Your Azure OpenAI endpoint and API key
- ✅ Jupyter Notebook or JupyterLab installed
- ✅ Basic Python knowledge

---

## Installation & Setup

### Step 1: Install Required Libraries

Create a `requirements.txt` file with the following dependencies:

```txt
langchain==0.1.0
langchain-openai==0.0.5
pandas==2.0.0
jupyter==1.0.0
openai==1.3.0
```

Then install them:

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Azure OpenAI Credentials

You need to configure your Azure OpenAI endpoint securely. Add your credentials to a `.env` file:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
```

**Security Note:** Never commit your `.env` file to GitHub! Add it to `.gitignore`.

### Step 3: Load Environment Variables

In your Jupyter notebook, load your credentials:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # This loads your .env file
```

---

## Code Breakdown

Now let's go through **every line of code** and understand what it does.

### **Chunk 1: Setup & Import Libraries**

```python
import os 
import pandas as pd 
from IPython.display import Markdown, HTML, display
```

**Line by line:**

| Code | Purpose |
|------|---------|
| `import os` | Allows you to access environment variables (like your API key stored securely) |
| `import pandas as pd` | Imports the data manipulation library (not used in this lesson, but useful for future projects) |
| `from IPython.display import Markdown, HTML, display` | Lets you display formatted text and HTML in Jupyter notebooks for better readability |

**Why this matters:** You're loading the basic Python tools you'll need for this project. Think of it like gathering all your tools before starting a project.

**Example use:**
```python
# You could use these later to display results nicely
display(Markdown("# This is a heading"))
display(HTML("<p>This is HTML formatted text</p>"))
```

---

### **Chunk 2: Connect to Azure OpenAI**

```python
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    openai_api_version="2024-04-01-preview",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
```

**Breaking it down:**

#### Line 1: Import HumanMessage
```python
from langchain.schema import HumanMessage
```
- **What it does:** Imports a special message format that the AI understands
- **Why:** The AI expects messages in a specific format (HumanMessage for user inputs, AIMessage for responses)
- **Analogy:** It's like learning the language an AI speaks before you talk to it

#### Line 2: Import the AI Model Connection
```python
from langchain_openai import AzureChatOpenAI
```
- **What it does:** Imports the Azure OpenAI chat model handler
- **Why:** This is the bridge between your code and Azure's GPT-4 model running in the cloud
- **Note:** LangChain simplifies working with AI models

#### Lines 3-8: Create the Model Connection
```python
model = AzureChatOpenAI(
    openai_api_version="2024-04-01-preview",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
```

**Parameter Explanation:**

| Parameter | Example | Explanation |
|-----------|---------|-------------|
| `openai_api_version` | `"2024-04-01-preview"` | The version of Azure's API to use. Different versions may have different features |
| `azure_deployment` | `"gpt-4-1106"` | Which AI model to use. "gpt-4-1106" is the GPT-4 model with 1106K tokens |
| `azure_endpoint` | `https://your-resource.openai.azure.com/` | The cloud server location where your AI model lives (retrieved from your `.env` file) |

**How it works:**
```
Your Code
    ↓
LangChain (middleware)
    ↓
Azure Endpoint (cloud)
    ↓
GPT-4 Model (AI brain)
    ↓
Response back to you
```

**What `os.getenv()` does:**
```python
os.getenv("AZURE_OPENAI_ENDPOINT")
```
- Looks for the environment variable `AZURE_OPENAI_ENDPOINT` from your `.env` file
- Returns the value securely without hardcoding it in your code
- This keeps your sensitive API keys safe!

---

### **Chunk 3: Prepare Your Prompt (Message)**

```python
message = HumanMessage(
    content="Translate this sentence from English "
    "to French and Spanish. I like red cars and "
    "blue houses, but my dog is yellow."
)
```

**Breaking it down:**

#### Create a HumanMessage Object
```python
message = HumanMessage(
    content="..."
)
```

- **`message =`** → Store the message in a variable named `message`
- **`HumanMessage()`** → Create a message object in the format the AI expects
- **`content=`** → The parameter that holds your actual question/instruction

#### The Message Content
```python
content="Translate this sentence from English "
        "to French and Spanish. I like red cars and "
        "blue houses, but my dog is yellow."
```

**How Python combines these strings:**
- Python automatically concatenates strings written next to each other
- This is just for readability—it becomes one continuous string:

```
"Translate this sentence from English to French and Spanish. I like red cars and blue houses, but my dog is yellow."
```

**Why use HumanMessage?**

The AI understands different message types:
- `HumanMessage()` → A question or input from a human
- `AIMessage()` → A response from the AI
- `SystemMessage()` → Instructions for how the AI should behave

This structure allows the AI to distinguish between different types of inputs in longer conversations.

**Visual representation:**
```
┌─────────────────────────────────────────┐
│        HumanMessage Object              │
├─────────────────────────────────────────┤
│ Type: Human                             │
│ Content: "Translate this sentence..."   │
└─────────────────────────────────────────┘
```

---

### **Chunk 4: Send to Model & Receive Response**

```python
model.invoke([message])
```

**Breaking it down:**

#### `model.invoke()`
- **What it does:** Sends your message to the AI model and waits for a response
- **`invoke`** → Means "call upon" or "execute"
- **How it works:** Your message travels to Azure's servers, processes through GPT-4, and returns an answer

#### `[message]`
- **Why it's in brackets:** The model expects a **list of messages** (even if it's just one)
- **Why a list?** This allows the model to handle multi-turn conversations with multiple messages
- **Example:** `[message1, message2, message3]` for a conversation

**Complete flow:**
```python
model.invoke([message])
```

1. Take the `message` variable (contains your question)
2. Put it in a list: `[message]`
3. Send it to the AI model via `invoke()`
4. Wait for the response
5. Return the result

---

### **The Response You Get**

```
AIMessage(content="**French:** J'aime les voitures rouges et les maisons bleues, mais mon chien est jaune.  
**Spanish:** Me gustan los coches rojos y las casas azules, pero mi perro es amarillo.")
```

**What this shows:**

| Component | Meaning |
|-----------|---------|
| `AIMessage()` | The response is wrapped in an AI Message object |
| `content=` | The actual response text |
| The text inside | Your translations in French and Spanish |

**How to extract just the text:**
```python
response = model.invoke([message])
print(response.content)  # Prints just the text part
```

---

## Visual Flow

Here's how the entire process works:

### Step-by-Step Flow Diagram

```
╔════════════════════════════════════════════════╗
║  Step 1: Setup Libraries                       ║
║  Import: os, pandas, IPython.display           ║
╚════════════════════════════════════════════════╝
                      ↓
╔════════════════════════════════════════════════╗
║  Step 2: Connect to Azure OpenAI               ║
║  - Create AzureChatOpenAI connection           ║
║  - Set API version & deployment                ║
║  - Load endpoint from environment              ║
╚════════════════════════════════════════════════╝
                      ↓
╔════════════════════════════════════════════════╗
║  Step 3: Create Your Message                   ║
║  - Wrap question in HumanMessage format        ║
║  - Store in 'message' variable                 ║
╚════════════════════════════════════════════════╝
                      ↓
╔════════════════════════════════════════════════╗
║  Step 4: Send to Model                         ║
║  - Call model.invoke([message])                ║
║  - Message travels to Azure servers            ║
╚════════════════════════════════════════════════╝
                      ↓
╔════════════════════════════════════════════════╗
║  Step 5: AI Processing                         ║
║  - GPT-4 model processes your request          ║
║  - Generates intelligent response              ║
╚════════════════════════════════════════════════╝
                      ↓
╔════════════════════════════════════════════════╗
║  Step 6: Receive Response                      ║
║  - AIMessage with French translation           ║
║  - AIMessage with Spanish translation          ║
╚════════════════════════════════════════════════╝
```

### Network Diagram

```
Your Computer                    Cloud (Azure)
┌──────────────┐                ┌──────────────────┐
│ Python Code  │                │ Azure OpenAI     │
│   + Jupyter  │────(HTTPS)────→│ Endpoint         │
│              │                │                  │
│ LangChain    │                │ GPT-4 Model      │
│              │←───(JSON)──────│ (AI Brain)       │
└──────────────┘                └──────────────────┘
     LOCAL                            CLOUD
```

---

## How to Run

### Step 1: Prepare Your Environment

```bash
# Create a project folder
mkdir my-first-ai-agent
cd my-first-ai-agent

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create Your `.env` File

```bash
# Create .env file in your project root
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
```

### Step 3: Create `requirements.txt`

```txt
langchain==0.1.0
langchain-openai==0.0.5
pandas==2.0.0
jupyter==1.0.0
openai==1.3.0
python-dotenv==1.0.0
```

### Step 4: Run the Notebook

```bash
# Start Jupyter
jupyter notebook

# Open 'L1_Your_First_AI_Agent.ipynb' and run each cell
```

### Step 5: See the Results

Execute the code and you'll see:
```
AIMessage(content="**French:** J'aime les voitures rouges et les maisons bleues, mais mon chien est jaune.  
**Spanish:** Me gustan los coches rojos y las casas azules, pero mi perro es amarillo.")
```

---

## Key Concepts

### 1. **LangChain**
- A framework that simplifies working with AI models
- Provides tools like `HumanMessage`, `AIMessage`, and model connections
- Makes complex AI interactions manageable

### 2. **Azure OpenAI**
- Microsoft's hosted version of OpenAI's GPT models
- Runs in the cloud (so you don't need expensive local hardware)
- Requires API credentials to access

### 3. **GPT-4**
- The latest large language model
- Can understand and generate human-like text
- The "brain" doing the intelligent work

### 4. **HumanMessage vs AIMessage**
```python
# You send this:
HumanMessage(content="Translate to French")

# You receive this:
AIMessage(content="French translation here")
```

### 5. **API Endpoint**
- A URL that points to where your AI model lives in the cloud
- Example: `https://your-resource.openai.azure.com/`
- Like sending a letter to a specific address

### 6. **Environment Variables**
- Secure way to store sensitive information (API keys)
- Stored in `.env` file, accessed via `os.getenv()`
- Keeps secrets out of your code

---

## What You Learned

✅ **Fundamentals of AI Interaction**
- How to connect to an AI service
- How to format questions for AI
- How to parse AI responses

✅ **Working with APIs**
- What an API endpoint is
- How to authenticate with credentials
- How to make requests and receive responses

✅ **Code Structure**
- Import statements and dependency management
- Creating objects (like HumanMessage)
- Method calls (like invoke())

✅ **Security Best Practices**
- Storing API keys in environment variables
- Using `.env` files
- Not hardcoding sensitive information

✅ **Python Concepts**
- String concatenation
- Objects and classes
- Method invocation
- List structures

---

## Next Steps

Now that you've mastered your first AI agent, try these challenges:

### 🎯 Challenge 1: Modify the Message
```python
# Try translating a different sentence
message = HumanMessage(
    content="Translate to French and Spanish: "
    "Hello, my name is Saurabh!"
)
response = model.invoke([message])
print(response.content)
```

### 🎯 Challenge 2: Build a Conversation
```python
from langchain.schema import SystemMessage

# Create a conversation with system instructions
messages = [
    SystemMessage(content="You are a helpful assistant that speaks in rhymes."),
    HumanMessage(content="Tell me about Python programming")
]
response = model.invoke(messages)
print(response.content)
```

### 🎯 Challenge 3: Extract and Display Results
```python
# Parse and display the response nicely
response = model.invoke([message])
print("=" * 50)
print("TRANSLATION RESULTS")
print("=" * 50)
print(response.content)
print("=" * 50)
```

### 🎯 Challenge 4: Build a Function
```python
def translate_to_languages(text, languages):
    """
    Translates a sentence to multiple languages
    
    Args:
        text (str): The sentence to translate
        languages (list): List of languages (e.g., ['French', 'Spanish'])
    
    Returns:
        str: The AI's translation response
    """
    prompt = f"Translate this to {' and '.join(languages)}: {text}"
    message = HumanMessage(content=prompt)
    response = model.invoke([message])
    return response.content

# Use it
result = translate_to_languages("I love coding", ["French", "Spanish", "German"])
print(result)
```

### 📚 Recommended Learning Path

1. ✅ **Lesson 1** (Current): Your First AI Agent
2. ⬜ **Lesson 2**: Multi-turn Conversations
3. ⬜ **Lesson 3**: System Messages & Personalities
4. ⬜ **Lesson 4**: Building Chains with LangChain
5. ⬜ **Lesson 5**: Memory & Context Management
6. ⬜ **Lesson 6**: Integrating Tools & APIs
7. ⬜ **Lesson 7**: Production Deployment

---

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langchain'`
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: `KeyError: 'AZURE_OPENAI_ENDPOINT'`
**Solution:** Make sure your `.env` file is in the project root and `python-dotenv` is installed
```bash
pip install python-dotenv
```

### Issue: `AuthenticationError` or `API Key is incorrect`
**Solution:** Verify your Azure credentials in the `.env` file

### Issue: `Connection timeout`
**Solution:** Check your internet connection and Azure endpoint URL

---

## Resources

- 📖 [LangChain Documentation](https://python.langchain.com/)
- 📖 [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- 📖 [OpenAI API Guide](https://platform.openai.com/docs/)
- 📖 [Python Environment Variables](https://docs.python.org/3/library/os.html#os.getenv)

---

## Summary

You've successfully built your first AI agent! Here's what you accomplished:

```
Input:  "Translate this to French and Spanish..."
         ↓
     [AI Processing]
         ↓
Output: "French translation... Spanish translation..."
```

This simple example demonstrates the **core pattern of AI development**:
1. Connect to an AI service
2. Format your request properly
3. Send the request
4. Process the response

As you progress, you'll use these same fundamentals to build chatbots, content generators, data analyzers, and more!

---

## Author

**Saurabh Shirgaokar**  
Data Specialist | AI & ML Enthusiast  
📧 shirgaokar.saurabh@gmail.com  
🔗 LinkedIn: [Your LinkedIn Profile]

---

## License

This project is open source and available under the MIT License.

---

**Happy coding! 🚀**
