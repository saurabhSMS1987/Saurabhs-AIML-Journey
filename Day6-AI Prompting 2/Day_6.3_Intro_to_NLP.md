# Day 6: Introduction to Natural Language Processing (NLP)

**Author:** Saurabh Shirgaokar  
**Date:** September 25, 2026  
**Topic:** Foundations of NLP  
**Level:** Beginner to Intermediate

---

## 🎯 What is NLP?

**Natural Language Processing** = Teaching computers to understand, generate, and classify human language

```
Traditional Programming:
Input: 1, 2, 3
Logic: Add them
Output: 6

NLP:
Input: "I love this product!"
Logic: Understand sentiment
Output: Positive (confidence: 95%)
```

---

## Part 1: Why NLP Matters

### Real-World Applications

```
✓ Email spam detection
✓ Chatbots and customer service
✓ Social media sentiment analysis
✓ Document classification
✓ Search engines
✓ Language translation
✓ Voice assistants (Alexa, Siri)
✓ Recommendation systems
```

**Business Impact:**
```
Automate text processing at scale
Understand customer feedback instantly
Extract insights from documents
Reduce manual work by 70-80%
```

---

## Part 2: NLP Pipeline Overview

The course covers 6 major topics:

```
1. TEXT PRE-PROCESSING
   Clean and prepare text data
   ├─ Remove noise
   ├─ Tokenization (split into words)
   ├─ Lowercasing
   └─ Remove punctuation/stopwords

2. PARTS OF SPEECH & NAMED ENTITIES
   Understand grammar and extract entities
   ├─ Tag words (noun, verb, adjective)
   ├─ Identify names and locations
   ├─ Extract key information
   └─ Build knowledge bases

3. SENTIMENT ANALYSIS
   Determine emotion/opinion in text
   ├─ Classify as positive/negative/neutral
   ├─ Analyze customer reviews
   ├─ Monitor social media
   └─ Track brand perception

4. TEXT VECTORIZATION
   Convert text to numbers for ML
   ├─ Bag of Words
   ├─ TF-IDF
   ├─ Word embeddings (Word2Vec)
   └─ Prepare for machine learning

5. ADVANCED TOPICS
   Complex techniques
   ├─ Topic Modeling (discover themes)
   ├─ Custom Classifiers
   ├─ Deep learning for NLP
   └─ Fine-tuning models

6. CASE STUDY
   Apply everything to real problem
   └─ Portfolio project
```

---

## Part 3: Core NLP Tasks

### Task 1: Text Pre-Processing

```python
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

text = "Hello! I LOVE this product. It's amazing!!!"

# Step 1: Lowercase
text = text.lower()
# Result: "hello! i love this product. it's amazing!!!"

# Step 2: Tokenization (split into words)
tokens = word_tokenize(text)
# Result: ['hello', '!', 'i', 'love', 'this', 'product', '.', 'it', "'s", 'amazing', '!', '!', '!']

# Step 3: Remove punctuation
tokens = [word for word in tokens if word.isalnum()]
# Result: ['hello', 'i', 'love', 'this', 'product', 'it', 's', 'amazing']

# Step 4: Remove stopwords (common words)
stop_words = set(stopwords.words('english'))
tokens = [word for word in tokens if word not in stop_words]
# Result: ['love', 'product', 'amazing']

print(tokens)
```

---

### Task 2: Parts of Speech Tagging

```python
import nltk
from nltk import pos_tag, word_tokenize

sentence = "The quick brown fox jumps over the lazy dog"
tokens = word_tokenize(sentence)

# Tag parts of speech
tagged = pos_tag(tokens)

print(tagged)
# Output:
# [('The', 'DT'), ('quick', 'JJ'), ('brown', 'JJ'), ('fox', 'NN'),
#  ('jumps', 'VBZ'), ('over', 'IN'), ('the', 'DT'), ('lazy', 'JJ'),
#  ('dog', 'NN')]

# DT=Determiner, JJ=Adjective, NN=Noun, VBZ=Verb, IN=Preposition
```

---

### Task 3: Named Entity Recognition (NER)

```python
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize

sentence = "John Smith works at Google in San Francisco"
tokens = word_tokenize(sentence)
tagged = pos_tag(tokens)

# Extract named entities
entities = ne_chunk(tagged)

print(entities)
# Output identifies:
# PERSON: John Smith
# ORG: Google
# LOCATION: San Francisco
```

---

### Task 4: Sentiment Analysis

```python
from textblob import TextBlob

# Method 1: TextBlob (simple)
texts = [
    "I love this product! It's amazing!",
    "This is terrible. Worst purchase ever.",
    "It's okay. Nothing special."
]

for text in texts:
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 to 1
    
    if sentiment > 0.1:
        result = "Positive"
    elif sentiment < -0.1:
        result = "Negative"
    else:
        result = "Neutral"
    
    print(f"Text: {text}")
    print(f"Sentiment: {result} (Score: {sentiment})\n")

# Output:
# Text: I love this product! It's amazing!
# Sentiment: Positive (Score: 0.8)
#
# Text: This is terrible. Worst purchase ever.
# Sentiment: Negative (Score: -0.9)
#
# Text: It's okay. Nothing special.
# Sentiment: Neutral (Score: 0.0)
```

---

### Task 5: Text Vectorization (TF-IDF)

```python
from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    "I love pizza and pasta",
    "Pizza is my favorite food",
    "I prefer pasta over pizza",
    "Cats and dogs are pets"
]

# Convert text to numerical vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)

print("Feature names:", vectorizer.get_feature_names_out())
# Shows all unique words and their importance

print("\nDocument vectors:")
print(vectors.toarray())
# Each row = one document, columns = word importance scores
```

---

## Part 4: Practical Implementation - Customer Review Analysis

### Complete Example: Analyze Product Reviews

```python
import nltk
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from nltk.corpus import stopwords

# Sample reviews
reviews = [
    "Love this product! Amazing quality and fast shipping.",
    "Terrible! Broke after one week. Waste of money.",
    "Good product. Decent quality for the price.",
    "Excellent! Exceeded my expectations. Highly recommend!",
    "Poor quality. Customer service was unhelpful."
]

# Analysis function
def analyze_review(review):
    # Sentiment
    blob = TextBlob(review)
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0.1:
        sentiment_label = "Positive"
    elif sentiment < -0.1:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    
    # Extract keywords (remove stopwords)
    tokens = word_tokenize(review.lower())
    stop_words = set(stopwords.words('english'))
    keywords = [w for w in tokens if w.isalnum() and w not in stop_words]
    
    return {
        'review': review,
        'sentiment': sentiment_label,
        'score': round(sentiment, 2),
        'keywords': keywords[:5]  # Top 5 keywords
    }

# Analyze all reviews
print("=" * 60)
print("REVIEW ANALYSIS REPORT")
print("=" * 60)

positive_count = 0
negative_count = 0

for review in reviews:
    result = analyze_review(review)
    
    print(f"\nReview: {result['review']}")
    print(f"Sentiment: {result['sentiment']} (Score: {result['score']})")
    print(f"Keywords: {', '.join(result['keywords'])}")
    
    if result['sentiment'] == "Positive":
        positive_count += 1
    elif result['sentiment'] == "Negative":
        negative_count += 1

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total Reviews: {len(reviews)}")
print(f"Positive: {positive_count} ({positive_count/len(reviews)*100:.0f}%)")
print(f"Negative: {negative_count} ({negative_count/len(reviews)*100:.0f}%)")
print(f"Average Sentiment: {sum([TestBlob(r).sentiment.polarity for r in reviews])/len(reviews):.2f}")

# Output shows:
# - Each review sentiment
# - Key terms mentioned
# - Overall product perception
# - Actionable insights
```

---

## Part 5: Real-World Use Cases

### Use Case 1: Email Spam Detection
```
Input: Email text
Process:
  - Pre-process (clean text)
  - Extract features (vectorize)
  - Classify (is it spam?)
Output: Spam or Not Spam
```

### Use Case 2: Customer Support Automation
```
Input: Customer inquiry
Process:
  - NER (extract issue type)
  - Sentiment (understand frustration)
  - Classify (route to right team)
Output: Auto-categorized ticket
```

### Use Case 3: Social Media Monitoring
```
Input: Stream of tweets/posts
Process:
  - Sentiment analysis (positive/negative)
  - Extract topics (what's being discussed)
  - Monitor mentions
Output: Brand perception dashboard
```

### Use Case 4: Document Classification
```
Input: Document text
Process:
  - Vectorize
  - Classify category
  - Extract key info
Output: Tagged, organized documents
```

---

## Part 6: Key Libraries & Tools

### Essential Python Libraries

```python
# Text processing
from nltk import ...              # Natural Language Toolkit
from textblob import TextBlob     # Simple sentiment analysis

# Vectorization
from sklearn.feature_extraction.text import TfidfVectorizer

# Advanced NLP
import spacy                      # Industrial-strength NLP
from transformers import ...      # Pre-trained models (BERT, GPT)
```

---

## Part 7: Learning Path

```
Week 1: Foundations
├─ Text pre-processing
├─ Tokenization
└─ Text cleaning

Week 2: Analysis
├─ Parts of speech tagging
├─ Named entity recognition
└─ Sentiment analysis

Week 3: Machine Learning
├─ Text vectorization
├─ Feature extraction
└─ Building classifiers

Week 4: Application
├─ Real-world project
├─ Portfolio piece
└─ Deploy solution
```

---

## Part 8: Common Mistakes to Avoid

```
❌ Skip pre-processing (dirty data = bad results)
❌ Don't understand your data (analyze first)
❌ Overlook edge cases (contractions, slang, emojis)
❌ Use wrong vectorization (TF-IDF vs Word2Vec)
❌ Ignore class imbalance (more positive than negative)

✅ Always pre-process
✅ Explore data thoroughly
✅ Handle special cases
✅ Choose right technique
✅ Balance your dataset
```

---

## Part 9: Quick Reference

### Pre-Processing Pipeline
```python
1. Lowercase text
2. Tokenize (split into words)
3. Remove punctuation
4. Remove stopwords
5. Stemming/Lemmatization (optional)
```

### Sentiment Analysis
```python
blob = TextBlob(text)
sentiment = blob.sentiment.polarity
# -1 to 0: Negative
# 0 to 1: Positive
```

### Text Vectorization
```python
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)
```

---

## Part 10: Key Takeaways

✅ **NLP enables computers to understand language**  
✅ **Pre-processing is critical foundation**  
✅ **Multiple techniques for different tasks** (sentiment, NER, classification)  
✅ **Vectorization converts text to numbers for ML**  
✅ **Real-world applications across industries**  
✅ **Start simple (TextBlob), scale to advanced (Transformers)**  

---

## Part 11: Immediate Next Steps

**This Week:**
- [ ] Learn text pre-processing
- [ ] Practice tokenization and cleaning
- [ ] Build simple sentiment analyzer

**Next Week:**
- [ ] Extract named entities from text
- [ ] Classify documents into categories
- [ ] Build NLP pipeline

**Week 3-4:**
- [ ] Create portfolio project
- [ ] Real-world data analysis
- [ ] Deploy solution

---

## Summary

**NLP is the bridge between human language and machine learning.**

- **Start with basics:** Pre-processing (90% of the work!)
- **Learn techniques:** Sentiment, NER, classification
- **Apply to data:** Build real projects
- **Scale up:** Use modern models (BERT, GPT)

**Impact:** Automate language-based tasks at scale 🚀
