# Agentic AI: From Theory to Production

> **Complete Agentic AI Mastery Guide** - From design patterns to production-grade systems.  
> Learn reflection, planning, multi-agent orchestration, evals, and deploy reliable agents that actually work in industry.

[![Last Updated](https://img.shields.io/badge/Updated-March%202026-blue.svg)]()
[![Stars](https://img.shields.io/github/stars/B-Bharath-Reddy/Agentic-AI?style=social)](https://github.com/B-Bharath-Reddy/Agentic-AI)

---

## Who This Is For

| Level | Description |
|-------|-------------|
| **Beginner** | Just heard about Agentic AI? Start with the [Quick Start](#quick-start-code) |
| **Developer** | Building your first agent? Follow the [30-min path](#how-to-use-this-guide) |
| **Production Engineer** | Deploying at scale? Jump to [Production Guide](#production-deployment--scaling) |

**Prerequisites:** Python basics + LLM API knowledge (OpenAI, Anthropic, etc.)

---

## How to Use This Guide

### 30-Minute Quick Start Path
1. Read [Core Design Patterns](#core-design-patterns-overview) (10 min)
2. Run [01-reflection-agent.py](examples/01-reflection-agent.py) (5 min)
3. Skim [Best Practices](agentic_ai_techniques_guide.md#11-best-practices-summary) (5 min)
4. Check [Production Checklist](production-checklist.md) (10 min)

### Full Deep-Dive Path
1. Read the complete [Agentic AI Techniques Guide](agentic_ai_techniques_guide.md) (2-3 hours)
2. Work through all [examples](examples/) (4-6 hours)
3. Build your own agent using [production template](examples/04-production-template/) (2-4 hours)

---

## What You Will Be Able to Build

After completing this guide, you'll have the skills to build:

| Project | Description | Complexity |
|---------|-------------|------------|
| **Customer Support Agent** | Multi-turn conversations with tool use, 87% resolution rate | Intermediate |
| **Research Analyst Agent** | Web search, synthesis, report generation | Intermediate |
| **Internal IT Ticket Agent** | Auto-triage, resolve, escalate with human-in-the-loop | Advanced |

---

## Quick Start Code

```python
# Install: pip install aisuite langgraph

from datetime import datetime

def get_current_time():
    """Returns current time - a simple tool example"""
    return datetime.now().strftime("%H:%M:%S")

# Your first agentic tool call
import aisuite as ai
client = ai.Client()

response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=[{"role": "user", "content": "What time is it?"}],
    tools=[get_current_time],
    max_turns=5
)
print(response.choices[0].message.content)
```

---

## Table of Contents

### Core Guide
- [Full 11-Section Reference Guide](agentic_ai_techniques_guide.md)
- [Production Checklist](production-checklist.md)

### Topics Covered
| Topic | Section | Status |
|-------|---------|--------|
| Reflection Pattern | [Guide Section 3](agentic_ai_techniques_guide.md#3-reflection-design-pattern-deep-dive) | Complete |
| Tool Use | [Guide Section 4](agentic_ai_techniques_guide.md#4-tool-use--function-calling) | Complete |
| Planning Workflows | [Guide Section 5](agentic_ai_techniques_guide.md#5-planning-workflows) | Complete |
| Multi-Agent Systems | [Guide Section 6](agentic_ai_techniques_guide.md#6-multi-agent-systems) | Complete |
| Evaluations | [Guide Section 7](agentic_ai_techniques_guide.md#7-evaluations-evals) | Complete |
| Error Analysis | [Guide Section 8](agentic_ai_techniques_guide.md#8-error-analysis-framework) | Complete |
| Production Deployment | [Below](#production-deployment--scaling) | Complete |
| Observability | [Below](#observability--monitoring) | Complete |
| Security & Guardrails | [Below](#security-guardrails--reliability) | Complete |
| Cost Optimization | [Below](#cost-optimization--performance) | Complete |

---

## Core Design Patterns Overview

```
The 4 Pillars of Agentic AI:

+-------------------+     +-------------------+
|   REFLECTION      |     |    TOOL USE       |
| Self-critique &   | --> | External          |
| improvement       |     | capabilities      |
+-------------------+     +-------------------+
         |                        |
         v                        v
+-------------------+     +-------------------+
|   PLANNING        |     |   MULTI-AGENT     |
| Step-by-step      | <-- | Specialized       |
| execution         |     | collaboration     |
+-------------------+     +-------------------+
```

### Quick Decision Matrix

| Your Task | Use This Pattern |
|-----------|-----------------|
| Code generation | Reflection + Tool Use |
| Complex multi-step | Planning + Tool Use |
| Need external data | Tool Use (Web search, DB) |
| Quality improvement | Reflection |
| Multiple expertise | Multi-Agent |
| Customer service | Planning + Tool Use + Reflection |

---

## Production Deployment & Scaling

### FastAPI + LangGraph Server

```python
# server.py - Production-ready agent server
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

app = FastAPI(title="Agentic AI API")

class AgentRequest(BaseModel):
    message: str
    session_id: str = None

# Create agent with memory
memory = MemorySaver()
agent = create_react_agent(
    model="gpt-4o",
    tools=[get_current_time, web_search, query_database],
    checkpointer=memory
)

@app.post("/agent/invoke")
async def invoke_agent(request: AgentRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    result = await agent.ainvoke(
        {"messages": [("user", request.message)]},
        config=config
    )
    return {"response": result["messages"][-1].content}
```

### Docker + Multi-Container Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - redis
      - postgres
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: agent_memory
      POSTGRES_PASSWORD: ${DB_PASSWORD}
```

### Serverless Options

| Platform | Best For | Cold Start | Cost |
|----------|----------|------------|------|
| **Vercel** | Quick deploy, edge | ~100ms | $0-20/mo |
| **Cloud Run** | Container workloads | ~500ms | $0-50/mo |
| **Modal** | GPU/ML workloads | ~1s | Pay-per-use |
| **AWS Lambda** | Enterprise integration | ~200ms | $0-10/mo |

### Horizontal Scaling & Queueing

```python
# Celery + RabbitMQ for async agent tasks
from celery import Celery

app = Celery('agent_tasks', broker='amqp://localhost//')

@app.task(bind=True, max_retries=3)
def process_agent_request(self, message: str, session_id: str):
    try:
        result = agent.invoke({"messages": [("user", message)]})
        return result["messages"][-1].content
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

---

## Observability & Monitoring

### LangSmith Integration

```python
import os
os.environ["LANGSMITH_API_KEY"] = "your-key"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "production-agents"

# All agent calls are now traced automatically
```

### Production Metrics Dashboard

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| **Latency P50** | < 2s | > 5s |
| **Latency P99** | < 10s | > 30s |
| **Success Rate** | > 95% | < 90% |
| **Cost per Task** | < $0.05 | > $0.10 |
| **Tool Error Rate** | < 5% | > 10% |

### Tracing Multi-Agent Workflows

```python
from langsmith import traceable

@traceable(name="research_agent")
def research_agent(query: str):
    # Web search and gather info
    return research_results

@traceable(name="writer_agent")
def writer_agent(research: str):
    # Write content based on research
    return draft

@traceable(name="reviewer_agent")
def reviewer_agent(draft: str):
    # Review and improve
    return final_content

@traceable(name="full_pipeline")
def multi_agent_pipeline(query: str):
    research = research_agent(query)
    draft = writer_agent(research)
    final = reviewer_agent(draft)
    return final
```

---

## Security, Guardrails & Reliability

### Prompt Injection Defense

```python
from nemoguardrails import LLMRails, RailsConfig

# Define guardrails
config = RailsConfig.from_path("./guardrails_config")
rails = LLMRails(config)

# Safe agent invocation
safe_response = await rails.generate_async(
    messages=[{"role": "user", "content": user_input}]
)
```

### Output Validation + PII Redaction

```python
import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def validate_and_redact(output: str) -> str:
    # PII Detection & Redaction
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()
    
    results = analyzer.analyze(text=output, language='en')
    redacted = anonymizer.anonymize(text=output, analyzer_results=results)
    
    # Output validation
    if len(redacted.text) > 10000:
        raise ValueError("Output exceeds maximum length")
    
    return redacted.text
```

### Retry Strategies & Fallbacks

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    reraise=True
)
def robust_agent_call(message: str, fallback_model="gpt-3.5-turbo"):
    try:
        return primary_agent.invoke(message)
    except RateLimitError:
        # Fallback to cheaper model
        return fallback_agent.invoke(message, model=fallback_model)
```

### Human-in-the-Loop Pattern

```python
HUMAN_APPROVAL_REQUIRED = ["process_payment", "delete_data", "send_email"]

def agent_with_approval(tool_name: str, tool_args: dict):
    if tool_name in HUMAN_APPROVAL_REQUIRED:
        approval = request_human_approval(tool_name, tool_args)
        if not approval:
            return "Action rejected by human operator"
    
    return execute_tool(tool_name, tool_args)
```

### Rate-Limit & Cost Guardrails

```python
from functools import wraps
import time

COST_LIMIT_PER_HOUR = 10.0  # USD
request_costs = []

def cost_guardrail(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        hourly_cost = sum(cost for cost, t in request_costs if time.time() - t < 3600)
        
        if hourly_cost >= COST_LIMIT_PER_HOUR:
            raise Exception(f"Hourly cost limit (${COST_LIMIT_PER_HOUR}) exceeded")
        
        result, cost = func(*args, **kwargs)
        request_costs.append((cost, time.time()))
        return result
    
    return wrapper
```

---

## Cost Optimization & Performance

### Model Routing (Cheap vs Expensive)

```python
def smart_model_router(task_type: str, complexity: str) -> str:
    """Route to appropriate model based on task"""
    
    ROUTING_TABLE = {
        ("simple_qa", "low"): "gpt-3.5-turbo",
        ("simple_qa", "medium"): "gpt-3.5-turbo",
        ("simple_qa", "high"): "gpt-4o-mini",
        ("code_gen", "low"): "gpt-4o-mini",
        ("code_gen", "medium"): "gpt-4o",
        ("code_gen", "high"): "gpt-4o",
        ("planning", "low"): "gpt-4o-mini",
        ("planning", "medium"): "gpt-4o",
        ("planning", "high"): "o1-preview",
        ("reflection", "any"): "o1-preview",  # Reasoning model
    }
    
    return ROUTING_TABLE.get((task_type, complexity), "gpt-4o-mini")
```

### Caching (Redis + Semantic Cache)

```python
import redis
import hashlib
from sentence_transformers import SentenceTransformer

redis_client = redis.Redis(host='localhost', port=6379, db=0)
encoder = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_cache_get(query: str, threshold: float = 0.95):
    """Check if similar query was cached"""
    query_embedding = encoder.encode(query)
    
    # Check against cached queries
    for cached_query, cached_embedding in get_all_cached_queries():
        similarity = cosine_similarity(query_embedding, cached_embedding)
        if similarity > threshold:
            cache_key = hashlib.md5(cached_query.encode()).hexdigest()
            return redis_client.get(cache_key)
    
    return None

def semantic_cache_set(query: str, response: str, ttl: int = 3600):
    """Cache response with semantic lookup"""
    cache_key = hashlib.md5(query.encode()).hexdigest()
    redis_client.setex(cache_key, ttl, response)
    store_embedding(query, encoder.encode(query))
```

### Batch Processing & Async Patterns

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def parallel_tool_calls(tools_to_call: list):
    """Execute multiple tools in parallel"""
    with ThreadPoolExecutor(max_workers=10) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, execute_tool, tool, args)
            for tool, args in tools_to_call
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Usage: 9 parallel web searches
results = await parallel_tool_calls([
    ("web_search", {"query": "agentic AI patterns"}),
    ("web_search", {"query": "LangGraph tutorial"}),
    # ... 7 more searches
])
```

---

## Enterprise Integration

### Connecting to Internal APIs, Databases, Auth

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """JWT Authentication for enterprise SSO"""
    try:
        payload = jwt.decode(
            credentials.credentials, 
            SECRET_KEY, 
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

@app.post("/agent/query")
async def enterprise_agent(
    request: AgentRequest,
    user: dict = Depends(verify_token)
):
    # User context available for audit logging
    audit_log(user["email"], request.message)
    return await agent.invoke(request.message)
```

### Compliance Checklist

| Requirement | Implementation | Status |
|-------------|---------------|--------|
| **GDPR** | PII detection, right to deletion, consent management | Pending |
| **SOC2** | Audit logging, access controls, encryption at rest | Pending |
| **HIPAA** | PHI handling, BAA with providers, access logging | Pending |
| **Data Retention** | Auto-delete after 90 days, configurable | Pending |
| **Access Control** | RBAC, API key rotation, MFA | Pending |

---

## Project Structure

```
Agentic-AI/
|-- README.md                          <- You are here
|-- agentic_ai_techniques_guide.md     <- Full 11+ section reference
|-- production-checklist.md            <- Pre-launch checklist
|-- examples/
|   |-- 01-reflection-agent.py         <- Reflection pattern code
|   |-- 02-planning-agent.ipynb        <- LangGraph + ReAct + planning
|   |-- 03-multi-agent-crew/           <- CrewAI + AutoGen examples
|   |-- 04-production-template/        <- FastAPI + Docker + tracing
|-- diagrams/                          <- Architecture diagrams (optional)
```

---

## Case Studies

### Case Study 1: Customer Support Agent at Scale

| Metric | Before | After |
|--------|--------|-------|
| Resolution Rate | 62% | **87%** |
| Avg Response Time | 4 min | **45 sec** |
| Cost per Ticket | $2.50 | **$0.12** |
| Human Escalation | 38% | **13%** |

**Implementation:** Planning + Tool Use + Reflection with 5 tools (order lookup, inventory, refund, email, knowledge base)

### Case Study 2: Research Analyst Agent

| Metric | Value |
|--------|-------|
| Reports Generated | 500+/month |
| Time Saved | 4 hours/report |
| Accuracy | 94% fact-checked |
| Cost per Report | $0.03 |

**Implementation:** Multi-agent (Researcher -> Writer -> Reviewer) with web search and reflection

### Case Study 3: Internal IT Ticket Agent

| Metric | Value |
|--------|-------|
| Auto-Resolution | 67% |
| Avg Resolution Time | 2 min |
| Employee Satisfaction | 4.2/5 |
| Cost Savings | $150K/year |

**Implementation:** Planning agent with 12 tools, human-in-the-loop for sensitive actions

---

## Tool Comparison

| Framework | Best For | Learning Curve | Production Ready |
|-----------|----------|----------------|------------------|
| **LangGraph** | Complex workflows, state management | Medium | Yes |
| **CrewAI** | Multi-agent teams | Low | Yes |
| **AutoGen** | Research, experimentation | Medium | Beta |
| **Semantic Kernel** | Enterprise .NET integration | Medium | Yes |
| **Custom** | Full control, specific needs | High | Yes |

---

## Further Reading & Resources

### Papers
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [HuggingGPT: Solving AI Tasks with ChatGPT](https://arxiv.org/abs/2303.17580)
- [Executable Code Actions Elicit Better LLM Agents](https://arxiv.org/abs/2402.01030)

### Courses
- [LangChain Academy](https://academy.langchain.com/)

### Communities
- [LangChain Discord](https://discord.gg/langchain)
- [r/LangChain](https://reddit.com/r/LangChain)
- [AI Engineer Discord](https://discord.gg/ai-engineers)

---

## FAQ

### 1. What's the difference between an LLM and an Agent?
An LLM generates text. An Agent uses tools, maintains state, and executes multi-step workflows.

### 2. Do I need LangGraph/CrewAI, or can I build from scratch?
Start with a framework (LangGraph recommended). Build custom once you understand the patterns.

### 3. How do I handle rate limits?
Implement retry with exponential backoff, use multiple API keys, or add a queueing system.

### 4. What's the cost of running agents in production?
Typically $0.01-0.10 per task. Use model routing and caching to optimize.

### 5. How do I evaluate if my agent is working?
Build evals from day 1. Track success rate, latency, and cost per task.

### 6. Can agents access my database?
Yes, via tools. Always use parameterized queries and limit permissions.

### 7. How do I prevent prompt injection?
Use guardrails (Llama Guard, NeMo), validate inputs, and sanitize outputs.

### 8. What's the best model for agents?
GPT-4o for complex tasks, GPT-4o-mini for simple tasks, o1 for reflection/reasoning.

### 9. How do I debug agent failures?
Use tracing (LangSmith), examine traces, and perform error analysis.

### 10. Can I run agents offline?
Yes, with local models (Ollama, LM Studio) and local tools.

---

## Acknowledgments

- **LangChain Team** for LangGraph and documentation
- **Open Source Community** for the tools and frameworks

---

<p align="center">
  <strong>From "I've heard of Agentic AI" to "I just deployed a reliable multi-agent system in production"</strong>
  <br/>
  <em>in a weekend.</em>
</p>

<p align="center">
  Star this repo if it helped you!
</p>