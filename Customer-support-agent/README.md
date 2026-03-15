# Customer Support Ticket Triage Agent

> **An Agentic AI solution for automated ticket classification, routing, and response generation.**

---

## 📋 Business Problem

### The Pain Point
Support teams receive **hundreds of tickets daily**, leading to:
- **Slow response times**: Average 4+ hours for first response
- **Wrong routing**: 15-20% of tickets routed to wrong team
- **Repetitive work**: 60% of tickets are common questions
- **Agent burnout**: High turnover due to repetitive tasks
- **Customer frustration**: Long wait times and multiple transfers

### Real-World Impact
| Metric | Before | After Agentic AI |
|--------|--------|------------------|
| First Response Time | 4+ hours | < 45 seconds |
| Resolution Rate | 62% | **87%** |
| Wrong Routing | 15-20% | < 3% |
| Cost per Ticket | $2.50 | **$0.12** |
| Human Escalation | 38% | **13%** |

*Source: Case study from Andrew Ng's Agentic AI course*

---

## 🎯 Solution Overview

An intelligent agent that:
1. **Classifies** incoming tickets by category and urgency
2. **Routes** tickets to appropriate team/agent
3. **Generates** automated responses for common issues
4. **Escalates** complex issues to human agents
5. **Learns** from resolved tickets to improve over time

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CUSTOMER SUPPORT WORKFLOW                                 │
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│   │   Incoming  │───►│  Classify   │───►│   Route &   │───►│  Response   │ │
│   │   Ticket    │    │ & Prioritize│    │   Assign    │    │  Generate   │ │
│   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│                             │                                      │        │
│                             ▼                                      ▼        │
│                     ┌─────────────┐                       ┌─────────────┐   │
│                     │   Urgent?   │                       │   Resolve   │   │
│                     │ Escalate?   │                       │  or Escalate│   │
│                     └─────────────┘                       └─────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Agentic Patterns Used

| Pattern | Application in This Project |
|---------|----------------------------|
| **Tool Use** | Database lookup, knowledge base search, ticket system API |
| **Reflection** | Review generated response for tone and accuracy |
| **Planning** | Multi-step resolution for complex tickets |
| **Multi-Agent** | Triage agent, resolution agent, escalation agent |

---

## 🚀 Learning Path (5 Phases)

### Phase 1: Basic Classification
**Goal**: Classify tickets by category and sentiment

**What You'll Build**:
- Ticket text preprocessing
- LLM-based classification (category, urgency, sentiment)
- Simple routing logic

**What You'll Learn**:
- Text classification with LLMs
- Structured output from LLMs
- Basic routing strategies

```
Input: "My order hasn't arrived yet, it's been 5 days!" 
Output: {"category": "shipping", "urgency": "high", "sentiment": "frustrated"}
```

---

### Phase 2: Add Response Generation
**Goal**: Generate appropriate responses for common issues

**What You'll Build**:
- Template-based responses
- LLM-generated responses
- Knowledge base integration
- Response quality check

**What You'll Learn**:
- Response generation techniques
- Knowledge base retrieval
- Quality validation

```
Ticket → Classify → Lookup KB → Generate Response → Review → Send
```

---

### Phase 3: Add Reflection & Validation
**Goal**: Ensure response quality and appropriateness

**What You'll Build**:
- Tone validation (professional, empathetic)
- Fact checking against policies
- Self-correction for problematic responses
- Escalation triggers

**What You'll Learn**:
- Reflection pattern for quality control
- Policy compliance checking
- Human-in-the-loop triggers

```
Generate Response → Reflect on Quality → Improve if needed → Final Response
```

---

### Phase 4: Add Multi-Agent System
**Goal**: Specialized agents for different ticket types

**What You'll Build**:
- Triage Agent: Classify and route
- Resolution Agent: Solve common issues
- Escalation Agent: Handle complex cases
- Manager Agent: Coordinate workflow

**What You'll Learn**:
- Multi-agent orchestration
- Agent communication patterns
- Hierarchical vs sequential workflows

```
                    ┌──────────────┐
                    │ Triage Agent │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │ Resolution   │ │  Technical   │ │  Escalation  │
     │    Agent     │ │    Agent     │ │    Agent     │
     └──────────────┘ └──────────────┘ └──────────────┘
```

---

### Phase 5: Production Ready
**Goal**: Deploy as a production service

**What You'll Build**:
- FastAPI endpoint for ticket intake
- Integration with ticket systems (Zendesk, Freshdesk)
- Real-time monitoring dashboard
- A/B testing for responses
- Continuous learning pipeline

**What You'll Learn**:
- Production deployment
- Third-party integrations
- Monitoring and observability
- Continuous improvement

---

## 📁 Project Structure

```
02-customer-support-agent/
├── README.md                   # This file
├── requirements.txt            # Dependencies
├── .env.example               # Environment variables template
│
├── data/
│   ├── sample_tickets/        # Sample support tickets
│   │   ├── tickets.json       # Ticket data
│   │   └── conversations.json # Conversation history
│   ├── knowledge_base/        # Knowledge base articles
│   │   ├── shipping.json
│   │   ├── returns.json
│   │   └── billing.json
│   └── categories.json        # Ticket categories and routing rules
│
├── src/
│   ├── __init__.py
│   ├── agent.py               # Main agent implementation
│   ├── classifiers/
│   │   ├── __init__.py
│   │   ├── category.py        # Category classification
│   │   └── sentiment.py       # Sentiment analysis
│   ├── generators/
│   │   ├── __init__.py
│   │   └── response.py        # Response generation
│   ├── routers/
│   │   ├── __init__.py
│   │   └── router.py          # Routing logic
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_classification.py # Classification tests
│   └── test_response.py       # Response generation tests
│
├── notebooks/
│   └── exploration.ipynb      # Development notebook
│
└── api/
    ├── main.py                # FastAPI application
    └── models.py              # Pydantic models
```

---

## 📦 Dependencies

```txt
# Core
openai>=1.0.0
python-dotenv>=1.0.0

# Text Processing
nltk>=3.8.0
textblob>=0.17.0

# API (Phase 5)
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0

# Database (Phase 5)
sqlalchemy>=2.0.0
redis>=5.0.0

# Evaluation
pandas>=2.0.0
scikit-learn>=1.3.0
```

---

## 🔑 Environment Variables

```bash
# .env.example
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini

# Ticket System Integration (Phase 5)
ZENDESK_API_KEY=your_zendesk_key
ZENDESK_SUBDOMAIN=your_subdomain

# Database (Phase 5)
DATABASE_URL=postgresql://user:password@localhost:5432/support_db
REDIS_URL=redis://localhost:6379

# Optional
LANGSMITH_API_KEY=your_langsmith_key  # For tracing
```

---

## 📊 Sample Data

### Ticket Categories

| Category | Description | Example Issues |
|----------|-------------|----------------|
| `shipping` | Delivery issues | Late delivery, wrong address, tracking |
| `returns` | Return requests | Defective product, wrong item, refund |
| `billing` | Payment issues | Charge disputes, invoices, refunds |
| `technical` | Product issues | Bug reports, feature requests, how-to |
| `account` | Account issues | Login, password, profile updates |
| `general` | Other inquiries | Feedback, suggestions, compliments |

### Sample Ticket Format

```json
{
  "ticket_id": "TKT-2024-00123",
  "customer_email": "john.doe@email.com",
  "customer_name": "John Doe",
  "subject": "Order not received",
  "message": "I placed an order 5 days ago (Order #8847) and still haven't received it. The tracking shows it's still in transit. Can you help?",
  "priority": "normal",
  "status": "open",
  "created_at": "2024-03-15T10:30:00Z",
  "order_id": "ORD-8847"
}
```

### Sample Classification Output

```json
{
  "ticket_id": "TKT-2024-00123",
  "classification": {
    "category": "shipping",
    "subcategory": "delivery_delay",
    "urgency": "high",
    "sentiment": "frustrated",
    "confidence": 0.92
  },
  "routing": {
    "team": "shipping_support",
    "agent": null,
    "sla_hours": 4
  },
  "suggested_response": "Hi John, I apologize for the delay with your order #8847...",
  "escalation_required": false,
  "similar_tickets": ["TKT-2024-00115", "TKT-2024-00098"]
}
```

### Knowledge Base Format

```json
{
  "article_id": "KB-001",
  "title": "Shipping Policy",
  "category": "shipping",
  "content": "Standard shipping takes 5-7 business days...",
  "keywords": ["shipping", "delivery", "tracking", "delay"],
  "last_updated": "2024-03-01"
}
```

---

## 🎓 Key Learnings

By completing this project, you will understand:

1. **How to classify text** using LLMs with structured outputs
2. **How to generate contextually appropriate responses** with guardrails
3. **How to implement reflection** for quality assurance
4. **How to build multi-agent systems** for specialized tasks
5. **How to integrate with real business systems** (ticketing platforms)

---

## 📖 References

- [Andrew Ng's Agentic AI Course](https://www.deeplearning.ai/)
- [Zendesk API Documentation](https://developer.zendesk.com/api/)
- [Building Customer Service Agents](https://platform.openai.com/docs/guides/customer-service-agents)

---

## 🤝 Next Steps

1. Set up environment: `pip install -r requirements.txt`
2. Add sample tickets to `data/sample_tickets/`
3. Start with **Phase 1** in `src/agent.py`
4. Progress through phases as you master each pattern

---

*Built as part of the Agentic AI Learning Journey*