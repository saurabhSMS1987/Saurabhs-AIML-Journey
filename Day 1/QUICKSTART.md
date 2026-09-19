# ⚡ Quick Start Guide

Get up and running in 5 minutes!

---

## 📋 Prerequisites Check

Before starting, make sure you have:

- [ ] Python 3.8 or higher installed (`python --version`)
- [ ] Azure account with OpenAI enabled
- [ ] Azure OpenAI endpoint URL
- [ ] Azure OpenAI API key
- [ ] Git installed (for cloning)
- [ ] Text editor (VS Code, PyCharm, etc.)

---

## 🚀 5-Minute Setup

### Step 1: Clone & Enter Directory (1 min)
```bash
git clone https://github.com/yourusername/first-ai-agent.git
cd first-ai-agent
```

### Step 2: Create Virtual Environment (1 min)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 4: Add Your Credentials (1 min)
```bash
# Create .env file
# Windows (PowerShell):
echo "AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/" > .env
echo "AZURE_OPENAI_API_KEY=your-api-key-here" >> .env

# macOS/Linux:
cat > .env << EOF
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
EOF
```

### Step 5: Run the Code (1 min)
```bash
# Option A: Run as Python script
python first_ai_agent.py

# Option B: Run in Jupyter
jupyter notebook
# Then open and run: L1_Your_First_AI_Agent.ipynb
```

---

## ✅ Success Indicators

You'll see output like:
```
============================================================
AI RESPONSE:
============================================================
**French:** J'aime les voitures rouges et les maisons bleues, 
           mais mon chien est jaune.

**Spanish:** Me gustan los coches rojos y las casas azules, 
            pero mi perro es amarillo.
============================================================
```

---

## 📂 File Structure After Setup

```
first-ai-agent/
├── venv/                                    # Virtual environment
├── .env                                     # Your credentials (not in Git!)
├── .gitignore                               # Git ignore rules
├── README.md                                # Main documentation
├── requirements.txt                         # Dependencies
├── first_ai_agent.py                        # Main Python script
├── L1_Your_First_AI_Agent.ipynb            # Jupyter notebook
└── First_AI_Agent_Complete_Guide.md        # Detailed explanations
```

---

## 🎯 What to Do Next

### Immediate (After running once):
1. ✅ Modify the sentence in the code
2. ✅ Try different languages
3. ✅ Observe how AI responds

### Short-term (Next 30 mins):
1. Read the code line-by-line
2. Understand what each part does
3. Check out [First_AI_Agent_Complete_Guide.md](./First_AI_Agent_Complete_Guide.md)

### Next Steps (Later today):
1. Build the reusable function
2. Try Challenge 1-4 in README.md
3. Modify the code yourself

### Future Learning:
1. Multi-turn conversations
2. Different AI models
3. Production deployment

---

## 🐛 Quick Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `KeyError: AZURE_OPENAI_ENDPOINT` | Create `.env` file with credentials |
| `AuthenticationError` | Check your API key and endpoint URL |
| `Connection timeout` | Check internet connection |

For more help, see [README.md - Troubleshooting](./README.md#-troubleshooting)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](./README.md) | Complete guide & reference |
| [First_AI_Agent_Complete_Guide.md](./First_AI_Agent_Complete_Guide.md) | Detailed code breakdown |
| [first_ai_agent.py](./first_ai_agent.py) | Commented Python script |
| [requirements.txt](./requirements.txt) | Python dependencies |
| [.gitignore](./.gitignore) | Git configuration |

---

## 💡 Quick Reference

### The Complete Code
```python
import os
from langchain.schema import HumanMessage
from langchain_openai import AzureChatOpenAI

# Connect to AI
model = AzureChatOpenAI(
    openai_api_version="2024-04-01-preview",
    azure_deployment="gpt-4-1106",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# Create message
message = HumanMessage(
    content="Translate to French and Spanish: "
    "I like red cars and blue houses, but my dog is yellow."
)

# Get response
response = model.invoke([message])
print(response.content)
```

### Environment Setup (One-liner)
```bash
python -m venv venv && (source venv/bin/activate || venv\Scripts\activate) && pip install -r requirements.txt
```

---

## 🎓 Key Concepts (30-second version)

1. **LangChain** = Framework for AI interactions
2. **Azure OpenAI** = GPT-4 in the cloud
3. **HumanMessage** = Your question formatted for AI
4. **model.invoke()** = Send message and get response
5. **Environment Variables** = Secure way to store API keys

---

## ❓ Common Questions

**Q: Why do I need a virtual environment?**  
A: To avoid conflicts with other Python projects on your computer.

**Q: Why use `.env` file?**  
A: To keep your API keys secret and not commit them to GitHub.

**Q: Can I use a different AI model?**  
A: Yes! LangChain supports OpenAI, Anthropic, Hugging Face, and more.

**Q: How much will this cost?**  
A: Depends on your Azure plan. Free tier includes credits. Check Azure pricing.

**Q: Is this suitable for production?**  
A: This is a learning project. For production, add error handling, logging, and security.

---

## 🔗 Useful Links

- [Azure OpenAI Setup](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource)
- [LangChain Docs](https://python.langchain.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Git & GitHub Basics](https://github.github.io/training-kit/downloads/github-git-cheat-sheet.pdf)

---

## 🚀 You're All Set!

You now have:
- ✅ A working AI agent
- ✅ Complete code documentation
- ✅ Learning resources
- ✅ A foundation to build on

**Next:** Run the code, see it work, then modify it to explore!

---

## 📞 Still Stuck?

1. **Check [README.md](./README.md)** for comprehensive guide
2. **Read [First_AI_Agent_Complete_Guide.md](./First_AI_Agent_Complete_Guide.md)** for detailed explanations
3. **Review [first_ai_agent.py](./first_ai_agent.py)** for commented code
4. **Check Azure docs** for credential issues

---

**Happy coding! 🎉**

```
   ╔════════════════════════════╗
   ║  Welcome to AI Development ║
   ║   Let's Build Something!   ║
   ╚════════════════════════════╝
```
