# Invoice Processing Agent

> **An Agentic AI solution for automated invoice data extraction, validation, and processing.**

---

## 📋 Business Problem

### The Pain Point
Companies receive **hundreds to thousands of invoices monthly** in various formats (PDFs, scanned images, emails). Manual data entry is:
- **Slow**: 2-5 minutes per invoice
- **Error-prone**: 3-5% data entry errors
- **Expensive**: $5-15 per invoice in labor costs
- **Frustrating**: Repetitive work leads to employee burnout

### Real-World Impact
| Metric | Before | After Agentic AI |
|--------|--------|------------------|
| Processing Time | 3-5 min/invoice | 10-30 seconds |
| Error Rate | 3-5% | < 1% |
| Cost per Invoice | $5-15 | $0.10-0.50 |
| Human Intervention | 100% | 10-15% (exceptions only) |

---

## 🎯 Solution Overview

An intelligent agent that:
1. **Extracts** data from invoice PDFs/images
2. **Validates** extracted data against business rules
3. **Structures** output in standardized format (JSON/Database)
4. **Flags** exceptions for human review
5. **Learns** from corrections to improve over time

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INVOICE PROCESSING WORKFLOW                               │
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│   │   Invoice   │───►│   Extract   │───►│  Validate   │───►│   Output    │ │
│   │    PDF      │    │    Data     │    │   & Clean   │    │   JSON/DB   │ │
│   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘ │
│                             │                   │                           │
│                             │                   ▼                           │
│                             │           ┌─────────────┐                    │
│                             └──────────►│   Reflect   │                    │
│                                         │ & Correct   │                    │
│                                         └─────────────┘                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Agentic Patterns Used

| Pattern | Application in This Project |
|---------|----------------------------|
| **Tool Use** | PDF parsing, OCR, database operations |
| **Reflection** | Validate extraction, self-correct errors |
| **Planning** | Handle multi-page invoices, complex layouts |
| **Multi-Agent** | Separate agents for extraction, validation, exception handling |

---

## 🚀 Learning Path (5 Phases)

### Phase 1: Basic Extraction
**Goal**: Extract key fields from simple invoice PDFs

**What You'll Build**:
- PDF text extraction using PyMuPDF/pdfplumber
- LLM-based field extraction (vendor, date, amount, line items)
- JSON output format

**What You'll Learn**:
- Tool use (PDF parsing)
- Prompt engineering for extraction
- Structured output handling

```
Input: invoice.pdf → Output: {"vendor": "...", "amount": ..., "date": "..."}
```

---

### Phase 2: Add Reflection
**Goal**: Self-validate and improve extraction quality

**What You'll Build**:
- Validation rules (date formats, amount calculations)
- Reflection loop to check extraction quality
- Error detection and correction

**What You'll Learn**:
- Reflection pattern implementation
- Validation strategies
- Iterative improvement

```
Extract → Validate → Reflect → Re-extract (if needed) → Final Output
```

---

### Phase 3: Add Evaluations
**Goal**: Measure and improve extraction accuracy

**What You'll Build**:
- Ground truth dataset
- Accuracy metrics (field-level, document-level)
- Error analysis framework

**What You'll Learn**:
- Building evaluation datasets
- Objective evaluation metrics
- Error analysis and improvement cycles

```
Ground Truth ↔ Extracted Data → Accuracy Score → Error Analysis → Improvements
```

---

### Phase 4: Handle Complex Formats
**Goal**: Process diverse invoice layouts and formats

**What You'll Build**:
- Format detection
- Multi-strategy extraction
- Table extraction for line items
- Handwritten/scanned invoice handling (OCR)

**What You'll Learn**:
- Planning pattern for format adaptation
- OCR integration
- Table extraction techniques

---

### Phase 5: Production Ready
**Goal**: Deploy as a production service

**What You'll Build**:
- FastAPI endpoint
- Database integration (PostgreSQL)
- Batch processing
- Human-in-the-loop for exceptions
- Monitoring and logging

**What You'll Learn**:
- Production deployment
- API design
- Human-in-the-loop patterns
- Observability

---

## 📁 Project Structure

```
01-invoice-processing-agent/
├── README.md                   # This file
├── requirements.txt            # Dependencies
├── .env.example               # Environment variables template
│
├── data/
│   ├── sample_invoices/       # Sample PDF invoices
│   │   ├── simple_001.pdf
│   │   ├── simple_002.pdf
│   │   ├── complex_001.pdf
│   │   └── scanned_001.pdf
│   └── ground_truth.json      # Expected extraction results
│
├── src/
│   ├── __init__.py
│   ├── agent.py               # Main agent implementation
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py   # PDF text extraction
│   │   └── llm_extractor.py   # LLM-based field extraction
│   ├── validators/
│   │   ├── __init__.py
│   │   └── validator.py       # Validation rules
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_extraction.py     # Extraction tests
│   └── test_validation.py     # Validation tests
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

# PDF Processing
PyMuPDF>=1.23.0
pdfplumber>=0.10.0

# OCR (optional, for scanned invoices)
pytesseract>=0.3.10
Pillow>=10.0.0

# API (Phase 5)
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0

# Database (Phase 5)
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Evaluation
pandas>=2.0.0
```

---

## 🔑 Environment Variables

```bash
# .env.example
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-4o-mini

# Database (Phase 5)
DATABASE_URL=postgresql://user:password@localhost:5432/invoice_db

# Optional
LANGSMITH_API_KEY=your_langsmith_key  # For tracing
```

---

## 📊 Sample Data

### Invoice Fields to Extract

| Field | Description | Example |
|-------|-------------|---------|
| `vendor_name` | Company name | "Acme Corporation" |
| `vendor_address` | Full address | "123 Business St, New York, NY 10001" |
| `invoice_number` | Invoice ID | "INV-2024-00123" |
| `invoice_date` | Issue date | "2024-03-15" |
| `due_date` | Payment due date | "2024-04-15" |
| `line_items` | List of items | [{"description": "...", "quantity": 2, "unit_price": 50.00}] |
| `subtotal` | Pre-tax total | 100.00 |
| `tax` | Tax amount | 8.00 |
| `total_due` | Final amount | 108.00 |

### Sample Ground Truth Format

```json
{
  "invoice_001.pdf": {
    "vendor_name": "Acme Corporation",
    "vendor_address": "123 Business St, New York, NY 10001",
    "invoice_number": "INV-2024-00123",
    "invoice_date": "2024-03-15",
    "due_date": "2024-04-15",
    "line_items": [
      {
        "description": "Consulting Services",
        "quantity": 10,
        "unit_price": 150.00,
        "total": 1500.00
      }
    ],
    "subtotal": 1500.00,
    "tax": 120.00,
    "total_due": 1620.00
  }
}
```

---

## 🎓 Key Learnings

By completing this project, you will understand:

1. **How to build tool-using agents** that interact with PDFs and databases
2. **How to implement reflection** for self-validation and correction
3. **How to create evaluations** to measure agent performance
4. **How to handle diverse formats** with planning strategies
5. **How to deploy agents** as production-ready services

---

## 📖 References

- [Andrew Ng's Agentic AI Course](https://www.deeplearning.ai/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

## 🤝 Next Steps

1. Set up environment: `pip install -r requirements.txt`
2. Add sample invoices to `data/sample_invoices/`
3. Start with **Phase 1** in `src/agent.py`
4. Progress through phases as you master each pattern

---

*Built as part of the Agentic AI Learning Journey*