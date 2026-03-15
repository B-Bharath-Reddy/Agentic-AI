# Data Analyst Agent

> **An Agentic AI solution for natural language data analysis, visualization, and insights generation.**

---

## 📋 Business Problem

### The Pain Point
Business users need data insights but face significant barriers:
- **SQL knowledge required**: Most business users don't know SQL
- **Slow turnaround**: Data team requests take days to fulfill
- **Repetitive queries**: Same questions asked repeatedly
- **Inconsistent analysis**: Different analysts give different answers
- **Visualization challenges**: Creating charts requires technical skills

### Real-World Impact
| Metric | Before | After Agentic AI |
|--------|--------|------------------|
| Time to Insight | 2-5 days | < 5 minutes |
| Data Team Load | 100% | 20% (complex queries only) |
| Self-Service Rate | 10% | **85%** |
| Report Generation | 4 hours | **30 seconds** |
| Cost per Analysis | $50-200 | **$0.05-0.50** |

---

## 🎯 Solution Overview

An intelligent agent that:
1. **Understands** natural language questions about data
2. **Generates** SQL queries or Python code automatically
3. **Executes** queries against databases/data files
4. **Creates** visualizations automatically
5. **Explains** findings in plain English

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATA ANALYST WORKFLOW                                     │
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│   │   Natural   │───►│   Generate  │───►│   Execute   │───►│  Generate   │ │
│   │   Language  │    │  SQL/Code   │    │   Query     │    │   Report    │ │
│   │   Question  │    │             │    │             │    │  & Charts   │ │
│   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│                             │                   │                           │
│                             │                   ▼                           │
│                             │           ┌─────────────┐                    │
│                             └──────────►│   Reflect   │                    │
│                                         │  & Validate │                    │
│                                         └─────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Agentic Patterns Used

| Pattern | Application in This Project |
|---------|----------------------------|
| **Tool Use** | Database queries, code execution, visualization |
| **Reflection** | Validate query correctness, verify results |
| **Planning** | Multi-step analysis, complex joins |
| **Multi-Agent** | Query agent, visualization agent, insight agent |

---

## 🚀 Learning Path (5 Phases)

### Phase 1: Basic Query Generation
**Goal**: Convert natural language to SQL and execute

**What You'll Build**:
- Natural language to SQL conversion
- Query execution against SQLite/PostgreSQL
- Basic result formatting

**What You'll Learn**:
- Prompt engineering for SQL generation
- Database connection and execution
- Error handling for invalid queries

```
Input: "What were total sales last month?"
Output: SELECT SUM(amount) FROM sales WHERE date >= '2024-02-01' → $125,000
```

---

### Phase 2: Add Code Execution
**Goal**: Execute Python code for complex analysis

**What You'll Build**:
- Python code generation for analysis
- Safe code execution sandbox
- Pandas integration for data manipulation

**What You'll Learn**:
- Code generation patterns
- Safe code execution
- Data transformation techniques

```
Input: "Show me the trend of sales by month"
Output: Python code → Line chart with monthly sales trend
```

---

### Phase 3: Add Visualization
**Goal**: Automatically generate appropriate visualizations

**What You'll Build**:
- Chart type selection based on data
- Matplotlib/Plotly integration
- Chart customization and labeling

**What You'll Learn**:
- Visualization selection logic
- Chart generation with code
- Multi-modal outputs (text + images)

```
Query Results → Analyze Data Types → Select Chart Type → Generate Code → Display Chart
```

---

### Phase 4: Add Reflection & Validation
**Goal**: Ensure query correctness and meaningful insights

**What You'll Build**:
- Query validation before execution
- Result sanity checks
- Self-correction for failed queries
- Insight quality validation

**What You'll Learn**:
- Reflection for query validation
- Error recovery strategies
- Quality assurance for analysis

```
Generate SQL → Validate → Execute → Check Results → Reflect → Fix if needed
```

---

### Phase 5: Production Ready
**Goal**: Deploy as a production service

**What You'll Build**:
- FastAPI endpoint for analysis requests
- Connection to multiple data sources
- Scheduled report generation
- Dashboard integration
- Query caching for performance

**What You'll Learn**:
- Production deployment
- Multi-database support
- Caching strategies
- Dashboard integration

---

## 📁 Project Structure

```
03-data-analyst-agent/
├── README.md                   # This file
├── requirements.txt            # Dependencies
├── .env.example               # Environment variables template
│
├── data/
│   ├── sample_datasets/       # Sample data files
│   │   ├── sales.csv          # Sales data
│   │   ├── customers.csv      # Customer data
│   │   └── products.csv       # Product catalog
│   ├── database/              # SQLite database
│   │   └── company.db
│   └── schema.json            # Database schema description
│
├── src/
│   ├── __init__.py
│   ├── agent.py               # Main agent implementation
│   ├── query/
│   │   ├── __init__.py
│   │   ├── sql_generator.py   # SQL generation
│   │   └── executor.py        # Query execution
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── code_generator.py  # Python code generation
│   │   └── sandbox.py         # Safe code execution
│   ├── visualization/
│   │   ├── __init__.py
│   │   ├── chart_generator.py # Chart generation
│   │   └── chart_selector.py  # Chart type selection
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_sql_generation.py # SQL generation tests
│   └── test_analysis.py       # Analysis tests
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

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Data Analysis
pandas>=2.0.0
numpy>=1.24.0

# Visualization
matplotlib>=3.7.0
plotly>=5.18.0
seaborn>=0.12.0

# Code Execution
restrictedpython>=6.0

# API (Phase 5)
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0

# Caching (Phase 5)
redis>=5.0.0
```

---

## 🔑 Environment Variables

```bash
# .env.example
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini

# Database connections
DATABASE_URL=postgresql://user:password@localhost:5432/analytics_db
SQLITE_PATH=./data/database/company.db

# Redis for caching (Phase 5)
REDIS_URL=redis://localhost:6379

# Optional
LANGSMITH_API_KEY=your_langsmith_key  # For tracing
```

---

## 📊 Sample Data

### Database Schema

```json
{
  "tables": {
    "sales": {
      "columns": {
        "sale_id": "INTEGER PRIMARY KEY",
        "date": "DATE",
        "customer_id": "INTEGER",
        "product_id": "INTEGER",
        "quantity": "INTEGER",
        "amount": "DECIMAL(10,2)",
        "region": "VARCHAR(50)"
      },
      "description": "Contains all sales transactions"
    },
    "customers": {
      "columns": {
        "customer_id": "INTEGER PRIMARY KEY",
        "name": "VARCHAR(100)",
        "email": "VARCHAR(100)",
        "signup_date": "DATE",
        "segment": "VARCHAR(50)"
      },
      "description": "Customer information"
    },
    "products": {
      "columns": {
        "product_id": "INTEGER PRIMARY KEY",
        "name": "VARCHAR(100)",
        "category": "VARCHAR(50)",
        "price": "DECIMAL(10,2)",
        "stock": "INTEGER"
      },
      "description": "Product catalog"
    }
  }
}
```

### Sample Queries

| Natural Language Question | Generated SQL |
|---------------------------|---------------|
| "What were total sales last month?" | `SELECT SUM(amount) FROM sales WHERE date >= DATE('now', '-1 month')` |
| "Top 5 products by revenue" | `SELECT p.name, SUM(s.amount) FROM sales s JOIN products p GROUP BY p.name ORDER BY SUM(s.amount) DESC LIMIT 5` |
| "Sales by region" | `SELECT region, SUM(amount) FROM sales GROUP BY region` |
| "Average order value" | `SELECT AVG(amount) FROM sales` |

### Sample Analysis Output

```json
{
  "question": "What were total sales last month?",
  "sql_generated": "SELECT SUM(amount) as total_sales FROM sales WHERE date >= '2024-02-01' AND date < '2024-03-01'",
  "results": {
    "total_sales": 125000.00
  },
  "visualization": {
    "type": "kpi_card",
    "value": "$125,000",
    "trend": "+15% vs previous month"
  },
  "insight": "Total sales for last month were $125,000, which is a 15% increase compared to the previous month. This growth is primarily driven by increased sales in the Electronics category.",
  "execution_time_ms": 45
}
```

### Sample Visualization Output

```json
{
  "question": "Show me sales trend by month",
  "chart_type": "line",
  "chart_config": {
    "title": "Monthly Sales Trend",
    "x_axis": "Month",
    "y_axis": "Total Sales ($)",
    "data": [
      {"month": "Jan", "sales": 100000},
      {"month": "Feb", "sales": 125000},
      {"month": "Mar", "sales": 115000}
    ]
  },
  "insights": [
    "February had the highest sales at $125,000",
    "Average monthly sales: $113,333",
    "Month-over-month growth: +15% (Jan to Feb)"
  ]
}
```

---

## 🎓 Key Learnings

By completing this project, you will understand:

1. **How to convert natural language to SQL** using LLMs
2. **How to execute code safely** in a sandboxed environment
3. **How to generate visualizations** automatically
4. **How to implement reflection** for query validation
5. **How to build production-ready** data analysis systems

---

## 📖 References

- [Andrew Ng's Agentic AI Course](https://www.deeplearning.ai/)
- [Text-to-SQL Best Practices](https://platform.openai.com/docs/guides/text-to-sql)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Plotly Python](https://plotly.com/python/)

---

## 🤝 Next Steps

1. Set up environment: `pip install -r requirements.txt`
2. Add sample data to `data/sample_datasets/`
3. Start with **Phase 1** in `src/agent.py`
4. Progress through phases as you master each pattern

---

*Built as part of the Agentic AI Learning Journey*