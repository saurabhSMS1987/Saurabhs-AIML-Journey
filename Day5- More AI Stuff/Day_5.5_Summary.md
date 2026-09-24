# Day 5 Summary: Advanced Prompt Engineering, AI Agents & File Operations

**Author:** Saurabh Shirgaokar  
**Date:** September 23, 2026  
**Topics:** 3 areas (Prompt Engineering Part 2 + AI Agents + Python Files) 

---

## 🎯 Day 5 Overview

Three interconnected skills:

```
PROMPT ENGINEERING (Advanced)
    ↓ Apply to
AI AGENTS (Building automation)
    ↓ Data from
PYTHON FILES (Reading/writing)
    ↓
Complete workflow!
```

---

## 📚 PART 1: ADVANCED PROMPT ENGINEERING

### Core Principles (3 Principles)

**Principle 1: Clarity of Output Expectations**
```
Define EXACTLY what you want
❌ "Tell me about history"
✅ "Summarize European history 1800-1902. 1500-2000 words. 
    Chronological format. Include 5-7 major events."
```

**Principle 2: Specificity & Unambiguousness**
```
Remove ALL ambiguous terms
❌ "Write code for data"
✅ "Write Python Pandas code to: load sales.csv, 
    remove null amounts, group by product, calculate revenue"
```

**Principle 3: Proper Framing**
```
Set context for AI response
Different framings = Different quality
- Technical framing (for engineers)
- Business framing (for managers)
- Educational framing (for learners)
```

### The Refinement Loop (Iteration Strategy)

Quality progression with iterations:

```
Iteration 1: 3/10 (Too vague)
     ↓ Add specifics
Iteration 2: 5/10 (Better but incomplete)
     ↓ Add more details
Iteration 3: 8/10 (Professional)
     ↓ Final refinements
Iteration 4: 9/10 (Production-ready!)
```

**Real Example: Data Code**
```
Iter 1: "Write Python code for data"
Output: Generic script (3/10)

Iter 2: "Write Pandas code to load sales.csv, calculate totals"
Output: Better, but missing details (5/10)

Iter 3: "Write Pandas code to load sales.csv, remove nulls, 
        group by product, calculate revenue, include comments"
Output: Good quality (8/10)

Iter 4: "Write production-ready Pandas code to load sales.csv,
        validate data, remove null amounts (log count),
        group by product, calculate revenue & month-over-month growth,
        include docstring, inline comments, error handling"
Output: Production-ready (9/10)
```

### Advanced Techniques (3 Techniques)

1. **Word Limit + Content Specification**
   - Combine quantity with quality requirements
   - "500-700 words, must include 3 examples with metrics"

2. **Before → After Method**
   - Show what NOT to do, then what TO do
   - Guides AI toward correct output type

3. **Role + Scenario Method**
   - Set specific context
   - "You are a data analyst explaining joins to business managers"

### Key Insight
```
450% quality improvement
2/10 (vague) → 9/10 (refined)
Same AI, different prompts → massive difference!
```

---

## 📚 PART 2: BUILDING AI AGENTS

### What is an AI Agent?

```
Traditional Program:
Input → Fixed Logic → Output
(Can't adapt, no intelligence)

AI Agent:
Input → AI Makes Decision → Action → Output
(Learns, adapts, intelligently responds)
```

### Building Blocks (4 Components)

1. **Input Source** - Where data comes from (chat, API, file, database)
2. **AI Decision Making** - The brain (prompt + model selection)
3. **Action Capability** - What it can do (text, API calls, emails, files)
4. **Feedback Loop** - Learning from results (track, refine, improve)

### n8n + Open Router Stack

**n8n = Visual Workflow Automation**
```
✓ Drag-and-drop workflow builder
✓ No coding required
✓ Connect any service
✓ 24/7 automation
✓ Free tier available
```

**Open Router = Unified AI API**
```
✓ Single API key for all models (ChatGPT, Claude, Gemini, etc.)
✓ Switch models instantly
✓ Cost optimization
✓ Fallback support
✓ Free tier available
```

### Simple Agent Example: Customer Support Bot

```
Step 1: Receive Input
└─ Customer message

Step 2: Call AI (via Open Router)
└─ Prompt: "Answer this question professionally"

Step 3: Take Action
└─ Send response to customer

Step 4: Log
└─ Store in database for audit
```

**Result:** 24/7 automated support (No human needed!)

### Real-World Use Cases

**E-Commerce:** Product recommendations (24/7)  
**Finance:** Invoice processing automation  
**Marketing:** Content generation (10x faster)  
**Support:** Customer service chatbots  
**Data:** Analysis report generation  

**Impact:** 24× productivity multiplier

---

## 📚 PART 3: PYTHON FILES - READING & WRITING

### File Operations (3 Core Operations)

```
READ   → Load data from file to Python
WRITE  → Save data from Python to file  
APPEND → Add to end of file
```

### Best Practice: "with" Statement

```python
# Safe file reading (auto-closes)
with open('data.txt', 'r') as file:
    content = file.read()

# Safe file writing
with open('output.txt', 'w') as file:
    file.write("data")

# Safe file appending
with open('log.txt', 'a') as file:
    file.write("new entry")
```

**Why "with":**
- ✓ Auto-closes files
- ✓ Handles errors
- ✓ Prevents file leaks

### File Types & Methods

| Type | Read | Write |
|------|------|-------|
| **Text** | `file.read()` | `file.write()` |
| **CSV** | `csv.reader()` | `csv.writer()` |
| **JSON** | `json.load()` | `json.dump()` |
| **Lines** | `file.readlines()` | `file.writelines()` |

### CSV Example

```python
import csv

# Read CSV
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['Name'])

# Write CSV
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Age'])
    writer.writerow(['Alice', '25'])
```

### JSON Example

```python
import json

# Read JSON
with open('config.json', 'r') as file:
    data = json.load(file)

# Write JSON
with open('config.json', 'w') as file:
    json.dump(data, file, indent=4)
```

### Error Handling

```python
try:
    with open('file.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("No permission")
```

### Practical Pipeline Example

```python
import csv
import json

# 1. Read CSV
with open('raw_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# 2. Process data
processed = []
for row in data:
    processed.append({
        'id': int(row['ID']),
        'name': row['Name'].upper(),
        'value': float(row['Value'])
    })

# 3. Filter
valid_data = [x for x in processed if x['value'] > 0]

# 4. Save to JSON
with open('results.json', 'w') as file:
    json.dump(valid_data, file, indent=4)
```

---

## 🔗 How Everything Connects

```
Write Excellent Prompt (Day 5 Part 1)
           ↓
Build AI Agent (Day 5 Part 2)
           ↓
Agent reads data from files (Day 5 Part 3)
           ↓
Process with AI
           ↓
Write results back to files
           ↓
Complete automation workflow!
```

**Practical Flow:**
1. Agent reads CSV file
2. Uses AI to analyze data
3. Generates insights
4. Writes results to JSON
5. All automated, 24/7

---

## ✅ Learning Checklist

**Prompt Engineering:**
- [ ] Understand 3 core principles
- [ ] Know the refinement loop
- [ ] Can iterate to 9/10 quality
- [ ] Understand 3 advanced techniques

**AI Agents:**
- [ ] Understand what agents are
- [ ] Know n8n basics
- [ ] Know Open Router setup
- [ ] Can build simple agent

**Python Files:**
- [ ] Use "with" statement
- [ ] Read CSV and JSON
- [ ] Write CSV and JSON
- [ ] Handle errors
- [ ] Build data pipeline

---

## 💡 Key Insights

**Prompt Engineering:**
```
Same AI Model + Different Prompts = 450% Quality Difference
The prompt is the differentiator
```

**AI Agents:**
```
No-code platform (n8n) + Unified API (Open Router)
= Anyone can build automation
24× productivity multiplier
```

**Python Files:**
```
Files are the bridge between programs
Read → Process → Write
Fundamental to all data work
```

---

## 🎓 Connection to Week 1

```
Days 1-3: Learn AI fundamentals
    ↓
Day 4: Learn to communicate (prompts) + combine data (joins)
    ↓
Day 5: Master communication → Build automation → Process files
    ↓
Days 6+: Apply to SQL, Power BI, advanced workflows
```

---

## Common Mistakes to Avoid

```
Prompts:        Don't be vague. Iterate 3-4 times. Test results.
AI Agents:      Use no-code platforms. Start simple. Grow complexity.
File Ops:       Always use "with". Handle errors. Validate data.
```

---

## Quick Reference

### Prompt Refinement
```
Iteration 1: 3/10 (vague)
Iteration 2: 5/10 (specifics added)
Iteration 3: 8/10 (near perfect)
Iteration 4: 9/10 (production ready)
```

### Agent Building
```
Input → AI Decision → Action → Output → Log
(Use n8n + Open Router)
```

### File Operations
```python
# Read
with open('file', 'r') as f: data = f.read()

# Write
with open('file', 'w') as f: f.write(data)

# CSV
import csv
# ... csv operations

# JSON
import json
# ... json operations
```
---

*Day 5 transforms you from understanding AI to building with AI.* 🚀
