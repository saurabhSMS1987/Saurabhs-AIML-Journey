# Day 4: Prompt Engineering - Complete Guide

**Author:** Saurabh Shirgaokar  
**Date:** September 22, 2026

---

## Overview

Prompt Engineering is the skill of crafting effective prompts to get the best results from AI tools. It's not about being polite to AI - it's about being **specific, clear, and strategic** in your requests.

**Why Learn This?**
```
✓ Essential skill for all professional roles in 2025+
✓ Applies to ALL AI tools (ChatGPT, Claude, Gemini, DALL-E, etc.)
✓ Directly impacts quality of your work
✓ Multiplies productivity and efficiency
✓ Separates expert users from casual users
```

---

## Part 1: Understanding the Problem

### 1.1 Why Prompts Matter

**Real Example: Compare Responses**

**Scenario:** You need to analyze sales data

**Vague Prompt:**
```
"Analyze my sales data for me"
```

**AI Response:**
```
Sales data analysis typically involves looking at various metrics 
and trends. You should consider factors like revenue, customer 
acquisition costs, and market trends. Different industries have 
different key performance indicators...
```

**Problems:**
- ❌ Too generic
- ❌ Not specific to your data
- ❌ Can't use it directly
- ❌ Time wasted refining
- ❌ Doesn't answer your actual question

---

**Well-Engineered Prompt:**
```
"I have Q3 sales data in CSV format with columns: Date, Product, 
Region, Revenue, Quantity. Please analyze and provide:

1. Total revenue by product (top 5)
2. Regional performance comparison
3. Month-over-month growth rate
4. Any significant trends or anomalies
5. 2-3 actionable recommendations

Format as a professional report suitable for management review.
Use clear formatting with headers and bullet points."
```

**AI Response:**
```
Q3 SALES ANALYSIS

Revenue by Product (Top 5):
- Product A: $250,000 (40%)
- Product B: $150,000 (24%)
...

Regional Performance:
- North: $450,000 (72% growth)
- South: $200,000 (8% growth)
...

Recommendations:
1. Focus marketing on North region (strong growth)
2. Investigate South region decline
...
```

**Benefits:**
- ✅ Specific to your situation
- ✅ Professional format
- ✅ Actionable insights
- ✅ Ready to present
- ✅ Saves hours of work

---

### 1.2 The Spectrum of Prompt Quality

```
Poor Prompt                      Good Prompt
     ↓                               ↓
"Write code"          "Write Python code using Pandas to:
                       1. Read 'sales.csv'
                       2. Remove rows with missing values
                       3. Calculate monthly revenue
                       4. Save to 'processed.csv'
                       Include comments for clarity"

Result: Unusable     Result: Production-ready
Output: Generic      Output: Specific
Quality: 2/10        Quality: 9/10
```

---

## Part 2: The 6 Essential Elements of Great Prompts

### 2.1 Element 1: Specificity

Be **exact** about what you need, not vague.

```
❌ Vague:
"Create a report"

✅ Specific:
"Create a report showing:
- Total sales revenue for Q3 2026
- Breakdown by product category
- Regional performance comparison
- Year-over-year growth percentages
- List of top 10 customers by purchase value"
```

**Why it matters:**
- AI can't read your mind
- Generic requests = generic responses
- Specific requests = targeted, useful responses

---

### 2.2 Element 2: Context

Provide **background information** so AI understands the situation.

```
❌ Without Context:
"Write SQL query for customer analysis"
(AI doesn't know your database structure)

✅ With Context:
"Write SQL query for customer analysis using our PostgreSQL database.
Tables: customers (id, name, email, signup_date)
        orders (id, customer_id, order_date, amount)
        
We need to identify high-value customers for targeted marketing.
Define high-value as: >$5,000 spent in last 12 months, >5 purchases"
(AI knows exactly what you need)
```

**Why it matters:**
- Context prevents misunderstandings
- Helps AI provide relevant solutions
- Reduces iterations needed

---

### 2.3 Element 3: Output Format

Specify **exactly** how you want the output formatted.

```
❌ Without Format Specification:
"Tell me about Python data structures"
(Could be essay, list, table, examples...)

✅ With Format Specification:
"Explain Python data structures in the following format:
1. List (with 2-3 usage examples)
2. Dictionary (with 2-3 usage examples)
3. Tuple (with 2-3 usage examples)
4. Set (with 2-3 usage examples)

For each: include description, when to use, and one code example"
(AI knows exactly how to organize information)
```

**Why it matters:**
- Makes output immediately usable
- Saves reformatting time
- Looks professional

---

### 2.4 Element 4: Examples

Show **one or two examples** of what you mean.

```
❌ Without Examples:
"Categorize this feedback as positive or negative"

✅ With Examples:
"Categorize this feedback as positive or negative.

Positive example: 'Amazing product! Works perfectly. Highly recommend!'
Negative example: 'Broke after 2 days. Waste of money.'

Now categorize these: [your feedback list]"
(AI knows exactly what distinguishes positive from negative)
```

**Why it matters:**
- Removes ambiguity
- Aligns AI output with your expectations
- Especially important for classification tasks

---

### 2.5 Element 5: Audience Definition

Specify **who will read/use** this output.

```
❌ Without Audience Definition:
"Explain machine learning"

✅ With Audience Definition:
"Explain machine learning to a business manager with NO technical 
background. They need to understand:
- What it is (in simple terms)
- Why the company should care
- ROI and business impact
- Common misconceptions

Use everyday analogies. Avoid technical jargon. 
Include 2-3 real business examples from retail, finance, or healthcare"
(AI adjusts complexity and examples for the audience)
```

**Why it matters:**
- Determines technical level
- Affects vocabulary and examples used
- Makes output relevant to reader

---

### 2.6 Element 6: Constraints

Mention any **limitations or requirements**.

```
❌ Without Constraints:
"Write an article about AI"

✅ With Constraints:
"Write an article about AI for a business blog. Requirements:
- Length: 1500-2000 words
- Tone: Professional, optimistic, practical
- Target audience: Business executives (non-technical)
- Must include: 3 real business examples, ROI discussion, common concerns
- Avoid: Technical jargon, complex math, academic tone
- Include: Clear call-to-action at end
- Format: 4-5 sections with clear headers"
(AI works within your parameters)
```

**Why it matters:**
- Prevents too-long or too-short outputs
- Maintains consistency
- Respects your constraints and needs

---

## Part 3: The Prompt Engineering Template

Use this structure for ANY prompt:

```
[YOUR ROLE/OBJECTIVE]
"I am a [your role]. I need to [specific goal]."

[WHAT YOU WANT (Detailed)]
"Please provide/write/generate [specific deliverable]. Include:
1. [Element/Section 1]
2. [Element/Section 2]
3. [Element/Section 3]"

[CONTEXT (If Needed)]
"Context: [relevant background information]
Note: [any important assumptions or details]"

[FORMAT & STRUCTURE]
"Format: [desired output format - code, table, essay, list, etc.]
Structure: [how to organize the information]"

[TONE & AUDIENCE]
"Tone: [professional/casual/technical/simple]
Audience: [who will read this, their expertise level]"

[EXAMPLES (If Helpful)]
"Example of what you mean: [provide 1-2 examples]"

[CONSTRAINTS]
"Constraints: [length limits, format limits, style requirements]"
```

---

## Part 4: Real-World Examples

### Example 1: Generate SQL Query

**Weak Prompt:**
```
"Write me a SQL query"
```

**Strong Prompt:**
```
ROLE:
"I'm a data analyst working with an e-commerce database."

OBJECTIVE:
"I need to identify our top customers by total spending in the last year."

CONTEXT:
"Database: PostgreSQL
Tables:
- customers (id, name, email, signup_date, country)
- orders (id, customer_id, order_date, amount, status)

We want: customers who spent >$500 in 2026"

WHAT I NEED:
"SQL query that returns:
1. Customer name
2. Total amount spent
3. Number of orders
4. Last order date
5. Customer since date

Sorted by: Total amount (highest first)"

FORMAT:
"Provide complete, runnable SQL code with comments
Add error handling for edge cases"

CONSTRAINT:
"Use standard SQL syntax compatible with PostgreSQL"
```

---

### Example 2: Generate Python Code

**Weak Prompt:**
```
"Write Python code for data cleaning"
```

**Strong Prompt:**
```
ROLE:
"I'm a data scientist preprocessing data for a machine learning model."

OBJECTIVE:
"I need to clean and prepare my dataset before modeling."

CONTEXT:
"Dataset: 'student_data.csv'
Columns: name, age, score, email, grade_level, attendance
Issues in data:
- Missing values in 'score' and 'email'
- Age has impossible values (negative, >150)
- Email format is inconsistent
- Duplicates exist based on (name, age)"

WHAT I NEED:
"Python code (using Pandas) that:
1. Reads the CSV file
2. Removes duplicates
3. Handles missing values:
   - Drop rows missing 'score'
   - Fill missing 'email' with 'unknown@email.com'
4. Removes age outliers (valid range: 5-100)
5. Standardizes email format (lowercase, no spaces)
6. Saves to 'clean_student_data.csv'"

FORMAT:
"Well-commented Python code
Include error handling
Show row counts at each step for verification"

CONSTRAINTS:
"Use only Pandas and NumPy
Make it production-ready
Include inline comments"
```

---

### Example 3: Create Power BI Dashboard Brief

**Weak Prompt:**
```
"Design a dashboard for sales"
```

**Strong Prompt:**
```
ROLE:
"I'm a sales manager who needs to track team performance."

OBJECTIVE:
"Design a Power BI dashboard for monitoring key sales metrics."

CONTEXT:
"Data source: Excel file with columns:
- Date, Sales Rep, Product, Revenue, Region, Customer Type
- Monthly data for 2026
- Team has 8 sales reps across 3 regions
- Using Power BI Desktop"

WHAT I NEED:
"Dashboard should include:

1. KPI Cards:
   - Total Revenue (vs target: $500K/month)
   - Number of Deals Closed
   - Average Deal Value
   
2. Visualizations:
   - Revenue trend (line chart, by month)
   - Top performers (bar chart)
   - Regional breakdown (pie chart)
   - Product sales (stacked bar chart)
   
3. Filters:
   - Date range selector
   - Region filter
   - Sales rep filter
   - Product filter"

AUDIENCE:
"Users: Sales managers (non-technical)
Update frequency: Weekly
Device: Desktop primarily"

RECOMMENDATIONS:
"Suggest color scheme, layout, and best practices for sales dashboards"

FORMAT:
"Provide:
1. Sketch/layout description
2. Data modeling suggestions
3. Recommended visualizations
4. Filter configuration"
```

---

### Example 4: Create Content (Blog/Script)

**Weak Prompt:**
```
"Write about artificial intelligence"
```

**Strong Prompt:**
```
ROLE:
"I'm creating content for a business blog."

OBJECTIVE:
"Write a comprehensive blog post on AI applications in business."

WHAT I NEED:
"5-article series (each 1500-2000 words):

Article 1: AI Basics for Business Leaders
- What is AI? (non-technical explanation)
- Why should companies care?
- Common misconceptions

Article 2: AI in Customer Service
- Real example: chatbots
- Real example: personalization
- ROI and implementation costs

Article 3: AI in Operations
- Real example: predictive maintenance
- Real example: supply chain optimization
- Cost savings potential

Article 4: AI in Marketing
- Real example: customer segmentation
- Real example: predictive analytics
- Revenue impact

Article 5: Getting Started with AI
- First steps for your company
- Common pitfalls to avoid
- ROI timeline
- Next resources"

TONE:
"Professional, business-focused, optimistic but realistic
No heavy technical jargon
Relatable examples"

AUDIENCE:
"Business executives, non-technical
Ages 35-60
Executive decision-makers"

STRUCTURE:
"Each article:
- Engaging introduction
- 2-3 real-world examples (with specific companies/results)
- Benefits and challenges
- Implementation considerations
- Call-to-action"

EXAMPLES:
"Business example style: 'Netflix uses AI to personalize 
recommendations, increasing watch time by 30%'"

CONSTRAINTS:
"Facts should be real and verifiable
Include no more than 1-2 metrics/percentages per article
End each with clear next steps
Encourage sharing and discussion"
```

---

## Part 5: Common Mistakes in Prompt Writing

### ❌ Mistake 1: Being Too Vague

```
❌ "Tell me about Python"
✅ "Explain 5 most important Python built-in functions 
    for data analysis (list, dict, pandas, numpy) with examples"
```

---

### ❌ Mistake 2: Assuming AI Knows Your Context

```
❌ "Fix my code"
   (AI doesn't know what code, what's wrong, what you want)
   
✅ "I'm trying to calculate average score from CSV data. 
    Getting 'KeyError: score' on line 5. 
    [paste code]. 
    What's wrong and how do I fix it?"
```

---

### ❌ Mistake 3: Not Specifying Format

```
❌ "Create a report"
   (Could be 1 page or 50 pages, could be text or table)
   
✅ "Create 2-page executive summary as PDF with:
    - Summary section (1 paragraph)
    - 3-4 key findings (bullet points)
    - 2-3 recommendations (numbered list)"
```

---

### ❌ Mistake 4: Forgetting Your Audience

```
❌ "Explain machine learning"
   (Could be too technical or too simple)
   
✅ "Explain machine learning to a 70-year-old non-technical 
    business owner. Use simple analogies. 
    Avoid jargon. Explain ROI in business terms."
```

---

### ❌ Mistake 5: No Examples

```
❌ "Classify customer feedback as positive or negative"
   (AI must guess what you mean by positive/negative)
   
✅ "Classify as positive or negative.
    Positive example: 'Great! Excellent service!'
    Negative example: 'Terrible. Will not buy again.'
    Now classify: [your list]"
```

---

## Part 6: The Iterative Refinement Process

Prompts are rarely perfect on the first try. **Refine based on results!**

```
Step 1: Write Initial Prompt
Input: "Analyze this dataset"
Output: Generic analysis
Quality: 4/10
Action: Too vague, add more specifics

Step 2: First Refinement
Input: "Analyze quarterly sales by region 
         for Q3 2026. Show top 5 regions"
Output: Better but too brief
Quality: 6/10
Action: Need recommendations too

Step 3: Second Refinement
Input: "Analyze Q3 2026 sales by region. 
         Show: top 5 regions, trends, 
         and 3 recommendations"
Output: Good quality report
Quality: 8/10
Action: Nearly perfect

Step 4: Final Refinement
Input: "Analyze Q3 2026 sales by region. 
         Show: top 5 regions, month-over-month trends, 
         outliers/anomalies, and 3 strategic recommendations.
         Format: Professional report for management"
Output: Excellent, actionable report
Quality: 9/10
Action: Ready to use!
```

**Key Points:**
- ✅ Iterating is normal
- ✅ Each refinement improves quality
- ✅ It's faster than manual work
- ✅ Results improve dramatically

---

## Part 7: Prompt Engineering Across Different Tools

### For ChatGPT/Claude (Text Generation)

```
Template:
"[ROLE] I need to [TASK].
Context: [BACKGROUND]
Requirements:
- [What it should include]
- [Format]
- [Tone]
- [Length/constraints]
Audience: [Who will read]"
```

### For DALL-E (Image Generation)

```
Template:
"Generate an image of [WHAT]:
Style: [artistic style - oil painting, photography, etc.]
Color palette: [colors]
Mood: [feeling it should convey]
Details: [specific elements to include]
Size: [dimensions if needed]"
```

### For Copilot/Code Assistants

```
Template:
"Language: [Python/JavaScript/SQL/etc.]
Task: [what the code should do]
Context: [database info, libraries, constraints]
Input: [what goes in]
Output: [what should come out]
Include: [comments, error handling, etc.]"
```

---

## Part 8: Advanced Techniques

### Chain-of-Thought Prompting

Ask AI to "think step-by-step"

```
❌ "What's the answer?"

✅ "Let me think through this step-by-step.
    First, I need to [step 1].
    Then, I should [step 2].
    Finally, I can [step 3].
    What's the answer?"
```

### Asking for Different Perspectives

```
"Give me three different approaches to solving this problem:
1. Quick and dirty (fast but maybe less elegant)
2. Best practice (takes longer but high quality)
3. Most efficient (balanced approach)

Then recommend which one I should use and why."
```

### Built-in Refinement

```
"Write [something]. 
Then review your answer and:
1. Identify any weaknesses
2. Improve the weak areas
3. Provide the final version"
```

---

## Part 9: Practice Exercises

### Exercise 1: Improve a Weak Prompt

**Given Weak Prompt:**
```
"Write code for my data"
```

**Your Task:**
Rewrite using the template from Part 3. Make it specific, detailed, and complete.

**Solution Should Include:**
- Your role
- Specific objective
- Data context (format, columns, issues)
- What output you need
- Format specification
- Any constraints

---

### Exercise 2: Create a Full Marketing Prompt

**Task:** Write a well-engineered prompt to create:
- LinkedIn post about your AI learning journey
- Target audience: professionals in data/tech
- Include 3 key learnings
- Call-to-action

**What to Include:**
- Role/context
- Specific requirements (length, tone, content)
- Audience definition
- Example of what you mean
- Output format

---

### Exercise 3: Compare Results

**Do This:**
1. Write a vague prompt
2. Get AI response
3. Note quality (rate 1-10)
4. Rewrite with all 6 elements
5. Get new AI response
6. Compare quality
7. Document what made the difference

---

## Quick Reference Checklist

Before hitting send on your prompt, check:

```
✓ Is it specific? (Not vague)
✓ Is it clear? (AI understands what you need)
✓ Have I provided context? (Background info)
✓ Is output format clear? (How should it be formatted)
✓ Is audience defined? (Who will use this)
✓ Are constraints clear? (Length, tone, etc.)
✓ Have I shown an example? (For complex tasks)
✓ Is it ready to execute? (Could AI do this with this prompt?)
```
---

*Prompt Engineering is not magic. It's a learnable skill that multiplies your productivity with AI.* 🚀
