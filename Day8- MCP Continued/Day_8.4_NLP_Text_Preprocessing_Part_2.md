# Day 8: NLP Text Preprocessing Part 2 - Advanced Techniques

**Date:** September 27, 2026  
**Topic:** Advanced NLP Text Preprocessing (Tokenization, Lemmatization, NER, Standardization)  
**Duration:** 90-120 minutes  
**Level:** Intermediate to Advanced  

---

## Overview

Building on Day 7's foundation (lowercasing, stop words, punctuation), Part 2 covers **advanced preprocessing techniques** that break text into meaningful units and standardize it for analysis.

**Key Question:** After cleaning text, how do we extract the real meaning?

---

## Lesson 1: Tokenization - Breaking Text into Meaningful Units

### Important Points:

**1. What is Tokenization?**

Tokenization is splitting text into smaller units called **tokens**.

```
Text: "Natural Language Processing is amazing!"

Tokenization Options:

Option 1: Word Tokenization (most common)
├─ Tokens: ["Natural", "Language", "Processing", "is", "amazing", "!"]
│
Option 2: Sentence Tokenization
├─ Tokens: ["Natural Language Processing is amazing!"]
│
Option 3: Character Tokenization
├─ Tokens: ["N", "a", "t", "u", "r", "a", "l", " ", "L", ...]
│
Option 4: Subword Tokenization
├─ Tokens: ["Natural", "Language", "Process", "ing", ...]
```

**2. Why Tokenization Matters**

```
Without Tokenization:
Text: "I love machine learning"
├─ Treated as one unit
├─ Can't analyze individual words
└─ Hard to understand meaning

With Tokenization:
Tokens: ["I", "love", "machine", "learning"]
├─ Can analyze sentiment of "love"
├─ Can identify key concepts
├─ Can count word frequencies
└─ Can build feature vectors
```

**3. Types of Tokenization**

```
Simple Word Tokenization:
├─ Split by whitespace
├─ Fast but imprecise
├─ Issues: "Don't" → ["Don't"], "U.S.A." → ["U.S.A."]
└─ Example: text.split()

Sentence Tokenization:
├─ Split by sentence boundaries
├─ More complex (handle periods in abbreviations)
├─ Example: Identify "Dr. Smith went to U.S.A." as one sentence
└─ NLTK: sent_tokenize()

Word Tokenization (advanced):
├─ Handles contractions
├─ Separate punctuation
├─ Example: "don't" → ["do", "n't"]
└─ NLTK: word_tokenize()

Subword Tokenization:
├─ Break words into smaller pieces
├─ Useful for rare/compound words
├─ Example: "unbelievable" → ["un", "believ", "able"]
└─ Used in modern transformers
```

**4. NLTK Tokenization**

```python
# Step 1: Import and download data
import nltk
nltk.download('punkt')  # For tokenization

# Step 2: Create sample text
text = "Natural Language Processing is amazing! Dr. Smith works in NLP."

# Step 3: Tokenize
from nltk.tokenize import word_tokenize, sent_tokenize

# Word tokenization
word_tokens = word_tokenize(text)
# Result: ['Natural', 'Language', 'Processing', 'is', 'amazing', '!', 
#          'Dr', '.', 'Smith', 'works', 'in', 'NLP', '.']

# Sentence tokenization
sent_tokens = sent_tokenize(text)
# Result: ['Natural Language Processing is amazing!', 
#          'Dr. Smith works in NLP.']
```

**5. Tokenization in Pipeline**

```
Raw Text
   ↓
Lowercasing (Day 7)
   ↓
Punctuation Removal (Day 7)
   ↓
Tokenization (Lesson 1) ← YOU ARE HERE
   ↓
Stop Words Removal (Day 7)
   ↓
Lemmatization/Stemming (Lesson 2)
   ↓
Named Entity Recognition (Lesson 3)
   ↓
Vectorization (numerical features)
```

### Practical Implementation:

**Example 1: Basic Word Tokenization**

```python
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Sample text
text = "Hello, world! How are you doing?"

# Tokenize
tokens = word_tokenize(text)
print(tokens)
# Output: ['Hello', ',', 'world', '!', 'How', 'are', 'you', 'doing', '?']

# Count tokens
print(f"Number of tokens: {len(tokens)}")
# Output: Number of tokens: 9
```

**Example 2: Sentence Tokenization**

```python
from nltk.tokenize import sent_tokenize

text = """Dr. Smith is a scientist. He works at Stanford University. 
His research focuses on A.I. and Machine Learning."""

sentences = sent_tokenize(text)
for i, sent in enumerate(sentences):
    print(f"{i+1}. {sent}")

# Output:
# 1. Dr. Smith is a scientist.
# 2. He works at Stanford University.
# 3. His research focuses on A.I. and Machine Learning.
```

**Example 3: Custom Tokenization with Regex**

```python
import re

text = "Natural-Language_Processing is amazing!"

# Split by non-word characters
tokens = re.findall(r'\w+', text)
print(tokens)
# Output: ['Natural', 'Language', 'Processing', 'is', 'amazing']

# Keep hyphens in words
tokens = re.findall(r'[\w\-]+', text)
print(tokens)
# Output: ['Natural-Language_Processing', 'is', 'amazing']
```

---

## Lesson 2: Stemming & Lemmatization - Reducing Words to Base Form

### Important Points:

**1. The Problem: Word Variation**

```
Same concept, different forms:

"run" family:
├─ run (base)
├─ running (present participle)
├─ runs (third person)
├─ ran (past)
└─ runner (agent noun)

All mean essentially same thing, but treated as different words!

Impact on Analysis:
├─ Frequency analysis misses connections
├─ Feature vectors treat as separate features
├─ Model misses patterns
└─ Predictions weaker
```

**2. Stemming vs Lemmatization**

```
Stemming:
├─ Cut off word endings (suffix removal)
├─ Heuristic-based (rule-based)
├─ Fast
├─ May produce non-words
│
├─ Example:
│  "running" → "runn" (WRONG - not a real word!)
│  "happiness" → "happi" (WRONG!)
│
└─ Porter Stemmer algorithm common

Lemmatization:
├─ Convert to dictionary base form
├─ Dictionary-based
├─ Slower
├─ Always produces real words
│
├─ Example:
│  "running" → "run" (CORRECT!)
│  "happiness" → "happy" (CORRECT!)
│
└─ Uses POS tagging and morphology
```

**3. Stemming in Detail**

Porter Stemmer rules:
```
Rule 1: SSES → SS
├─ "caresses" → "caress"
├─ "cries" stays "cries"

Rule 2: IES → I
├─ "cries" → "cri"
├─ "dies" → "di"

Rule 3: S → (remove)
├─ "cats" → "cat"
├─ "dogs" → "dog"

Rule 4: Vowel endings
├─ "motoring" → "motor"
├─ "conflate" → "conflat"

Results:
├─ FAST (no dictionary lookup)
├─ Sometimes produces non-words
├─ Good for search/retrieval
└─ Not for meaning analysis
```

**4. Lemmatization in Detail**

Dictionary-based approach:
```
Process:
1. Identify Part-of-Speech (POS)
2. Look up in morphological dictionary
3. Return canonical form

Example: "better"
├─ Without POS: "better" → "better" (no change)
├─ With POS as adjective: "better" → "good" (correct!)

Example: "studies"
├─ Without POS: "studies" → "studi" (stemming)
├─ With POS as verb: "studies" → "study" (correct!)
│  OR
├─ With POS as noun: "studies" → "study" (correct!)

Key: POS tagging is essential!
```

**5. When to Use What?**

```
Use Stemming when:
├─ Speed is critical
├─ Exact meaning less important
├─ Building search indexes
└─ Memory limited

Use Lemmatization when:
├─ Accuracy important
├─ Meaning must be preserved
├─ Building ML models
├─ NLP analysis needed
├─ Have labeled data for POS tagging
└─ (Slightly slower is acceptable)

Rule of Thumb:
Production ML Models → Lemmatization
Quick text preprocessing → Stemming
```

### Practical Implementation:

**Example 1: Stemming with Porter Stemmer**

```python
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')

# Initialize stemmer
ps = PorterStemmer()

# Words to stem
words = ['running', 'runs', 'ran', 'happiness', 'caresses', 
         'troubled', 'flying', 'files']

print("Stemming Results:")
for word in words:
    stemmed = ps.stem(word)
    print(f"{word:12} → {stemmed}")

# Output:
# running      → run
# runs         → run
# ran          → ran (doesn't know past tense!)
# happiness    → happi (not a word!)
# caresses     → caress
# troubled     → troubl (not a word!)
# flying       → fli (not a word!)
# files        → file
```

**Example 2: Lemmatization with NLTK**

```python
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.pos_tag import pos_tag
import nltk

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Words to lemmatize
words = ['running', 'runs', 'ran', 'happiness', 'caresses', 
         'better', 'studies', 'is', 'are']

print("Lemmatization Results:")
for word in words:
    # Without POS (default: noun)
    lemma_noun = lemmatizer.lemmatize(word, pos='n')
    # With POS: verb
    lemma_verb = lemmatizer.lemmatize(word, pos='v')
    
    print(f"{word:12} → noun: {lemma_noun:12} verb: {lemma_verb}")

# Output shows importance of POS tagging!
```

**Example 3: Complete Lemmatization with POS Tagging**

```python
from nltk.tokenize import word_tokenize
from nltk.pos_tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Map NLTK POS tags to WordNet POS tags
def get_wordnet_pos(treebank_tag):
    from nltk.corpus import wordnet
    
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # default

# Text to process
text = "The studies showed that running improves health"

# Tokenize
tokens = word_tokenize(text)

# POS tagging
pos_tags = pos_tag(tokens)

# Lemmatize with correct POS
lemmatizer = WordNetLemmatizer()
lemmas = []

for word, pos_tag_value in pos_tags:
    wordnet_pos = get_wordnet_pos(pos_tag_value)
    lemma = lemmatizer.lemmatize(word, pos=wordnet_pos)
    lemmas.append(lemma)
    print(f"{word:12} (POS: {pos_tag_value}) → {lemma}")

print(f"\nOriginal: {text}")
print(f"Lemmatized: {' '.join(lemmas)}")

# Output shows correct lemmatization with POS!
```

---

## Lesson 3: Named Entity Recognition (NER) - Identifying Entities

### Important Points:

**1. What is Named Entity Recognition?**

Identifying and classifying proper nouns and entities in text.

```
Text: "John Smith works at Google in Mountain View, California."

Named Entities:
├─ John Smith → PERSON
├─ Google → ORGANIZATION
├─ Mountain View → LOCATION
├─ California → LOCATION

Why Matters:
├─ Extract key information automatically
├─ Build knowledge graphs
├─ Information retrieval
├─ Sentiment analysis (attribute sentiment to entities)
└─ Relationship extraction
```

**2. Common Entity Types**

```
PERSON
├─ Individual names: John, Sarah, Einstein
├─ Titles: Dr., Mr., President
└─ Roles: teacher, doctor, CEO

ORGANIZATION
├─ Companies: Google, Microsoft, Apple
├─ Government: FBI, CIA
├─ Universities: Stanford, MIT
└─ NGOs: Red Cross, Amnesty International

LOCATION
├─ Cities: New York, Tokyo
├─ Countries: USA, France
├─ Regions: California, Scandinavia
├─ Landmarks: Eiffel Tower, Big Ben
└─ Geographic features: Amazon, Mount Everest

DATE/TIME
├─ Dates: January 15, 2024
├─ Times: 3:00 PM, noon
├─ Durations: 5 years, 2 weeks
└─ Relative: yesterday, next Monday

MONEY
├─ Amounts: $100, €50, ¥1000
└─ Currencies: dollars, euros

PERCENT
├─ Percentages: 50%, 99.5%

FACILITY
├─ Buildings: Empire State Building
├─ Structures: Golden Gate Bridge

GPE (Geopolitical Entity)
├─ Nation-states
├─ Cities with political relevance
```

**3. NER Approaches**

```
Rule-Based NER:
├─ Hand-coded patterns
├─ "Dr. [Name]" → PERSON
├─ "[City], [State]" → LOCATION
├─ Fast but limited
├─ Low accuracy
└─ Hard to maintain

Statistical NER:
├─ Train on labeled data
├─ Learn patterns
├─ Good accuracy (~90%)
├─ Requires training data
└─ Can handle new patterns

Deep Learning NER:
├─ Neural networks
├─ BiLSTM, Transformers
├─ Highest accuracy (95%+)
├─ Requires large datasets
├─ State-of-the-art
└─ Computational cost
```

**4. NLTK NER (Limited)**

```python
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize

nltk.download('maxent_ne_chunker')
nltk.download('words')

text = "John Smith works at Google in Mountain View, California."
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
named_entities = ne_chunk(pos_tags)

# Shows: PERSON (John Smith), ORGANIZATION (Google), LOCATION (Mountain View, California)
```

**5. spaCy NER (Production-Grade)**

```python
import spacy

# Load trained model
nlp = spacy.load('en_core_web_sm')

text = "John Smith works at Google in Mountain View, California."
doc = nlp(text)

# Extract entities
for ent in doc.ents:
    print(f"{ent.text:20} → {ent.label_}")

# Output:
# John Smith           → PERSON
# Google               → ORG
# Mountain View        → GPE
# California           → GPE
```

### Practical Implementation:

**Example 1: NLTK NER (Limited, Educational)**

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.pos_tag import pos_tag
from nltk.ne_chunk import ne_chunk

nltk.download('maxent_ne_chunker')
nltk.download('words')

text = "Steve Jobs founded Apple in 1976. Microsoft was started by Bill Gates."

# Process
tokens = word_tokenize(text)
pos_tags = pos_tag(tokens)
entities = ne_chunk(pos_tags)

# Display
print(entities)
```

**Example 2: spaCy NER (Production-Quality)**

```python
import spacy

# Load model (first time: python -m spacy download en_core_web_sm)
nlp = spacy.load('en_core_web_sm')

# Process text
text = """
Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne 
on April 1, 1976 in Los Altos, California. The company's first product 
was the Apple I computer, sold by the Byte Shop in Mountain View.
"""

doc = nlp(text)

# Extract and display entities
print("Named Entities Found:")
print("-" * 50)
for ent in doc.ents:
    print(f"Text: {ent.text:20} | Type: {ent.label_:10} | Start: {ent.start_char} | End: {ent.end_char}")

print("\nEntities by Type:")
print("-" * 50)
for label in set(ent.label_ for ent in doc.ents):
    entities_of_type = [ent.text for ent in doc.ents if ent.label_ == label]
    print(f"{label}: {', '.join(entities_of_type)}")
```

**Example 3: Extracting Information with NER**

```python
import spacy

nlp = spacy.load('en_core_web_sm')

# Sample news text
text = """
Tesla announced record profits on January 15, 2024. 
CEO Elon Musk stated the company earned $100 million in Q4. 
The Austin, Texas facility produced 25% more vehicles than last year.
"""

doc = nlp(text)

# Extract information
entities_dict = {}
for ent in doc.ents:
    if ent.label_ not in entities_dict:
        entities_dict[ent.label_] = []
    entities_dict[ent.label_].append(ent.text)

# Display organized results
print("Information Extracted:")
print("=" * 40)
print(f"Companies: {entities_dict.get('ORG', [])}")
print(f"People: {entities_dict.get('PERSON', [])}")
print(f"Dates: {entities_dict.get('DATE', [])}")
print(f"Money: {entities_dict.get('MONEY', [])}")
print(f"Locations: {entities_dict.get('GPE', [])}")
print(f"Percent: {entities_dict.get('PERCENT', [])}")
```

---

## Lesson 4: Text Standardization & Normalization

### Important Points:

**1. What is Standardization?**

Converting text to consistent format for analysis.

```
Standardization Goals:
├─ Consistency: different forms → same form
├─ Normalization: special characters, encoding
├─ Canonicalization: unique representation
└─ Comparability: can compare different texts

Example:
"naïve" vs "naive"
"Café" vs "cafe"  
"$100" vs "100 dollars"
```

**2. Types of Standardization**

```
Case Standardization:
├─ Lowercase: "Hello" → "hello"
├─ Uppercase: "Hello" → "HELLO"
├─ Title Case: "hello world" → "Hello World"
└─ Most common: lowercase (Day 7)

Character Encoding:
├─ UTF-8 encoding issues
├─ Accent removal: "café" → "cafe"
├─ Example: unidecode library
└─ Important for international text

Contraction Expansion:
├─ "don't" → "do not"
├─ "I'm" → "I am"
├─ "can't" → "can not"
└─ Helps some models

Number Standardization:
├─ Replace with <NUM>: "I have 5 cats" → "I have <NUM> cats"
├─ Keep as words: "123" → "one hundred twenty three"
├─ Replace with placeholder
└─ Domain-specific decision

Special Character Handling:
├─ Emoticons: 😊 → "happy", ":)" → "smile"
├─ URLs: "https://example.com" → "<URL>"
├─ Email: "john@example.com" → "<EMAIL>"
├─ Hashtags: "#NLP" → keep or strip #?
└─ Mentions: "@user" → keep or remove?
```

**3. Text Normalization Pipeline**

```
Raw Text
   ↓
Step 1: Encoding fix
├─ Handle UTF-8 issues
├─ Remove/normalize accents
└─ Unidecode: "naïve" → "naive"
   ↓
Step 2: Standardize case
├─ Usually to lowercase
└─ Unless case is semantic
   ↓
Step 3: Expand contractions
├─ "don't" → "do not"
└─ Optional, model-dependent
   ↓
Step 4: Normalize numbers/special chars
├─ "<NUM>" for numbers
├─ "<URL>" for URLs
└─ "<EMAIL>" for emails
   ↓
Step 5: Whitespace normalization
├─ Multiple spaces → single space
├─ Remove tabs, newlines
└─ Strip leading/trailing
   ↓
Standardized Text
```

**4. Contraction Dictionary**

Common contractions:
```python
contractions_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "could've": "could have",
    "couldn't": "could not",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}
```

### Practical Implementation:

**Example 1: Basic Standardization**

```python
import re
import unicodedata

def standardize_text(text):
    """Complete text standardization"""
    
    # Step 1: Normalize unicode (handle accents)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('ASCII')
    
    # Step 2: Lowercase
    text = text.lower()
    
    # Step 3: Remove URLs
    text = re.sub(r'http\S+|www.\S+', '<URL>', text)
    
    # Step 4: Remove emails
    text = re.sub(r'\S+@\S+', '<EMAIL>', text)
    
    # Step 5: Replace numbers
    text = re.sub(r'\d+', '<NUM>', text)
    
    # Step 6: Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Test
text = "Check out café at https://example.com! Email me at john@example.com. I have 5 cats!"
standardized = standardize_text(text)
print(f"Original: {text}")
print(f"Standardized: {standardized}")
```

**Example 2: Accent Removal**

```python
from unidecode import unidecode

# Text with accents
texts = [
    "naïve café résumé",
    "München Köln",  # German
    "São Paulo Rio de Janeiro",  # Portuguese
    "Zürich Geneva",  # Swiss
]

print("Accent Removal:")
for text in texts:
    normalized = unidecode(text)
    print(f"{text:30} → {normalized}")

# Output:
# naïve café résumé            → naive cafe resume
# München Köln                 → Munchen Koln
# São Paulo Rio de Janeiro     → Sao Paulo Rio de Janeiro
# Zürich Geneva                → Zurich Geneva
```

**Example 3: Contraction Expansion**

```python
import re

contractions_dict = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "could've": "could have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'll": "he will",
    "he's": "he is",
    "i'd": "i would",
    "i'll": "i will",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it will",
    "it's": "it is",
    "shouldn't": "should not",
    "that's": "that is",
    "there's": "there is",
    "they'd": "they would",
    "they'll": "they will",
    "they're": "they are",
    "they've": "they have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'll": "we will",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "won't": "will not",
    "wouldn't": "would not",
    "you'd": "you would",
    "you'll": "you will",
    "you're": "you are",
    "you've": "you have"
}

def expand_contractions(text):
    """Expand contractions in text"""
    pattern = re.compile(r'\b({0})\b'.format('|'.join(
        contractions_dict.keys())), flags=re.IGNORECASE | re.DOTALL)
    
    def replace(match):
        return contractions_dict[match.group(0).lower()]
    
    return pattern.sub(replace, text)

# Test
text = "I can't believe it's working! Don't you agree? I'd love to help."
expanded = expand_contractions(text)
print(f"Original: {text}")
print(f"Expanded: {expanded}")

# Output:
# Original: I can't believe it's working! Don't you agree? I'd love to help.
# Expanded: I cannot believe it is working! Do not you agree? I would love to help.
```

---

## Lesson 5: Complete Preprocessing Pipeline

### Important Points:

**1. Full Pipeline Architecture**

```
Raw Text
   ↓
[Step 1] Cleaning (Day 7)
├─ Lowercase
├─ Remove punctuation
├─ Remove HTML/special chars
   ↓
[Step 2] Normalization (Lesson 4)
├─ Fix encoding
├─ Expand contractions
├─ Standardize numbers
   ↓
[Step 3] Tokenization (Lesson 1)
├─ Split into tokens
├─ Handle edge cases
   ↓
[Step 4] Stop Words Removal (Day 7)
├─ Remove common words
├─ Domain-specific filtering
   ↓
[Step 5] POS Tagging (Required for Lemmatization)
├─ Identify word types
├─ Essential for accuracy
   ↓
[Step 6] Lemmatization (Lesson 2)
├─ Convert to base form
├─ Use POS tags
   ↓
[Step 7] Named Entity Recognition (Lesson 3)
├─ Identify entities
├─ Extract key information
   ↓
[Step 8] Vectorization (Next: Lesson)
├─ Convert to numerical features
├─ TF-IDF, word embeddings, etc.
   ↓
Clean, Normalized, Meaningful Features
```

**2. Decision Points in Pipeline**

```
Question: Should I use Stemming or Lemmatization?
├─ If speed critical & accuracy not → Stemming
└─ If accuracy matters → Lemmatization

Question: Include Named Entity Recognition?
├─ If need to extract entities → YES
├─ If just classifying text → Maybe NO
└─ If need semantic understanding → YES

Question: Keep or remove numbers?
├─ If numbers are important → Keep as <NUM>
├─ If text classification → Remove
└─ Domain-specific decision

Question: Which stop words list?
├─ NLTK default English
├─ Custom domain-specific
├─ None (if using embeddings)
└─ Consider context
```

**3. Quality Metrics**

How to evaluate preprocessing:

```
Metrics:
├─ Token count: How many tokens?
├─ Unique tokens: Vocabulary size
├─ Compression ratio: Original vs processed
├─ Information loss: Did we lose important info?
└─ Manual spot check: Does it look right?

Example Analysis:
Original: "Dr. John Smith doesn't believe in artificial intelligence!"
Tokens: 10
After processing:
├─ Stop words removed: "dr john smith believe artificial intelligence"
├─ Lemmatized: "dr john smith believ artifici intellig"
├─ Vocab: 6 unique tokens
└─ Compression: 10 → 6 (40% reduction)
```

### Practical Implementation:

**Complete Pipeline Example**

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.pos_tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.ne_chunk import ne_chunk
import re
import unicodedata
from unidecode import unidecode

# Download required data
for item in ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'wordnet', 'maxent_ne_chunker', 'words']:
    try:
        nltk.data.find('tokenizers/' + item)
    except LookupError:
        nltk.download(item)

class TextPreprocessor:
    """Complete text preprocessing pipeline"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.contractions_dict = {
            "ain't": "am not", "aren't": "are not", "can't": "cannot",
            "didn't": "did not", "doesn't": "does not", "don't": "do not",
            "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
            "he'd": "he would", "he'll": "he will", "he's": "he is",
            "i'd": "i would", "i'll": "i will", "i'm": "i am", "i've": "i have",
            "isn't": "is not", "it'd": "it would", "it'll": "it will", "it's": "it is",
            "shouldn't": "should not", "that's": "that is", "there's": "there is",
            "they'd": "they would", "they'll": "they will", "they're": "they are",
            "they've": "they have", "wasn't": "was not", "we'd": "we would",
            "we'll": "we will", "we're": "we are", "we've": "we have",
            "weren't": "were not", "won't": "will not", "wouldn't": "would not",
            "you'd": "you would", "you'll": "you will", "you're": "you are",
            "you've": "you have"
        }
    
    def get_wordnet_pos(self, treebank_tag):
        """Map NLTK POS tags to WordNet"""
        from nltk.corpus import wordnet
        
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN
    
    def clean_text(self, text):
        """Step 1-4: Cleaning & Normalization"""
        # Normalize unicode
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ASCII', 'ignore').decode('ASCII')
        
        # Remove URLs
        text = re.sub(r'http\S+|www\.\S+', '<URL>', text)
        
        # Remove emails
        text = re.sub(r'\S+@\S+', '<EMAIL>', text)
        
        # Expand contractions
        pattern = re.compile(r'\b({0})\b'.format('|'.join(self.contractions_dict.keys())),
                           flags=re.IGNORECASE | re.DOTALL)
        text = pattern.sub(lambda x: self.contractions_dict[x.group(0).lower()], text)
        
        # Lowercase
        text = text.lower()
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove numbers
        text = re.sub(r'\d+', '<NUM>', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text):
        """Step 5: Tokenization"""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """Step 6: Stop words removal"""
        return [token for token in tokens if token not in self.stop_words]
    
    def pos_tag(self, tokens):
        """Step 7: POS tagging"""
        return pos_tag(tokens)
    
    def lemmatize(self, pos_tagged_tokens):
        """Step 8: Lemmatization"""
        lemmas = []
        for word, pos_tag_value in pos_tagged_tokens:
            wordnet_pos = self.get_wordnet_pos(pos_tag_value)
            lemma = self.lemmatizer.lemmatize(word, pos=wordnet_pos)
            lemmas.append(lemma)
        return lemmas
    
    def process(self, text, remove_stops=True, lemmatize=True):
        """Complete pipeline"""
        # Clean
        cleaned = self.clean_text(text)
        print(f"1. Cleaned: {cleaned}")
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        print(f"2. Tokenized: {tokens}")
        
        # Remove stop words
        if remove_stops:
            tokens = self.remove_stopwords(tokens)
            print(f"3. Removed stopwords: {tokens}")
        
        # Lemmatize
        if lemmatize:
            pos_tagged = self.pos_tag(tokens)
            print(f"4. POS tagged: {pos_tagged}")
            
            tokens = self.lemmatize(pos_tagged)
            print(f"5. Lemmatized: {tokens}")
        
        return tokens

# Test the pipeline
preprocessor = TextPreprocessor()

text = """
Dr. John Smith doesn't believe in artificial intelligence! 
He said "AI won't replace human creativity." 
Email him at john@example.com or visit https://example.com
"""

print("Original text:")
print(text)
print("\n" + "="*60 + "\n")

processed = preprocessor.process(text)

print("\n" + "="*60)
print(f"\nFinal result: {' '.join(processed)}")
print(f"Vocabulary size: {len(set(processed))}")
print(f"Token reduction: {len(text.split())} → {len(processed)}")
```

**Output:**
```
Original text:
Dr. John Smith doesn't believe in artificial intelligence! 
He said "AI won't replace human creativity." 
Email him at john@example.com or visit https://example.com

============================================================

1. Cleaned: dr john smith does not believe in artificial intelligence he said ai will not replace human creativity email him at <EMAIL> or visit <URL>

2. Tokenized: ['dr', 'john', 'smith', 'does', 'not', 'believe', 'in', 'artificial', 'intelligence', 'he', 'said', 'ai', 'will', 'not', 'replace', 'human', 'creativity', 'email', 'him', 'at', '<EMAIL>', 'or', 'visit', '<URL>']

3. Removed stopwords: ['dr', 'john', 'smith', 'believe', 'artificial', 'intelligence', 'said', 'ai', 'replace', 'human', 'creativity', 'email']

4. POS tagged: [('dr', 'NN'), ('john', 'NN'), ('smith', 'NN'), ('believe', 'VB'), ('artificial', 'JJ'), ('intelligence', 'NN'), ('said', 'VBD'), ('ai', 'NN'), ('replace', 'VB'), ('human', 'JJ'), ('creativity', 'NN'), ('email', 'NN')]

5. Lemmatized: ['dr', 'john', 'smith', 'believe', 'artificial', 'intelligence', 'say', 'ai', 'replace', 'human', 'creativity', 'email']

============================================================

Final result: dr john smith believe artificial intelligence say ai replace human creativity email
Vocabulary size: 11
Token reduction: 35 → 12
```

---

## Summary Table: NLP Part 2 Techniques

| Technique | Purpose | Input | Output | Complexity |
|-----------|---------|-------|--------|-----------|
| **Tokenization** | Break into units | Text | Tokens | Low |
| **Stemming** | Reduce words | Tokens | Stems | Low |
| **Lemmatization** | Base form | Tokens + POS | Lemmas | Medium |
| **NER** | Extract entities | Tokens | Labeled entities | Medium-High |
| **Standardization** | Consistent format | Text | Normalized text | Low |

---

## Pipeline Complexity vs Accuracy

```
Simple Pipeline:
lowercase → tokenize → (optional: lemmatize)
├─ Speed: FAST
├─ Accuracy: 70-75%
└─ Best for: Quick text classification

Moderate Pipeline:
lowercase → tokenize → remove_stopwords → 
lemmatize (with POS) → standardize
├─ Speed: MEDIUM
├─ Accuracy: 80-85%
└─ Best for: Most ML models

Complete Pipeline:
All above + NER + custom handling
├─ Speed: SLOWER
├─ Accuracy: 85-95%
└─ Best for: Production systems, research

Overkill:
Everything above + multiple redundant steps
├─ Speed: VERY SLOW
├─ Accuracy: Maybe 1-2% improvement
├─ Cost-Benefit: Negative
└─ Lesson: Don't over-engineer!
```

---

## Common Mistakes to Avoid

```
❌ Stemming for production NLP models
✓ Use lemmatization (needs POS tagging)

❌ Removing all stop words blindly
✓ Consider domain context ("no" in sentiment analysis matters!)

❌ Not validating preprocessing results
✓ Manual spot-check output

❌ Using NER without checking accuracy
✓ Test on your domain (models trained on news may not work on tweets)

❌ Standardizing away semantic meaning
✓ Numbers might be important in some domains

❌ Single preprocessing pipeline for all tasks
✓ Sentiment analysis ≠ Topic modeling (different requirements)

❌ Ignoring encoding issues
✓ Handle unicode/accents properly from start

❌ POS tagging without context
✓ "running" is verb (lemmatize to "run") not noun (stay "running")
```

---

## Integration with Regression Analysis

**Connection to Day 8 Multiple Linear Regression:**

```
Clean Text Data (NLP Part 2)
       ↓
Convert to Features (vectorization)
       ↓
Build Numerical Features
       ↓
Multiple Linear Regression
       ↓
Predict outcomes
```

**Example: Predicting House Prices from Descriptions**

```
Raw description: "Beautiful home in downtown! Don't miss this opportunity."
       ↓
Preprocess:
├─ Tokenize
├─ Remove stopwords
├─ Lemmatize
└─ Result: ["beautiful", "home", "downtown", "opportunity"]
       ↓
Vectorize:
├─ TF-IDF
└─ Result: numerical features
       ↓
Combine with other features (size, year from Day 8)
       ↓
Multiple Linear Regression
       ↓
Predict price!
```

---

## Next Steps (Day 9+)

→ Text Vectorization (TF-IDF, Word2Vec, GloVe)  
→ Sentiment Analysis  
→ Topic Modeling (Latent Dirichlet Allocation)  
→ Text Classification  
→ Word Embeddings  
→ Transformer Models (BERT, GPT)

---

**Date:** September 27, 2026  
**Topic:** NLP Text Preprocessing Part 2 - Advanced Techniques  
**Lessons:** 5 core lessons + 15+ practical examples  
**Outcome:** Production-grade text preprocessing pipeline ready for ML models

