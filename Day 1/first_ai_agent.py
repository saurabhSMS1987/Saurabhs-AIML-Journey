"""
Your First AI Agent
====================

This script demonstrates how to build your first AI application using:
- LangChain: A framework for working with AI models
- Azure OpenAI: Microsoft's hosted GPT-4 model
- HumanMessage: The format AI understands for user inputs

Author: Saurabh Shirgaokar
Date: 2026
Level: Beginner

What This Does:
- Connects to Azure OpenAI's GPT-4 model
- Takes a sentence and translates it to French and Spanish
- Returns the translated text

Prerequisites:
- Python 3.8+
- Azure OpenAI account and API key
- Required libraries (see requirements.txt)
"""

# ============================================================================
# STEP 1: SETUP & IMPORT LIBRARIES
# ============================================================================
"""
Import all the tools we need for this project.
Think of this as gathering your toolkit before starting work.
"""

import os  # For accessing environment variables (like API keys)
import pandas as pd  # For data manipulation (not used here but good to have)
from IPython.display import Markdown, HTML, display  # For formatted output in Jupyter


# ============================================================================
# STEP 2: CONNECT TO AZURE OPENAI
# ============================================================================
"""
Connect to the Azure OpenAI service.

This is where the magic happens - we're establishing a connection to 
Microsoft's cloud servers where GPT-4 lives.
"""

from langchain.schema import HumanMessage  # Import message format for our questions
from langchain_openai import AzureChatOpenAI  # Import the AI model connection


# Create the model connection
model = AzureChatOpenAI(
    # The API version - this tells Azure which version of the API to use
    # Different versions may have different features and behaviors
    openai_api_version="2024-04-01-preview",
    
    # The deployment name - this specifies which AI model to use
    # "gpt-4-1106" refers to GPT-4 with 1106K tokens of capacity
    azure_deployment="gpt-4-1106",
    
    # The endpoint - this is the cloud server where your AI model lives
    # We retrieve it safely from the environment (see your .env file)
    # Using os.getenv() keeps your sensitive info secure
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

"""
EXPLANATION OF THE CONNECTION:
Your Code → LangChain (middleware) → Azure Endpoint → GPT-4 Model → Response back

Why use LangChain?
- Simplifies working with AI models
- Handles message formatting automatically
- Supports multiple AI providers (OpenAI, Anthropic, Hugging Face, etc.)
- Makes switching between models easier
"""


# ============================================================================
# STEP 3: PREPARE YOUR PROMPT (THE QUESTION TO ASK)
# ============================================================================
"""
Create a message in the format the AI understands.

A HumanMessage tells the AI that this is input FROM a human (you).
We could also use AIMessage (for AI responses) or SystemMessage (for instructions).
"""

message = HumanMessage(
    # The 'content' parameter holds your actual question/instruction
    # Python combines these string lines into one continuous string
    content="Translate this sentence from English "
    "to French and Spanish. I like red cars and "
    "blue houses, but my dog is yellow."
)

"""
WHAT THIS CREATES:
╔════════════════════════════════════════════╗
│        HumanMessage Object                 │
├════════════════════════════════════════════┤
│ Type: 'human'                              │
│ Content: "Translate this sentence..."      │
╚════════════════════════════════════════════╝

The AI knows this is a question from a human and responds appropriately.
"""


# ============================================================================
# STEP 4: SEND THE MESSAGE AND GET THE RESPONSE
# ============================================================================
"""
Send your message to the AI model and receive the response.

model.invoke() means: "Execute this message on the model and return the result"

The [message] part puts our message in a list because:
- The model can handle multiple messages (for conversations)
- Even for a single message, it expects a list structure
- Example: [message1, message2, message3] for a multi-turn conversation
"""

# Send the message and store the response
response = model.invoke([message])

# The response is an AIMessage object, so we extract the content (text)
print("=" * 60)
print("AI RESPONSE:")
print("=" * 60)
print(response.content)
print("=" * 60)

"""
WHAT HAPPENS INTERNALLY:
1. Your message travels to Azure's servers via HTTPS
2. It arrives at the Azure OpenAI endpoint
3. GPT-4 processes your request
4. The AI generates a response (French and Spanish translations)
5. The response travels back to your computer
6. You receive an AIMessage object with the answer

EXPECTED OUTPUT:
**French:** J'aime les voitures rouges et les maisons bleues, mais mon chien est jaune.
**Spanish:** Me gustan los coches rojos y las casas azules, pero mi perro es amarillo.
"""


# ============================================================================
# OPTIONAL: BONUS - EXTRACT AND DISPLAY RESULTS NICELY
# ============================================================================
"""
Here are some ways to work with the response:
"""

# Get just the text (not the object wrapper)
just_text = response.content
print(f"\nJust the text:\n{just_text}")

# Extract by message type
message_type = response.type  # Should be "ai"
print(f"\nMessage type: {message_type}")

# Display in a formatted way (if using Jupyter)
display(Markdown(f"### AI Translation\n{response.content}"))


# ============================================================================
# EXAMPLE: BUILD A REUSABLE FUNCTION
# ============================================================================
"""
Instead of writing the same code repeatedly, wrap it in a function.
This is good software engineering practice.
"""

def translate_to_multiple_languages(text_to_translate, target_languages):
    """
    Translates a sentence to multiple languages using AI.
    
    Args:
        text_to_translate (str): The sentence you want translated
        target_languages (list): List of languages, e.g., ['French', 'German', 'Japanese']
    
    Returns:
        str: The AI's response with all translations
    
    Example:
        >>> result = translate_to_multiple_languages(
        ...     "Hello, how are you?",
        ...     ['French', 'Spanish', 'German']
        ... )
        >>> print(result)
    """
    
    # Create the prompt dynamically
    languages_string = " and ".join(target_languages)
    prompt = f"Translate this to {languages_string}: {text_to_translate}"
    
    # Create the HumanMessage
    user_message = HumanMessage(content=prompt)
    
    # Send to model and get response
    ai_response = model.invoke([user_message])
    
    # Return just the text content
    return ai_response.content


# Test the function with different languages
if __name__ == "__main__":
    # Example 1: Basic usage
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Translate to Multiple Languages")
    print("=" * 60)
    
    result = translate_to_multiple_languages(
        "I love coding with Python",
        ["French", "Spanish", "German"]
    )
    print(result)
    
    
    # Example 2: More languages
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Many Languages")
    print("=" * 60)
    
    result = translate_to_multiple_languages(
        "Data science is amazing",
        ["French", "Spanish", "German", "Italian", "Portuguese"]
    )
    print(result)


# ============================================================================
# KEY CONCEPTS SUMMARY
# ============================================================================
"""
1. LANGCHAIN
   - Framework that simplifies AI model interactions
   - Handles message formatting and model connections
   - Supports multiple AI providers

2. AZURE OPENAI
   - Microsoft's hosted version of OpenAI's models
   - Requires cloud credentials
   - Scales automatically with demand

3. HUMANMESSAGE vs AIMESSAGE
   HumanMessage: Questions/inputs FROM the user
   AIMessage: Responses FROM the AI
   This distinction helps the AI understand conversation flow

4. API ENDPOINTS
   - The URL where your model lives in the cloud
   - Example: https://your-resource.openai.azure.com/
   - Like sending a letter to a specific address

5. ENVIRONMENT VARIABLES
   - Secure way to store API keys
   - Kept in .env file, accessed via os.getenv()
   - Prevents accidentally sharing secrets on GitHub

6. MODEL.INVOKE()
   - Sends your message to the AI
   - [message] format allows multiple messages
   - Returns an AIMessage object with the response
"""


# ============================================================================
# LEARNING PROGRESSION
# ============================================================================
"""
Now that you understand this lesson, try these next steps:

LEVEL 1 - Modify Inputs
└─ Change the sentence and see how translations differ
└─ Try different languages
└─ Test with longer paragraphs

LEVEL 2 - Build Conversations
└─ Use SystemMessage to give AI personality
└─ Send multiple messages to create context
└─ Track conversation history

LEVEL 3 - Add Functionality
└─ Create a chatbot interface
└─ Add error handling and logging
└─ Save responses to a file

LEVEL 4 - Advanced Features
└─ Implement prompt engineering techniques
└─ Use embeddings for semantic search
└─ Build memory/knowledge systems

LEVEL 5 - Production Deployment
└─ Deploy as a web API (Flask/FastAPI)
└─ Add authentication and rate limiting
└─ Monitor costs and usage
└─ Implement caching for efficiency
"""


# ============================================================================
# TROUBLESHOOTING GUIDE
# ============================================================================
"""
If you get errors, check:

1. ModuleNotFoundError: 'langchain'
   FIX: pip install -r requirements.txt

2. KeyError: 'AZURE_OPENAI_ENDPOINT'
   FIX: Make sure .env file exists with your credentials

3. AuthenticationError
   FIX: Verify your Azure API key and endpoint URL

4. Connection timeout
   FIX: Check internet connection and Azure service status

5. Rate limit exceeded
   FIX: Wait a moment and try again or upgrade your plan
"""


# ============================================================================
# RESOURCES
# ============================================================================
"""
Helpful links for learning more:

📖 Official Documentation
   - LangChain: https://python.langchain.com/
   - Azure OpenAI: https://learn.microsoft.com/en-us/azure/ai-services/openai/
   - OpenAI API: https://platform.openai.com/docs/

🎓 Learning Resources
   - Python basics: https://python.org/
   - API concepts: https://restfulapi.net/
   - Cloud computing: https://azure.microsoft.com/

🛠 Tools
   - Jupyter Notebook: https://jupyter.org/
   - VS Code: https://code.visualstudio.com/
   - Git & GitHub: https://github.com/
"""

print("\n✅ Your First AI Agent is complete!")
print("📚 Next: Try modifying the prompt and experiment!")
print("🚀 Future: Build chatbots, content generators, and more!")
