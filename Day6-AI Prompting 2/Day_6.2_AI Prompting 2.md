# Day 6: Chain of Thoughts (CoT) - Advanced Prompting Technique

**Author:** Saurabh Shirgaokar  
**Date:** September 24, 2026  
**Topic:** Chain of Thoughts Prompting  
**Level:** Intermediate

---

## 🎯 Day 6 Overview

Today you learned **Chain of Thoughts (CoT)** - a revolutionary prompting technique that makes AI reason through problems step-by-step before answering.

**Why it matters:**
```
Without CoT: AI gives answer directly (often wrong)
With CoT:    AI shows reasoning, then answer (much more accurate)

Accuracy improvement: 10-40% depending on task complexity
```

---

## Part 1: What is Chain of Thoughts?

### 1.1 Core Concept

**Chain of Thoughts** = Asking AI to show its thinking process

```
Traditional:
Question → AI → Answer
(No reasoning shown, answer might be wrong)

Chain of Thoughts:
Question → AI thinks step-by-step → Shows reasoning → Answer
(Reasoning visible, answer more accurate)
```

### 1.2 Why CoT Works

AI reasoning process:
```
Step 1: Understand the problem
Step 2: Break into sub-problems  
Step 3: Solve each sub-problem
Step 4: Combine solutions
Step 5: Verify answer

Without CoT: Skips to answer (risky)
With CoT: Shows all steps (reliable)
```

---

## Part 2: Two Types of Chain of Thoughts

### 2.1 Zero-Shot CoT

**Definition:** Ask AI to reason WITHOUT providing examples

**How it works:**
```
Prompt Structure:
1. Present problem
2. Explicitly ask to think step-by-step
3. Tell model: "Let's think step by step"
4. AI reasons through problem
5. AI provides answer with reasoning
```

**Key Phrase:** "Let's think step by step" or "Think step-by-step"

**Example 1: Math Problem**

```
Prompt (WITHOUT CoT):
"If a train travels at 60 mph for 2.5 hours, how far does it go?"

AI Response (Direct):
"150 miles"
(No reasoning shown, hard to verify)

---

Prompt (WITH Zero-Shot CoT):
"If a train travels at 60 mph for 2.5 hours, how far does it go?
Let's think step by step."

AI Response (With Reasoning):
"Let me break this down:
Step 1: Identify what we know
  - Speed: 60 mph
  - Time: 2.5 hours
  - Need to find: Distance

Step 2: Use the formula
  - Distance = Speed × Time
  - Distance = 60 × 2.5

Step 3: Calculate
  - 60 × 2.5 = 150 miles

Answer: The train travels 150 miles"
(Reasoning visible, easy to verify)
```

### 2.2 Few-Shot CoT

**Definition:** Provide examples WITH reasoning, then ask for answer

**How it works:**
```
1. Show example 1 (problem + step-by-step solution)
2. Show example 2 (problem + step-by-step solution)
3. Ask the actual question
4. AI follows the pattern and reasons through
5. AI provides answer with similar step-by-step breakdown
```

**Key Difference from Zero-Shot:**
```
Zero-Shot: No examples, just ask to think step-by-step
Few-Shot:  Show examples, then AI follows the pattern
```

**Example 2: Few-Shot CoT**

```
Prompt (Few-Shot CoT):
"Here are two examples of problem-solving:

Example 1:
Q: If John has 3 apples and buys 5 more, how many does he have?
A: Let's think step by step.
  Step 1: John starts with 3 apples
  Step 2: He buys 5 more apples
  Step 3: Total = 3 + 5 = 8 apples
  Answer: 8 apples

Example 2:
Q: If a book costs $12 and you buy 3 books with a 10% discount, 
   how much do you spend?
A: Let's think step by step.
  Step 1: Original price per book = $12
  Step 2: Number of books = 3
  Step 3: Total before discount = 12 × 3 = $36
  Step 4: Discount amount = 10% of $36 = $3.60
  Step 5: Total after discount = $36 - $3.60 = $32.40
  Answer: $32.40

Now solve this:
Q: Sarah earns $15/hour and works 8 hours/day for 5 days. 
   If she saves 20% of her earnings, how much does she save?"

AI Response (Following Pattern):
"Let me think step by step.
  Step 1: Hourly rate = $15
  Step 2: Hours per day = 8
  Step 3: Daily earnings = $15 × 8 = $120
  Step 4: Days worked = 5
  Step 5: Total earnings = $120 × 5 = $600
  Step 6: Savings percentage = 20%
  Step 7: Amount saved = 20% of $600 = $120
  Answer: Sarah saves $120"
```

---

## Part 3: When to Use CoT

### 3.1 Best Use Cases

**Use CoT for:**
```
✓ Complex reasoning problems
✓ Multi-step calculations
✓ Logic and deduction
✓ Analysis and synthesis
✓ Novel problem-solving
✓ Critical thinking tasks

Example domains:
- Math and physics
- Data analysis
- Business decision-making
- Research and writing
- Code debugging
```

**Don't need CoT for:**
```
✓ Simple factual recall
✓ Basic definitions
✓ Information lookup
✓ Direct answers

Example:
Q: What is the capital of France?
A: Paris (No reasoning needed)
```

---

## Part 4: Practical Implementation Examples

### Example 1: Business Decision Problem

**Without CoT:**
```
Prompt: "Should we expand to a new market?"

AI Response: "Yes, you should expand. It offers growth opportunities."
(No reasoning, not convincing)
```

**With Zero-Shot CoT:**
```
Prompt: "Should we expand to a new market? 
Let's think step by step about this decision."

AI Response:
"Let me analyze this systematically.

Step 1: Identify key factors
  - Market size and growth potential
  - Competition level
  - Our resources and capabilities
  - Financial requirements
  - Risk factors

Step 2: Analyze market opportunity
  - New market size: $50M annually
  - Growth rate: 15% year-over-year
  - Current market penetration: Low

Step 3: Assess our capabilities
  - Existing customer base: Strong
  - Brand recognition: Moderate
  - Financial reserves: Sufficient for expansion
  - Team expertise: Relevant to new market

Step 4: Evaluate risks
  - Competition: High but fragmented
  - Regulatory: Standard, manageable
  - Execution risk: Moderate with proper planning

Step 5: Compare alternatives
  - Option A: Expand (higher risk, higher reward)
  - Option B: Stay put (safe, limited growth)
  - Option C: Slow expansion (balanced risk/reward)

Recommendation: Expand gradually (Option C) to balance opportunity with risk.
Reasoning: Large market with manageable competition, but requires careful 
execution given our current resources."
```

### Example 2: Data Analysis Problem

**Without CoT:**
```
Prompt: "Analyze this customer retention data and identify trends"

AI Response: "Retention is declining. Focus on customer service."
(Shallow analysis)
```

**With Few-Shot CoT:**
```
Prompt:
"Here's how to analyze retention data:

Example 1:
Q: Q1 retention was 85%, Q2 was 82%, Q3 was 80%. What's the trend?
A: Step by step:
  Step 1: List the values: 85%, 82%, 80%
  Step 2: Calculate decline per quarter: 3%, 2%
  Step 3: Identify pattern: Steady decline, accelerating
  Step 4: Calculate projected Q4: ~77%
  Step 5: Root cause analysis needed: Why declining?
  Conclusion: Negative trend requiring investigation

Now analyze: Our retention Q1-Q3 was 90%, 88%, 85%. 
What's happening and what should we do?"

AI Response:
"Let me analyze systematically:
  Step 1: List the values: 90%, 88%, 85%
  Step 2: Calculate decline: 2% per quarter (consistent)
  Step 3: Pattern: Steady decline, predictable
  Step 4: Projected Q4: ~83%
  Step 5: Implications: Loss of 7% of customers per year
  Step 6: Annual revenue impact: If avg customer = $1000, 
          losing 70 customers/quarter = $70k loss
  
Actions to take:
  1. Interview churning customers (find reasons)
  2. Improve onboarding (reduce early churn)
  3. Add loyalty program (increase retention)
  4. Monitor weekly metrics (catch problems early)"
```

### Example 3: Code Debugging

**Without CoT:**
```
Prompt: "Why does this code fail?"

Code:
```python
data = [1, 2, 3]
result = data[5]
```

AI Response: "IndexError: You're accessing an index that doesn't exist."
(Correct but surface-level)
```

**With CoT:**
```
Prompt: "Why does this code fail? Think through it step by step."

Code:
```python
data = [1, 2, 3]
result = data[5]
```

AI Response:
"Let me trace through this code step by step:

Step 1: List creation
  - data = [1, 2, 3]
  - List has 3 elements with indices: 0, 1, 2

Step 2: Index analysis
  - Trying to access: data[5]
  - Valid indices: 0, 1, 2
  - Requested index: 5

Step 3: Check bounds
  - Max valid index = length - 1 = 3 - 1 = 2
  - Requested index 5 > max valid index 2
  - INDEX OUT OF BOUNDS!

Step 4: Error type
  - Python raises: IndexError
  - Message: 'list index out of range'

Step 5: Solution
  - Option 1: Change to data[2] (last element)
  - Option 2: Check list length: data[min(5, len(data)-1)]
  - Option 3: Use try-except for safety

Root Cause: Accessing array index beyond list bounds
Prevention: Always check len(data) before accessing data[i]"
```

### Example 4: Research and Writing Problem

**Without CoT:**
```
Prompt: "Write an analysis of AI impact on jobs"

AI Response: "AI will change jobs. Some jobs disappear, new jobs appear. 
Workers need retraining."
(Generic, lacks depth)
```

**With Zero-Shot CoT:**
```
Prompt: "Analyze AI's impact on job market. 
Let's think through this systematically."

AI Response:
"Let me analyze this comprehensively:

Step 1: Define the scope
  - Which jobs affected? Which sectors?
  - What timeframe? (5 years, 10 years, 20 years)
  - Which AI technologies? (LLMs, computer vision, etc.)

Step 2: Jobs at risk (automation potential)
  - High risk: Data entry, customer service, basic coding
  - Medium risk: Accounting, legal research, content creation
  - Low risk: Creative, complex interpersonal, physical jobs

Step 3: Job displacement timeline
  - 2024-2026: Early stage (10-15% job market affected)
  - 2026-2030: Growth phase (25-30% affected)
  - 2030+: Mature phase (depends on policy)

Step 4: New job creation
  - AI trainers and evaluators
  - AI maintenance and oversight
  - Jobs requiring human touch (therapy, management, art)
  - New roles we can't predict yet

Step 5: Economic impact analysis
  - Productivity gains: 20-40% in affected sectors
  - Wage pressures: Downward for routine tasks, upward for rare skills
  - Income inequality: May increase without intervention

Step 6: Policy considerations
  - Reskilling programs needed
  - Social safety net adjustments
  - Tax/benefit system changes
  - Education curriculum updates

Conclusion: Significant job market transformation expected. 
Net job loss likely in short term, but new opportunities will emerge. 
Policy response critical for managing transition."
```

---

## Part 5: CoT Best Practices

### 5.1 How to Write Effective CoT Prompts

**Template for Zero-Shot CoT:**

```
"[Problem Statement]

Let's think through this step by step:
Step 1: [Break down the problem]
Step 2: [Identify key components]
Step 3: [Solve each component]
Step 4: [Combine solutions]
Step 5: [Verify the answer]"
```

**Template for Few-Shot CoT:**

```
"Here's an example of step-by-step thinking:

Example:
Q: [Similar problem]
A: Step 1: [reasoning]
   Step 2: [reasoning]
   Step 3: [reasoning]
   Answer: [result]

Now solve this:
Q: [Your actual problem]"
```

### 5.2 Tips for Better Results

```
✓ Be explicit: "Let's think step by step"
✓ Number the steps: "Step 1", "Step 2", etc.
✓ Show reasoning: Not just answers
✓ Verify each step: Check logic
✓ For few-shot: Use similar problems as examples
✓ For complex problems: Use few-shot (better than zero-shot)
✓ Test both: See which works better for your use case
```

---

## Part 6: Common Mistakes

### ❌ Mistake 1: Expecting CoT for Simple Queries

```
❌ "What's the capital of France? Let's think step by step."
(Overkill, doesn't help)

✓ "What's the capital of France?" (Direct answer fine)
```

---

### ❌ Mistake 2: Poor Step Numbering in Few-Shot

```
❌ "Here's how to solve:
   First, do this. Then, do that. Finally, do this."
(Unclear, hard to follow)

✓ "Step 1: ...
   Step 2: ...
   Step 3: ..."
(Clear, structured)
```

---

### ❌ Mistake 3: Not Showing Reasoning in Few-Shot Examples

```
❌ Example:
   Q: 5 + 3 × 2 = ?
   A: 11

(No reasoning shown, AI can't learn pattern)

✓ Example:
   Q: 5 + 3 × 2 = ?
   A: Step 1: Order of operations (PEMDAS)
      Step 2: Multiply first: 3 × 2 = 6
      Step 3: Then add: 5 + 6 = 11
      Answer: 11

(Reasoning clear, AI learns pattern)
```

---

## Part 7: When to Use Which Type

### CoT Type Comparison

| Aspect | Zero-Shot CoT | Few-Shot CoT |
|--------|--------------|--------------|
| **Effort** | Minimal | More setup |
| **When to use** | Simple reasoning | Complex problems |
| **Accuracy** | Good (70-80%) | Better (80-90%) |
| **Learning curve** | Immediate | Model learns from examples |
| **Best for** | Quick answers | Critical decisions |

---

## Part 8: Impact & Results

### Quality Improvement with CoT

```
Without CoT (Direct answers):
- Accuracy: 60-70% for complex problems
- Reasoning visible: No
- Verifiable: Difficult

With Zero-Shot CoT:
- Accuracy: 75-85% for complex problems
- Reasoning visible: Yes
- Verifiable: Easy (+20% accuracy)

With Few-Shot CoT:
- Accuracy: 85-95% for complex problems
- Reasoning visible: Yes
- Verifiable: Easy (+30% accuracy)
```

---

## Part 9: Quick Reference

### Zero-Shot CoT Prompt

```
[Your Question]

Let's think step by step.
```

### Few-Shot CoT Prompt

```
Example 1:
Q: [Similar problem]
A: Step 1: [solution]
   Step 2: [solution]
   Answer: [result]

Example 2:
Q: [Another similar problem]
A: Step 1: [solution]
   Step 2: [solution]
   Answer: [result]

Now solve this:
Q: [Your problem]
```

---

## Part 10: Key Takeaways

✅ **CoT makes AI reason step-by-step** instead of jumping to answers  
✅ **Zero-Shot CoT:** No examples, just ask to think step-by-step  
✅ **Few-Shot CoT:** Provide examples of step-by-step thinking  
✅ **Use for complex problems:** Math, analysis, decision-making  
✅ **Improves accuracy:** 20-30% improvement typical  
✅ **Makes thinking visible:** Easy to verify and correct  

---

## Part 11: Summary Table

| Scenario | Technique | Example Prompt |
|----------|-----------|-----------------|
| Math problem | Zero-Shot CoT | "Solve this. Let's think step by step" |
| Analysis | Few-Shot CoT | Show examples, then ask |
| Decision making | Zero-Shot CoT | "Should we...? Think step by step" |
| Debugging | Zero-Shot CoT | "Why fails? Walk through code step by step" |
| Research writing | Zero-Shot CoT | "Analyze... Let's think systematically" |

---

## Part 12: Next Steps

**This Week:**
- [ ] Practice zero-shot CoT on math problems
- [ ] Try few-shot CoT with examples
- [ ] Compare results with/without CoT
- [ ] Measure accuracy improvement

**Next Week:**
- [ ] Combine CoT with prompt engineering principles
- [ ] Use CoT in agents and automation
- [ ] Create CoT templates for your workflows

---

*Chain of Thoughts transforms AI from a guesser into a reasoner. Master this technique and dramatically improve AI output quality.* 🚀
