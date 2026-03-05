# Production Template

A production-ready template for deploying Agentic AI systems.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key-here"

# Run the server
uvicorn server:app --reload
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f agent-api

# Stop services
docker-compose down
```

## Project Structure

```
04-production-template/
|-- server.py           # FastAPI application with LangGraph agent
|-- Dockerfile          # Container configuration
|-- docker-compose.yml  # Multi-container setup
|-- requirements.txt    # Python dependencies
|-- README.md           # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/agent/invoke` | POST | Invoke agent with message |
| `/agent/stream` | POST | Stream agent response |
| `/tools` | GET | List available tools |

## Usage Examples

### Invoke Agent

```bash
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "What time is it?", "session_id": "test-123"}'
```

Response:
```json
{
  "response": "The current time is 14:30:45.",
  "session_id": "test-123",
  "timestamp": "2024-01-15T14:30:45",
  "metadata": {"message_count": 3}
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T14:30:45",
  "version": "1.0.0",
  "components": {
    "agent": "ready",
    "memory": "ready",
    "langsmith": "enabled"
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `LANGSMITH_API_KEY` | No | LangSmith API key for tracing |
| `LANGSMITH_PROJECT` | No | LangSmith project name |
| `MODEL_NAME` | No | Model to use (default: gpt-4o-mini) |
| `DEBUG` | No | Enable debug mode |
| `PORT` | No | Server port (default: 8000) |

## Production Checklist

Before deploying to production:

- [ ] Set all required environment variables
- [ ] Configure CORS settings in server.py
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Set up monitoring and alerting
- [ ] Configure SSL/TLS certificates
- [ ] Review security settings
- [ ] Set up database backups (if using PostgreSQL)

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  agent-api:
    deploy:
      replicas: 3
```

### Load Balancing

Use Nginx or a cloud load balancer:

```nginx
upstream agent_api {
    server agent-api-1:8000;
    server agent-api-2:8000;
    server agent-api-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://agent_api;
    }
}
```

## Monitoring

### LangSmith Dashboard

1. Set `LANGSMITH_API_KEY` environment variable
2. View traces at https://smith.langchain.com
3. Monitor latency, costs, and errors

### Health Monitoring

```bash
# Kubernetes liveness probe
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **CORS**: Configure allowed origins for production
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Input Validation**: All inputs are validated via Pydantic
5. **Non-root User**: Docker container runs as non-root user

## Troubleshooting

### Common Issues

**Agent not initialized**
- Check that `OPENAI_API_KEY` is set
- Verify the key is valid

**Connection refused**
- Ensure the server is running
- Check port 8000 is not in use

**High latency**
- Check model selection (gpt-4o-mini is faster)
- Enable caching with Redis
- Review LangSmith traces

## Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Docker Documentation](https://docs.docker.com/)