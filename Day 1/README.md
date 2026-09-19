# 🚀 Your First AI Agent

**Build your first AI application with LangChain and Azure OpenAI**

A beginner-friendly guide to connecting to GPT-4, sending prompts, and getting intelligent responses. This is the perfect starting point for anyone wanting to learn AI development.

---

## 📚 What You'll Learn

This project teaches you:

- ✅ How to connect to Azure OpenAI's GPT-4 model
- ✅ How to format messages for AI using LangChain
- ✅ How to send requests and parse responses
- ✅ Security best practices (environment variables, API keys)
- ✅ The fundamentals of AI development

**Time to complete:** 15-30 minutes  
**Difficulty:** Beginner  
**Prerequisites:** Basic Python knowledge

---

## 🎯 What Does This Do?

This script demonstrates AI in action by translating a sentence:

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

## 🛠 Installation

### Prerequisites
- Python 3.8 or higher
- An Azure account with OpenAI access
- Your Azure OpenAI endpoint and API key

### Step 1: Clone This Repository

```bash
git clone https://github.com/yourusername/first-ai-agent.git
cd first-ai-agent
```

### Step 2: Create Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Credentials

Create a `.env` file in the project root:

```bash
# .env file
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
```

> ⚠️ **Security:** Add `.env` to your `.gitignore` file to prevent accidentally sharing your API key!

### Step 5: Run the Code

```bash
# Run as Python script
python first_ai_agent.py

# Or open Jupyter notebook
jupyter notebook
# Then open L1_Your_First_AI_Agent.ipynb
```

---

## 📁 Project Structure

```
first-ai-agent/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── .env                                   # Your credentials (NOT in Git!)
├── .gitignore                             # Git ignore rules
├── first_ai_agent.py                      # Main Python script
├── L1_Your_First_AI_Agent.ipynb           # Jupyter notebook
├── First_AI_Agent_Complete_Guide.md       # Detailed guide with explanations
└── docs/
    ├── CODE_BREAKDOWN.md                  # Step-by-step code explanation
    └── TROUBLESHOOTING.md                 # Common issues and fixes
```

---

## 💻 Code Breakdown

### The 4 Main Steps

```python
# 1. Import Libraries
import os
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

# 2. Connect to AI Model
model = AzureChatOpenAI(
    openai_api_version="2024-04-01-preview",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# 3. Create Your Message
message = HumanMessage(
    content="Translate this sentence from English to French and Spanish. "
    "I like red cars and blue houses, but my dog is yellow."
)

# 4. Send to AI and Get Response
response = model.invoke([message])
print(response.content)
```

### Flow Diagram

```
┌─────────────────────┐
│  Your Question      │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  LangChain (Formats message)        │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  Azure OpenAI Endpoint (Cloud)      │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  GPT-4 Model (Processing)           │
└──────────┬──────────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│  Response (French & Spanish)        │
└─────────────────────────────────────┘
```

---

## 📖 Documentation

For detailed explanations, see:

- **[First_AI_Agent_Complete_Guide.md](./First_AI_Agent_Complete_Guide.md)** 
  - Complete breakdown of every line of code
  - Concepts explained in simple terms
  - Visual diagrams and examples

- **[first_ai_agent.py](./first_ai_agent.py)**
  - Fully commented Python script
  - Bonus reusable functions
  - Learning progression guide

---

## 🎓 Learning Resources

| Resource | Link |
|----------|------|
| LangChain Docs | https://python.langchain.com/ |
| Azure OpenAI | https://learn.microsoft.com/en-us/azure/ai-services/openai/ |
| OpenAI API | https://platform.openai.com/docs/ |
| Python Basics | https://python.org/ |
| Jupyter Notebook | https://jupyter.org/ |

---

## 🚀 Next Steps & Challenges

### Challenge 1: Translate Different Content
Modify the message to translate different sentences:

```python
message = HumanMessage(
    content="Translate to French and Spanish: Hello, my name is Saurabh!"
)
response = model.invoke([message])
print(response.content)
```

### Challenge 2: Build a Reusable Function
```python
def translate_text(text, languages):
    prompt = f"Translate to {', '.join(languages)}: {text}"
    message = HumanMessage(content=prompt)
    return model.invoke([message]).content

# Use it
result = translate_text("I love AI!", ["French", "Spanish", "German"])
print(result)
```

### Challenge 3: Create a Multi-Turn Conversation
```python
from langchain.schema import SystemMessage

messages = [
    SystemMessage(content="You are a helpful AI assistant."),
    HumanMessage(content="What is Python?"),
]
response = model.invoke(messages)
print(response.content)

# Continue the conversation
messages.append(HumanMessage(content="Tell me more about data science"))
response = model.invoke(messages)
print(response.content)
```

### Challenge 4: Build a Simple Chatbot
See `challenges/chatbot.py` for a complete example.

---

## ⚙️ Configuration

### Environment Variables

Your `.env` file should contain:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here

# Optional: For debugging
DEBUG=True
LOG_LEVEL=INFO
```

### requirements.txt

```txt
langchain==0.1.0
langchain-openai==0.0.5
python-dotenv==1.0.0
pandas==2.0.0
jupyter==1.0.0
openai==1.3.0
```

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'langchain'`

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Problem: `KeyError: 'AZURE_OPENAI_ENDPOINT'`

**Solution:** Create `.env` file with your credentials
```bash
# Create .env in project root
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
```

### Problem: `AuthenticationError: Invalid credentials`

**Solution:** Verify your Azure API key and endpoint URL

### Problem: `Connection timeout`

**Solution:** Check internet connection and Azure service status

For more troubleshooting help, see [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

---

## 📊 Key Concepts

### LangChain
A framework that simplifies working with AI models. It provides:
- Message formatting (HumanMessage, AIMessage)
- Model connections (Azure, OpenAI, etc.)
- Chain building (for complex AI workflows)

### Azure OpenAI
Microsoft's hosted version of OpenAI's GPT models:
- Cloud-based (no local hardware needed)
- Requires credentials (API key + endpoint)
- Scales automatically

### HumanMessage & AIMessage
```python
# You send this:
HumanMessage(content="Your question here")

# AI responds with this:
AIMessage(content="The answer")
```

### Environment Variables
Secure way to store sensitive info:
```python
# Safe (using environment variable)
api_key = os.getenv("AZURE_OPENAI_API_KEY")

# UNSAFE (never do this!)
api_key = "sk-1234567890abcdef"  # Don't commit this!
```

---

## 🔒 Security Best Practices

1. ✅ **Never hardcode API keys** - Use environment variables
2. ✅ **Add `.env` to `.gitignore`** - Prevent accidental commits
3. ✅ **Use `.env` files** - Keep secrets local only
4. ✅ **Rotate API keys** - Change them periodically
5. ✅ **Limit permissions** - Give your API key only needed access

---

## 📈 Learning Path

### Level 1: Foundations (Current)
- ✅ Connect to AI model
- ✅ Send single message
- ✅ Parse response

### Level 2: Conversations
- ⬜ Multi-turn conversations
- ⬜ System messages
- ⬜ Message history

### Level 3: Advanced Features
- ⬜ Error handling
- ⬜ Logging
- ⬜ Response parsing

### Level 4: Production
- ⬜ Web API (Flask/FastAPI)
- ⬜ Database integration
- ⬜ Deployment

---

## 💬 Examples

### Example 1: Basic Translation
```python
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(...)
message = HumanMessage(content="Translate 'Hello World' to Spanish")
response = model.invoke([message])
print(response.content)
```

### Example 2: Reusable Function
```python
def ask_ai(question):
    message = HumanMessage(content=question)
    response = model.invoke([message])
    return response.content

result = ask_ai("What is machine learning?")
print(result)
```

### Example 3: Multi-Message Conversation
```python
from langchain.schema import SystemMessage

messages = [
    SystemMessage(content="You are an expert programmer."),
    HumanMessage(content="Explain Python to a beginner"),
]
response = model.invoke(messages)
print(response.content)
```

---

## 🤝 Contributing

Found a bug or have a suggestion? Open an issue or submit a pull request!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Saurabh Shirgaokar**

- 📧 Email: shirgaokar.saurabh@gmail.com
- 📞 Phone: +1 857-919-5640
- 🔗 LinkedIn: [Connect](https://linkedin.com/in/saurabh-shirgaokar)
- 📍 Location: Schaumburg, IL

**About:** Data Specialist with 4+ years of experience building AI, ML, and data solutions using Python, SQL, PySpark, and Databricks.

---

## 🎯 Goals

This project aims to:
- 📚 Teach AI development fundamentals
- 🚀 Show practical AI application
- 💡 Inspire further learning
- 🤝 Build community interest in AI

---

## 📞 Support

Need help? Check these resources:

- 📖 **Read the docs** → [First_AI_Agent_Complete_Guide.md](./First_AI_Agent_Complete_Guide.md)
- 🐛 **Troubleshooting** → [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)
- 💬 **Open an issue** → [GitHub Issues](https://github.com/yourusername/first-ai-agent/issues)

---

## ⭐ If This Helped You

If you found this helpful:
- ⭐ Star this repository
- 🔗 Share with friends
- 📢 Spread the word about AI learning

---

**Happy coding! 🚀**

```
     ╔═════════════════════╗
     ║  Your First AI Agent ║
     ║     Let's Go! 🚀     ║
     ╚═════════════════════╝
```

---

## Quick Reference

```python
# Install
pip install -r requirements.txt

# Create .env with credentials
echo "AZURE_OPENAI_ENDPOINT=your-endpoint" > .env
echo "AZURE_OPENAI_API_KEY=your-key" >> .env

# Run
python first_ai_agent.py

# Or use Jupyter
jupyter notebook
```

---

**Last Updated:** 2026  
**Status:** ✅ Complete & Tested
