# Agentic AI Techniques: Complete Reference Guide

> A comprehensive guide derived from Andrew Ng's Agentic AI course (M1-M5), covering all design patterns, implementation techniques, and best practices for building production-grade agentic workflows.

---

## Table of Contents

1. [Quick Reference: When to Use What](#1-quick-reference-when-to-use-what)
2. [Core Design Patterns](#2-core-design-patterns)
3. [Reflection Design Pattern (Deep Dive)](#3-reflection-design-pattern-deep-dive)
4. [Tool Use / Function Calling](#4-tool-use--function-calling)
5. [Planning Workflows](#5-planning-workflows)
6. [Multi-Agent Systems](#6-multi-agent-systems)
7. [Evaluations (Evals)](#7-evaluations-evals)
8. [Error Analysis Framework](#8-error-analysis-framework)
9. [Development Process](#9-development-process)
10. [Practical Examples](#10-practical-examples)
11. [Best Practices Summary](#11-best-practices-summary)

---

## 1. Quick Reference: When to Use What

### Decision Matrix: Choosing the Right Pattern

| Scenario | Recommended Pattern(s) | Why |
|----------|------------------------|-----|
| **Simple task, clear output** | Direct Generation (Zero-shot) | Fast, no overhead |
| **Code generation** | Reflection + Tool Use | Self-correct via execution errors |
| **Complex multi-step task** | Planning + Tool Use | Break down into manageable steps |
| **Need external data** | Tool Use (Web search, DB) | LLM can't know everything |
| **Quality improvement needed** | Reflection | Iterative refinement |
| **Multiple expertise areas** | Multi-Agent | Specialized agents per domain |
| **Customer service bot** | Planning + Tool Use + Reflection | Dynamic steps, external systems |
| **Research/writing** | Multi-Agent + Reflection | Research → Write → Review cycle |
| **Data extraction** | Tool Use + Evals | Structured output validation |
| **Visual tasks** | Multi-Agent + Tool Use | Different models for different modalities |

### Degrees of Autonomy

```
Less Autonomous ──────────────────────────────────► More Autonomous

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Predefined     │    │  Semi-          │    │  Highly         │
│  Steps          │    │  Autonomous     │    │  Autonomous     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • All steps     │    │ • Agent makes   │    │ • Agent makes   │
│   predetermined │    │   some decisions│    │   many decisions│
│ • All tool use  │    │ • All tools     │    │ • Can create    │
│   hard-coded    │    │   predefined    │    │   new tools     │
│ • Autonomy in   │    │                 │    │   on-the-fly    │
│   text only     │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Task Suitability Assessment

| Task Characteristic | Easier for Agentic AI | Harder for Agentic AI |
|---------------------|----------------------|----------------------|
| **Process** | Clear, step-by-step | Steps unknown ahead of time |
| **Procedures** | Standard to follow | Plan/solve as you go |
| **Assets** | Text only | Multimodal (sound, vision) |

---

## 2. Core Design Patterns

### The Four Pillars of Agentic AI

```
┌────────────────────────────────────────────────────────────────┐
│                    AGENTIC DESIGN PATTERNS                      │
├────────────────┬───────────────┬──────────────┬───────────────┤
│  REFLECTION    │   TOOL USE    │   PLANNING   │  MULTI-AGENT  │
├────────────────┼───────────────┼──────────────┼───────────────┤
│ Self-critique  │ External      │ Step-by-step │ Specialized   │
│ & improvement  │ capabilities  │ execution    │ collaboration │
└────────────────┴───────────────┴──────────────┴───────────────┘
```

### Pattern 1: Reflection

**Definition:** The LLM examines its own output and iteratively improves it.

**When to Use:**
- Code generation (catch syntax/logic errors)
- Writing tasks (improve clarity, tone)
- Any task where quality matters more than speed

**Key Insight:** Reflection consistently outperforms direct generation on variety of tasks.

### Pattern 2: Tool Use

**Definition:** Equipping agents with external tools (functions, APIs) to extend capabilities.

**When to Use:**
- Need current information (web search)
- Need to interact with databases
- Need to perform calculations
- Need to execute code

**Tool Categories:**
| Category | Examples |
|----------|----------|
| **Information Gathering** | Web search, Wikipedia, Database access |
| **Analysis** | Code execution, Wolfram Alpha |
| **Productivity** | Email, Calendar, Messaging |
| **Images** | Image generation, captioning, OCR |

### Pattern 3: Planning

**Definition:** Agent creates a step-by-step plan before execution.

**When to Use:**
- Complex tasks with multiple dependencies
- Tasks where steps aren't known ahead of time
- Customer service (dynamic query handling)

### Pattern 4: Multi-Agent Collaboration

**Definition:** Multiple specialized agents working together.

**When to Use:**
- Tasks requiring different expertise
- Research + Writing + Review workflows
- Tasks that would benefit from "team" approach

---

## 3. Reflection Design Pattern (Deep Dive)

### How Reflection Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    REFLECTION WORKFLOW                           │
│                                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │  Write   │───►│ Review/  │───►│ Reflect  │───►│ Improved │ │
│   │  Draft   │    │ Critique │    │ & Revise │    │  Output  │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                         │                              │        │
│                         └──────────────────────────────┘        │
│                           (Iterate if needed)                    │
└─────────────────────────────────────────────────────────────────┘
```

### Types of Reflection

#### 1. Self-Reflection (Same LLM)
```
Agent writes code → Agent reviews own code → Agent improves code
```

#### 2. Reflection with Different LLM
```
LLM 1 (Coder) writes code → LLM 2 (Reviewer) critiques → LLM 1 revises
```
*Tip: Use a reasoning model for reflection step*

#### 3. Reflection with External Feedback
```
LLM writes code → Execute code → Get errors → LLM fixes based on errors
```

**Example - Code Reflection:**
```
Step 1: Write first draft
        def do_task(args):
            ...

Step 2: Execute code
        SyntaxError: unterminated string literal (detected at line 1)

Step 3: Reflect and fix
        def do_task_v2(args):
            ...  # Fixed version
```

### Tips for Writing Reflection Prompts

| Element | Example |
|---------|---------|
| **Clearly indicate reflection action** | "Review the email first draft." |
| **Specify criteria to check** | "Check that the tone is professional and look for phrases that could be considered rude or insensitive." |
| **Verify facts** | "Verify all facts, dates, and promises are accurate." |
| **Define output format** | "Then write the next draft of the email." |

**Example Reflection Prompt for Email:**
```
Review the email first draft.
- Check that the tone is professional
- Look for phrases that could be considered rude or insensitive
- Verify all facts, dates, and promises are accurate
Then write the next draft of the email.
```

**Example Reflection Prompt for Domain Names:**
```
Review the domain names you suggested.
- Check if each name is easy to pronounce (word of mouth)
- Consider whether each name might mean something negative in other languages
Then output a shortlist of only the names that meet these criteria.
```

### External Feedback Tools for Reflection

| Challenge | Example | Source of Feedback |
|-----------|---------|-------------------|
| Mentioning competitors | "Our company's shoes are better than RivalCo" | Pattern matching for competitor names |
| Fact checking | "The Taj Mahal was built in 1648" | Web search results |
| Output length | Essay is over word limit | Word count tool |
| Code errors | SyntaxError, RuntimeError | Code execution output |

---

## 4. Tool Use / Function Calling

### What Are Tools?

Tools are just **code that the LLM can request to be executed**.

### Simple Tool Example

```python
from datetime import datetime

def get_current_time():
    """Returns the current time as a string"""
    return datetime.now().strftime("%H:%M:%S")
```

### Tool with Parameters

```python
from datetime import datetime
from zoneinfo import ZoneInfo

def get_current_time(timezone):
    """Returns current time for the given time zone"""
    timezone = ZoneInfo(timezone)
    return datetime.now(timezone).strftime("%H:%M:%S")
```

### How LLMs Use Tools

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL USE WORKFLOW                             │
│                                                                  │
│   User: "What time is it?"                                       │
│                     │                                            │
│                     ▼                                            │
│   ┌─────────────────────────────────┐                           │
│   │ LLM decides: Need current time  │                           │
│   │ Calls: get_current_time()       │                           │
│   └─────────────────────────────────┘                           │
│                     │                                            │
│                     ▼                                            │
│   Tool returns: "15:20:45"                                       │
│                     │                                            │
│                     ▼                                            │
│   LLM responds: "It's 3:20pm."                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Tool Selection: LLM Chooses When Appropriate

| Prompt | Tool Called | Output |
|--------|-------------|--------|
| "What time is it?" | `get_current_time()` | "It's 3:20pm." |
| "How much caffeine in green tea?" | *(None - uses training)* | "Green tea typically contains 25-50 mg..." |

### Tool Examples by Use Case

| Prompt | Tool | Output |
|--------|------|--------|
| "Find Italian restaurants near Mountain View, CA" | `web_search(query="restaurants near Mountain View, CA")` | "Spaghetti City is an Italian restaurant..." |
| "How much money after 10 years if I deposit $500 at 5% interest?" | `eval("500 * (1 + 0.05) ** 10")` | "$814.45" |
| "Show customers who bought white sunglasses" | `query_database(table="sales", product="sunglasses", color="white")` | "28 customers bought white sunglasses..." |

### Defining Tool Syntax

```python
import aisuite as ai
client = ai.Client()

response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=messages,
    tools=[get_current_time],  # Function automatically described to LLM
    max_turns=5
)
```

### Behind the Scenes: JSON Schema

The function's `name` and `description` (from docstring) are automatically converted to JSON Schema:

```json
{
    "name": "get_current_time",
    "description": "Returns the current time as a string",
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "The timezone to get the current time for"
            }
        },
        "required": ["timezone"]
    }
}
```

### Code Execution as a Tool

**Why use code execution?**
- LLMs are bad at math
- Code is precise and executable
- Can handle complex calculations

**Example:**
```
User: "What's the square root of 2?"

System Prompt: Write code to solve the user's query.
Return your answer as python code delimited with 
<execute_python> and </execute_python> tags.

LLM Output:
<execute_python>
import math
print(math.sqrt(2))
</execute_python>

Execution Result: 1.4142135623730951

LLM Response: "The square root of 2 is approximately 1.4142."
```

### Security Considerations

⚠️ **Running code outside of a sandbox can be risky**

**Best Practices:**
- Use sandboxed environments
- Limit file system access
- Restrict network access
- Set execution timeouts

### Model Context Protocol (MCP)

**Problem:** Each app creates their own tools → duplication, inconsistency

**Solution:** MCP provides standardized tool servers

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE                              │
│                                                                  │
│   Before MCP:                    With MCP:                       │
│   ┌─────┐ ┌─────┐ ┌─────┐       ┌─────┐ ┌─────┐ ┌─────┐        │
│   │App 1│ │App 2│ │App 3│       │App 1│ │App 2│ │App 3│        │
│   └──┬──┘ └──┬──┘ └──┬──┘       └──┬──┘ └──┬──┘ └──┬──┘        │
│      │       │       │             │       │       │            │
│   ┌──▼──┐ ┌──▼──┐ ┌──▼──┐       ┌──▼──────▼───────▼──┐         │
│   │Tools│ │Tools│ │Tools│       │   Shared MCP Server │         │
│   └─────┘ └─────┘ └─────┘       └─────────────────────┘         │
│                                                                  │
│   Each app creates              Each app uses shared             │
│   their own tools               MCP server                       │
└─────────────────────────────────────────────────────────────────┘
```

**Available MCP Servers:**
- Slack
- Google Drive
- GitHub
- PostgreSQL
- And many more...

---

## 5. Planning Workflows

### What is Planning?

Planning is when an agent **creates a step-by-step plan before execution**, then executes each step sequentially.

### Planning Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    PLANNING WORKFLOW                             │
│                                                                  │
│   User Query                                                     │
│      │                                                           │
│      ▼                                                           │
│   ┌──────────────────────────────────────┐                      │
│   │ System: You have access to tools:    │                      │
│   │ {tool_descriptions}                  │                      │
│   │ Return a step-by-step plan.          │                      │
│   └──────────────────────────────────────┘                      │
│      │                                                           │
│      ▼                                                           │
│   ┌──────────────────────────────────────┐                      │
│   │ LLM generates plan:                  │                      │
│   │ 1. Use tool_A to...                  │                      │
│   │ 2. Use tool_B to...                  │                      │
│   │ 3. Use tool_C to...                  │                      │
│   └──────────────────────────────────────┘                      │
│      │                                                           │
│      ▼                                                           │
│   Execute Step 1 → Execute Step 2 → Execute Step 3 → Output     │
└─────────────────────────────────────────────────────────────────┘
```

### Example: Customer Service Agent

**Database:**
| id | name | description | price | stock |
|----|------|-------------|-------|-------|
| 1001 | Aviator | Timeless pilot style, metal frame | 80 | 12 |
| 1002 | Catseye | Glamorous 1950s profile, plastic frame | 60 | 28 |
| 1003 | Moon | Oversized round style, plastic frame | 120 | 15 |
| 1004 | Classic | Classic round profile, gold frame | 60 | 9 |

**Query 1:** "Do you have any round sunglasses in stock that are under $100?"

**Plan Generated:**
```
1. Use get_item_descriptions tool to find round sunglasses
2. Use check_inventory to see if results are in stock
3. Use get_item_price to see if in-stock results are <$100
```

**Execution:**
```
Step 1: get_item_descriptions("round") → [Moon, Classic]
Step 2: check_inventory([Moon, Classic]) → Moon: 15, Classic: 9 (both in stock)
Step 3: get_item_price([Moon, Classic]) → Moon: $120, Classic: $60
Result: "Yes, we have our Classic sunglasses, a classic round metal frame for $60."
```

**Query 2:** "I would like to return the gold frame glasses I purchased, but not the metal frame ones."

**Plan Generated:**
```
1. Use check_past_transactions to find which glasses they bought
2. Use get_item_descriptions to find the gold frame glasses
3. Use process_item_return to return the gold-framed glasses
```

### Formatting Plans as JSON

For programmatic execution, format plans as structured JSON:

```json
{
    "plan": [
        {
            "step": 1,
            "action": "get_item_descriptions",
            "parameters": {"style": "round"}
        },
        {
            "step": 2,
            "action": "check_inventory",
            "parameters": {"items": "$step1_results"}
        },
        {
            "step": 3,
            "action": "get_item_price",
            "parameters": {"items": "$step2_instock"}
        }
    ]
}
```

### Planning with Code Execution

**Challenge with Tool-Based Planning:**
- Brittle (many edge cases)
- Inefficient (many tool calls)
- Continuously dealing with edge cases

**Solution: Planning with Code**

Instead of:
```
1. Use filter_rows for January Hot Chocolate
2. Use get_column_mean for January
3. Use filter_rows for February Hot Chocolate
4. Use get_column_mean for February
... (repeat for all 12 months)
```

Use code:
```python
df[df['coffee_name'] == 'Hot Chocolate'].groupby('month')['amount'].mean()
```

**Performance Improvement:**

| Model | Tool Actions | Code Actions |
|-------|--------------|--------------|
| GPT-4 | ~60% success | ~90% success |

*Adapted from "Executable Code actions Elicit Better LLM Agents", Wang et al. 2024*

---

## 6. Multi-Agent Systems

### Why Multi-Agent?

> "Some tasks require more than 1 person!" - Andrew Ng

### Example: Marketing Team

```
┌─────────────────────────────────────────────────────────────────┐
│                    MARKETING TEAM AGENTS                         │
│                                                                  │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│   │  RESEARCHER  │  │    WRITER    │  │   DESIGNER   │         │
│   ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│   │ Tasks:       │  │ Tasks:       │  │ Tasks:       │         │
│   │ • Analyze    │  │ • Transform  │  │ • Create     │         │
│   │   trends     │  │   research   │  │   visuals    │         │
│   │ • Research   │  │   into copy  │  │ • Generate   │         │
│   │   competitors│  │              │  │   artwork    │         │
│   ├──────────────┤  ├──────────────┤  ├──────────────┤         │
│   │ Tools:       │  │ Tools:       │  │ Tools:       │         │
│   │ • Web search │  │ • (None)     │  │ • Image gen  │         │
│   │              │  │              │  │ • Code exec  │         │
│   └──────────────┘  └──────────────┘  └──────────────┘         │
│          │                 │                 │                  │
│          └─────────────────┼─────────────────┘                  │
│                            ▼                                    │
│                    ┌──────────────┐                            │
│                    │ FINAL REPORT │                            │
│                    └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

### Communication Patterns

#### 1. Linear/Sequential
```
Agent A → Agent B → Agent C → Output

Example: Researcher → Writer → Editor
```

#### 2. Hierarchical
```
                    ┌──────────┐
                    │ Manager  │
                    └────┬─────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │ Agent A  │  │ Agent B  │  │ Agent C  │
    └──────────┘  └──────────┘  └──────────┘
```

#### 3. All-to-All (Debate)
```
    ┌──────────┐
    │ Agent A  │◄────────────┐
    └────┬─────┘             │
         │                   │
         ▼                   │
    ┌──────────┐             │
    │ Agent B  │◄────────────┤
    └────┬─────┘             │
         │                   │
         ▼                   │
    ┌──────────┐             │
    │ Agent C  │─────────────┘
    └──────────┘
```

### Multi-Agent Debate Results

| Task | Single Agent | Multi-Agent Debate |
|------|--------------|-------------------|
| Biographies | 66.0% | **73.8%** |
| MMLU | 63.9% | **71.1%** |
| Chess move | 29.3% | **45.2%** |

*From "Improving Factuality and Reasoning in Language Models through Multiagent Debate", Du et al., 2023*

### When to Use Multi-Agent

| Scenario | Recommended Pattern |
|----------|---------------------|
| Clear handoffs (Research → Write) | Linear |
| Complex project management | Hierarchical |
| Need consensus/diverse perspectives | All-to-All (Debate) |
| Different expertise required | Specialized Agents |

---

## 7. Evaluations (Evals)

### Why Evals Matter

> "You cannot improve what you cannot measure."

### Types of Evaluations

```
┌─────────────────────────────────────────────────────────────────┐
│                    EVALUATION TYPES                              │
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    END-TO-END EVALS                      │   │
│   │   Test the entire workflow from input to final output    │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                 COMPONENT-LEVEL EVALS                    │   │
│   │   Test individual components (web search, LLM step, etc) │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   ┌────────────────────────────┬────────────────────────────┐   │
│   │      OBJECTIVE EVALS       │     SUBJECTIVE EVALS       │   │
│   │   (Code-based checking)    │    (LLM-as-a-Judge)        │   │
│   ├────────────────────────────┼────────────────────────────┤   │
│   │ • Date extraction          │ • Essay quality            │   │
│   │ • Word count               │ • Chart clarity            │   │
│   │ • Competitor mentions      │ • Response tone            │   │
│   │ • Format compliance        │ • Content completeness     │   │
│   └────────────────────────────┴────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Creating an Eval: Step-by-Step

#### Example: Invoice Date Extraction

**Step 1: Create Ground Truth**
```
Manually extract due dates from 10-20 invoices
Invoice 1: "August 20, 2025" → Ground truth: "2025/08/20"
Invoice 2: "Sept 15, 2025" → Ground truth: "2025/09/15"
...
```

**Step 2: Specify Output Format in Prompt**
```
Format the due date as YYYY/MM/DD
```

**Step 3: Extract from LLM Response**
```python
import re

date_pattern = r'\d{4}/\d{2}/\d{2}'
extracted_date = re.findall(date_pattern, llm_response)

if extracted_date == actual_date:
    num_correct += 1
```

**Step 4: Track and Improve**
```
Run eval → Get score → Make changes → Re-run eval → Compare
```

### Objective vs Subjective Evals

| Type | When to Use | Example |
|------|-------------|---------|
| **Objective** | Clear right/wrong answer | Date extraction, word count, format |
| **Subjective** | Quality assessment needed | Essay quality, tone, creativity |

### LLM-as-a-Judge

**Problem with direct comparison:**
- Answers often not very good
- Position bias (LLM picks first option more often)

**Solution: Rubric-based grading**

```python
rubric = """
Assess the attached image against this quality rubric.
Each item should receive a score of 1 (true) or 0 (false).

1. Has clear title
2. Axis labels present
3. Appropriate chart type
4. Axes use appropriate numerical range
5. Legend is clear and readable

Return the scores as a JSON object.
"""
```

### Example: Research Agent Eval

**Problem:** Sometimes misses key points a human would make

**Solution:**
1. Choose 3-5 gold standard discussion points for each topic
2. Use LLM-as-judge to count how many points were mentioned
3. Get score for each prompt in eval set

**Prompt for LLM Judge:**
```
Determine how many of the 5 gold-standard talking points 
are present in the provided essay.

Original Prompt: {original_prompt}
Essay to Evaluate: {essay_text}
Gold Standard Talking Points: {gold_standard_points}

Return a JSON object with:
- score: number between 0 and 5
- explanation: list the talking points present
```

### Tips for Designing Evals

- ✅ Quick and dirty is ok to start!
- ✅ Improve metrics when they fail to capture human judgment
- ✅ Look for places where performance is worse than humans
- ✅ Use ~20 examples for initial evals
- ✅ Component-level evals are faster and more targeted

---

## 8. Error Analysis Framework

### The Error Analysis Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    ERROR ANALYSIS WORKFLOW                       │
│                                                                  │
│   1. IDENTIFY ERRORS                                             │
│      └── Look at outputs where performance is subpar            │
│                                                                  │
│   2. EXAMINE TRACES                                              │
│      └── Look at each step in the workflow                      │
│                                                                  │
│   3. CATEGORIZE ERRORS                                           │
│      └── Count which components fail most often                  │
│                                                                  │
│   4. PRIORITIZE FIXES                                            │
│      └── Focus on highest-impact improvements                   │
└─────────────────────────────────────────────────────────────────┘
```

### Example: Research Agent Error Analysis

**Workflow:**
```
Search web → Fetch 5 best sources → Write essay draft
```

**Observed Error:** Sometimes misses key points

**Possible Causes:**
- Bad search terms?
- Low quality search results?
- Poor selection of sources?
- Bad reasoning over texts?

**Error Count Table:**

| Prompt | Search terms | Search results | Picking sources | Reasoning |
|--------|--------------|----------------|-----------------|-----------|
| Black hole science | | Too many blog posts | | |
| Renting vs buying | | | Missed well-known blog | |
| Robotics harvesting | Terms too generic | Elementary school sites | | |
| EV batteries | | Only US companies | Missed magazine | |
| **Error Rate** | **5%** | **45%** | **10%** | **?** |

**Insight:** 45% of errors come from search results → Focus on improving search

### Example: Invoice Processing Error Analysis

**Workflow:**
```
PDF-to-text → LLM data extraction → Update database
```

**Error Count Table:**

| Input | PDF-to-text | LLM extraction |
|-------|-------------|----------------|
| Invoice 1 | Errors in extraction | |
| Invoice 2 | | Wrong date selected |
| Invoice 3 | | Wrong date selected |
| ... | ... | ... |
| Invoice 20 | Errors in extraction | Wrong date selected |

| Component | Error Rate |
|-----------|------------|
| PDF-to-text | 15% |
| LLM extraction | 87% |

**Insight:** LLM extraction is the problem → Focus on improving prompts

### Example: Customer Email Response Error Analysis

**Workflow:**
```
Extract key info → Query database → Draft response
```

| Input | LLM query | Database query | Drafted email |
|-------|-----------|----------------|---------------|
| Email 1 | Wrong table | | |
| Email 2 | | Error in DB entry | Didn't address details |
| Email 3 | Incorrect math | | |
| Email 50 | | | Defensive tone |

| Component | Error Rate |
|-----------|------------|
| LLM query | 75% |
| Database query | 4% |
| Drafted email | 30% |

**Insight:** LLM query generation is the main issue

### Tips for Error Analysis

- ✅ Develop a habit of looking at traces
- ✅ Carry out error analysis to find which component performed poorly
- ✅ Use error analysis output to decide where to focus efforts
- ✅ Select 10-100 examples where performance is subpar

---

## 9. Development Process

### The Build-Analyze-Improve Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT PROCESS                           │
│                                                                  │
│                        ┌─────────┐                              │
│                        │  BUILD  │                              │
│                        └────┬────┘                              │
│                             │                                    │
│                             ▼                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              Build end-to-end system                     │   │
│   └─────────────────────────────────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│                        ┌─────────┐                              │
│                        │ ANALYZE │                              │
│                        └────┬────┘                              │
│                             │                                    │
│                             ▼                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │   • Examine outputs and traces                           │   │
│   │   • Build evals; compute metrics                         │   │
│   │   • Error analysis                                       │   │
│   │   • Component-level evals                                │   │
│   └─────────────────────────────────────────────────────────┘   │
│                             │                                    │
│                             ▼                                    │
│                        ┌─────────┐                              │
│                        │IMPROVE  │                              │
│                        └────┬────┘                              │
│                             │                                    │
│                             ▼                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │   Improve individual components                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                             │                                    │
│                             └────────────► (Back to ANALYZE)    │
└─────────────────────────────────────────────────────────────────┘
```

### Driving Development with Evals

1. **Build a system** and look at outputs to discover unsatisfactory behavior
   - E.g., incorrect due dates in invoice extraction

2. **Put in place a small eval** with ~20 examples to track progress

3. **Monitor as you make changes** (new prompts, new algorithms)

4. **See if the metric improves**

### Improving Non-LLM Components

| Component | Improvement Options |
|-----------|---------------------|
| **Web search** | Tune: number of results, date range. Replace: try different search engine |
| **RAG** | Tune: similarity threshold, chunk size. Replace: different RAG provider |
| **ML models** | Tune: detection threshold. Replace: different model |
| **Code execution** | Tune: timeout, memory limits. Replace: different sandbox |

### Improving LLM Components

| Technique | Description |
|-----------|-------------|
| **Improve prompts** | Add explicit instructions, add examples (few-shot) |
| **Try new model** | Test multiple LLMs, use evals to pick best |
| **Split up steps** | Decompose task into smaller steps |
| **Fine-tune** | Train on internal data for specific tasks |

### Model Selection Tips

- Play with models often to develop intuition
- Have a personal set of evals for comparison
- Read other people's prompts for ideas
- Use different models for different tasks
- `aisuite` makes it easy to swap models

### Latency and Cost Optimization

**Example: Research Agent Timing**

```
Search web: 7s
Fetch sources: 5s
Process: 3s
Write draft: 11s
Total: 18s
```

**Optimization Options:**
- Parallelize where possible
- Use smaller/faster models for simple steps
- Use faster LLM providers

**Cost Tracking:**

| Step | Cost Type | Amount |
|------|-----------|--------|
| Web search | API call | $0.016 |
| Fetch sources | API call | $0.002 |
| PDF-to-text | Compute | $0.03 |
| LLM steps | Tokens | $0.0004 each |

---

## 10. Practical Examples

### Example 1: Essay Writing Workflow

**Zero-shot (Non-agentic):**
```
Prompt: "Write an essay on topic X"
Output: [Single-pass essay - often low quality]
```

**Agentic Workflow:**
```
Step 1: Write an essay outline on topic X
Step 2: Do you need any web research? → If yes, search web
Step 3: Write a first draft
Step 4: Consider what parts need revision or more research
Step 5: Revise your draft
Step 6: Request human review (optional)
```

**With Parallelization:**
```
        ┌── web search 1 ──┐
        │                   │
┌───┐   ├── web search 2 ──┼───┐    ┌─────────┐
│LLM│──►├── web search 3 ──┼───┼───►│ Write   │
└───┘   ├── web fetch 1 ──┼───┤    │ essay   │
        ├── web fetch 2 ──┤   │    └─────────┘
        │                   │
        └── web fetch N ──┘

9 parallel operations → Much faster!
```

### Example 2: Customer Service Agent

**Tools Available:**
- `process_item_sale`
- `get_item_descriptions`
- `check_inventory`
- `check_past_transactions`
- `process_item_return`
- `get_item_price`

**Query:** "Do you have any round sunglasses in stock under $100?"

**Execution:**
```
1. get_item_descriptions("round") → [Moon, Classic]
2. check_inventory([Moon, Classic]) → Both in stock
3. get_item_price([Moon, Classic]) → Moon: $120, Classic: $60
4. Response: "Yes, Classic sunglasses, round metal frame, $60"
```

### Example 3: Chart Generation with Reflection

**Workflow:**
```
User: "Create a plot comparing Q1 coffee sales in 2024 and 2025"

Step 1: LLM generates code
        import matplotlib.pyplot as plt
        import pandas as pd
        q1_sales = df[df['quarter'] == 1]
        ...

Step 2: Execute code → plot.png

Step 3: LLM 2 (Reviewer) critiques
        "Chart missing title, axis labels unclear..."

Step 4: LLM 1 generates improved code

Step 5: Execute → plot_v2.png (better!)
```

### Example 4: Invoice Processing

**Required Fields:**
- Biller
- Biller address
- Amount due
- Due date

**Workflow:**
```
PDF Invoice → PDF-to-text → LLM extraction → Update database
```

**Eval Setup:**
```
1. Manually extract due dates from 20 invoices
2. Specify format: YYYY/MM/DD
3. Extract date from LLM response using regex
4. Compare to ground truth
5. Track: num_correct / total
```

### Example 5: Email Response Agent

**Input:**
```
From: sjones9@email.com
Subject: Wrong item shipped

I ordered a blue KitchenPro blender (Order #8847) but 
received a red toaster instead. I need the blender for 
my daughter's birthday party this weekend. Can you help?

Susan Jones
```

**Workflow:**
```
Step 1: Extract key information
        - Name: Susan Jones
        - Email: sjones9@email.com
        - Order #: 8847
        - Issue: Wrong item (received toaster, ordered blender)

Step 2: Query orders database
        - Verify order details

Step 3: Draft response for human review
```

---

## 11. Best Practices Summary

### The 4 Must-Implement Patterns for Production

```
┌─────────────────────────────────────────────────────────────────┐
│           PRODUCTION AGENTIC SYSTEM REQUIREMENTS                 │
│                                                                  │
│   1. ROBUST TOOL USE                                            │
│      • Standardize tool schemas                                  │
│      • Provide comprehensive docstrings                          │
│      • Use typed arguments                                       │
│                                                                  │
│   2. PLANNING WITH MEMORY                                        │
│      • Implement orchestrator pattern (ReAct or state graph)    │
│      • Formulate step-by-step plans dynamically                 │
│      • Track execution state                                     │
│                                                                  │
│   3. REFLECTION / SELF-CORRECTION                               │
│      • Implement feedback loops                                  │
│      • Feed execution errors back to LLM                         │
│      • Allow strategy revision                                   │
│                                                                  │
│   4. SYSTEMATIC EVALUATIONS                                      │
│      • Set up test suite with real-world edge cases             │
│      • Define input-output pairs with assertions                │
│      • Validate reasoning traces                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Checklist

#### Before Building
- [ ] Can the task be decomposed into steps?
- [ ] What tools are needed?
- [ ] What does success look like? (Define evals early)
- [ ] Is this suited for agentic AI?

#### During Building
- [ ] Start with end-to-end system
- [ ] Add evals early
- [ ] Examine traces regularly
- [ ] Iterate on components

#### After Building
- [ ] Run comprehensive evals
- [ ] Perform error analysis
- [ ] Optimize latency/cost
- [ ] Set up monitoring

### Key Takeaways by Module

| Module | Key Insight |
|--------|-------------|
| **M1** | Agentic workflows outperform zero-shot by iterating |
| **M2** | Reflection enables self-improvement |
| **M3** | Tools extend LLM capabilities beyond training data |
| **M4** | Evals drive improvement; analyze traces to debug |
| **M5** | Planning and multi-agent enable complex tasks |

### Common Pitfalls to Avoid

| Pitfall | Solution |
|---------|----------|
| No evals | Build evals from day 1 |
| Only end-to-end testing | Add component-level evals |
| Ignoring traces | Examine traces for every error |
| Over-engineering | Start simple, iterate |
| No reflection | Add self-correction loops |
| Monolithic agents | Consider multi-agent for complex tasks |

---

## Appendix: Code Templates

### Basic Tool Definition

```python
from datetime import datetime

def get_current_time(timezone: str = "UTC") -> str:
    """
    Returns the current time for a given timezone.
    
    Args:
        timezone: The timezone string (e.g., 'America/New_York')
    
    Returns:
        The current time as a string in HH:MM:SS format
    """
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(timezone)
    return datetime.now(tz).strftime("%H:%M:%S")
```

### Tool Integration with aisuite

```python
import aisuite as ai

client = ai.Client()

response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=messages,
    tools=[get_current_time, web_search, query_database],
    max_turns=5
)
```

### Reflection Prompt Template

```python
REFLECTION_PROMPT = """
Review the following {content_type}:

{content}

Check for:
1. {criteria_1}
2. {criteria_2}
3. {criteria_3}

Then provide an improved version.
"""
```

### Eval Template

```python
def run_eval(test_cases, agent_func):
    results = []
    for case in test_cases:
        output = agent_func(case["input"])
        score = evaluate_output(output, case["ground_truth"])
        results.append({
            "input": case["input"],
            "output": output,
            "expected": case["ground_truth"],
            "score": score
        })
    return sum(r["score"] for r in results) / len(results)
```

---

*This guide is derived from Andrew Ng's Agentic AI course (M1-M5). For implementation, refer to the specific module materials and adapt patterns to your use case.*