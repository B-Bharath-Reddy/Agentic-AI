# Production Checklist for Agentic AI Systems

> Copy-paste this checklist before deploying your agent to production.

---

## Pre-Launch Checklist

### 1. Core Agent Design

- [ ] **Pattern Selection** - Chosen appropriate pattern(s) for task:
  - [ ] Reflection (for quality improvement)
  - [ ] Tool Use (for external data/actions)
  - [ ] Planning (for multi-step tasks)
  - [ ] Multi-Agent (for specialized collaboration)

- [ ] **Tool Definitions** - All tools have:
  - [ ] Clear, descriptive docstrings
  - [ ] Typed parameters with defaults
  - [ ] Error handling and return values
  - [ ] Rate limiting (if external APIs)

- [ ] **Prompt Engineering** - System prompts include:
  - [ ] Clear role definition
  - [ ] Available tools description
  - [ ] Output format specification
  - [ ] Edge case handling instructions

---

### 2. Evaluations (Evals)

- [ ] **End-to-End Evals**
  - [ ] Created 10-20 test cases with ground truth
  - [ ] Defined success metrics (accuracy, completeness)
  - [ ] Baseline score recorded: `____%`

- [ ] **Component-Level Evals**
  - [ ] Individual tool performance tested
  - [ ] LLM step outputs validated
  - [ ] Error rate per component tracked

- [ ] **Subjective Evals** (if applicable)
  - [ ] LLM-as-judge rubric defined
  - [ ] Quality scoring system in place

---

### 3. Error Handling & Reliability

- [ ] **Retry Logic**
  - [ ] Exponential backoff implemented
  - [ ] Max retries defined (recommended: 3)
  - [ ] Fallback model configured

- [ ] **Error Recovery**
  - [ ] Graceful degradation on tool failure
  - [ ] User-friendly error messages
  - [ ] Error logging and alerting

- [ ] **Edge Cases**
  - [ ] Empty input handling
  - [ ] Very long input handling
  - [ ] Invalid input validation
  - [ ] Timeout handling

---

### 4. Security & Guardrails

- [ ] **Input Validation**
  - [ ] Prompt injection defense in place
  - [ ] Input length limits set
  - [ ] Sanitization for user inputs

- [ ] **Output Validation**
  - [ ] PII detection and redaction
  - [ ] Output length limits
  - [ ] Format validation

- [ ] **Access Control**
  - [ ] Authentication required (JWT/API key)
  - [ ] Rate limiting per user
  - [ ] Audit logging enabled

- [ ] **Sensitive Actions**
  - [ ] Human-in-the-loop for critical actions
  - [ ] Action confirmation prompts
  - [ ] Rollback capability

---

### 5. Observability & Monitoring

- [ ] **Tracing**
  - [ ] LangSmith / Phoenix / Helicone configured
  - [ ] All agent steps traced
  - [ ] Tool calls logged with timing

- [ ] **Metrics Dashboard**
  - [ ] Latency (P50, P99)
  - [ ] Success rate
  - [ ] Cost per task
  - [ ] Tool error rate

- [ ] **Alerting**
  - [ ] Latency threshold alerts
  - [ ] Error rate alerts
  - [ ] Cost threshold alerts

---

### 6. Performance & Cost

- [ ] **Model Selection**
  - [ ] Appropriate model for task complexity
  - [ ] Model routing implemented (cheap vs expensive)
  - [ ] Fallback model configured

- [ ] **Caching**
  - [ ] Response caching enabled
  - [ ] Semantic cache for similar queries
  - [ ] Cache invalidation strategy defined

- [ ] **Parallelization**
  - [ ] Independent tools run in parallel
  - [ ] Async patterns implemented

- [ ] **Cost Controls**
  - [ ] Hourly/daily cost limits set
  - [ ] Cost per task tracked
  - [ ] Budget alerts configured

---

### 7. Infrastructure

- [ ] **Deployment**
  - [ ] Docker containerized
  - [ ] Health check endpoint
  - [ ] Environment variables secured

- [ ] **Scaling**
  - [ ] Horizontal scaling tested
  - [ ] Queue system for async tasks (Celery/RabbitMQ)
  - [ ] Load balancing configured

- [ ] **Data Persistence**
  - [ ] Session memory configured
  - [ ] Database backups enabled
  - [ ] Data retention policy defined

---

### 8. Compliance & Legal

- [ ] **Data Protection**
  - [ ] GDPR compliance (if EU users)
  - [ ] Data encryption at rest
  - [ ] Data encryption in transit

- [ ] **Audit Trail**
  - [ ] All actions logged
  - [ ] User consent recorded
  - [ ] Data access auditable

- [ ] **Terms & Policies**
  - [ ] Privacy policy updated
  - [ ] Terms of service updated
  - [ ] User disclosure about AI usage

---

## Production Metrics Template

Copy this template to track your production metrics:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Success Rate** | > 95% | ___% | [ ] |
| **Latency P50** | < 2s | ___s | [ ] |
| **Latency P99** | < 10s | ___s | [ ] |
| **Cost per Task** | < $0.05 | $___ | [ ] |
| **Tool Error Rate** | < 5% | ___% | [ ] |
| **User Satisfaction** | > 4.0/5 | ___/5 | [ ] |
| **Daily Active Users** | ___ | ___ | [ ] |
| **Tasks per Day** | ___ | ___ | [ ] |

---

## Pre-Launch Testing Script

```bash
# 1. Run evals
python -m pytest tests/evals/ -v

# 2. Load test
locust -f tests/load_test.py --host=http://localhost:8000

# 3. Security scan
bandit -r src/

# 4. Check dependencies
pip-audit

# 5. Docker build test
docker build -t agent-test . && docker run -p 8000:8000 agent-test

# 6. Health check
curl http://localhost:8000/health

# 7. Smoke test
python tests/smoke_test.py
```

---

## Common Failure Modes to Watch For

| Failure Mode | Symptoms | Fix |
|--------------|----------|-----|
| **Infinite Loop** | Agent keeps calling tools | Add max turns limit |
| **Hallucination** | Wrong facts, fake tools | Add reflection, validate outputs |
| **Rate Limit Hit** | 429 errors | Implement backoff, multiple keys |
| **Cost Spike** | Unexpected bill | Set cost guardrails, alerts |
| **Memory Leak** | Increasing memory usage | Clear session data, limit history |
| **Timeout** | Long-running tasks | Add timeouts, async processing |
| **Prompt Injection** | Unexpected behavior | Add guardrails, input validation |

---

## Launch Day Checklist

- [ ] All pre-launch checks passed
- [ ] Monitoring dashboard ready
- [ ] Alert channels configured (Slack/PagerDuty)
- [ ] Rollback plan documented
- [ ] Team on-call schedule set
- [ ] User documentation updated
- [ ] Support team briefed
- [ ] Staged rollout plan (10% -> 50% -> 100%)

---

## Post-Launch Monitoring (First 48 Hours)

- [ ] Check metrics every 2 hours
- [ ] Review error logs
- [ ] Monitor cost dashboard
- [ ] Collect user feedback
- [ ] Document any issues
- [ ] Plan improvements based on data

---

## Quick Reference Commands

```bash
# Check agent health
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "test query", "session_id": "test"}'

# View recent traces
langsmith traces list --project production-agents --limit 10

# Check costs
python scripts/calculate_costs.py --last 24h

# Run evals
python -m pytest tests/evals/ --tb=short

# Scale deployment
kubectl scale deployment agent-api --replicas=5
```

---

*Last updated: March 2026*