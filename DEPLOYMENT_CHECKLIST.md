# Deployment & Setup Checklist

## Pre-Deployment

- [ ] **Docker Installation**
  - [ ] Docker Desktop installed (Windows/Mac)
  - [ ] Docker & Docker Compose available in PATH
  - [ ] Docker daemon running
  - [ ] Verify: `docker --version && docker-compose --version`

- [ ] **System Requirements**
  - [ ] Minimum 4GB RAM available
  - [ ] 20GB free disk space
  - [ ] Ports available: 8000, 5000, 6333, 11434, 6379, 5432, 8080
  - [ ] Network connectivity

- [ ] **Repository Setup**
  - [ ] Code cloned to local machine
  - [ ] All three subdirectories present (orchestrator-agent, hotel-search-engine, tbo)
  - [ ] Git configured (if needed)

## Configuration Setup

- [ ] **Environment Variables**
  - [ ] `.env` file copied from template
  - [ ] Database credentials set
  - [ ] Email notifications configured (if needed)
  - [ ] API keys populated (if any external services)

- [ ] **File Structure**
  - [ ] `docker-compose.yml` present
  - [ ] `.env` file present
  - [ ] `start.bat` or `start.sh` executable
  - [ ] `test_integration.py` present

## Pre-Deployment Tests

- [ ] **Local Verification**
  - [ ] `orchestrator-agent/requirements.txt` checked
  - [ ] `hotel-search-engine/requirements.txt` checked
  - [ ] `tbo/requirements.txt` checked
  - [ ] All dependencies listed

- [ ] **Code Quality**
  - [ ] No Python syntax errors
  - [ ] Import statements valid
  - [ ] Configuration paths correct
  - [ ] No hardcoded credentials

## Deployment

### Step 1: Initial Startup
- [ ] Navigate to project root: `cd tbo-chatbot`
- [ ] Start services: `docker-compose up --build`
- [ ] Monitor logs for errors
- [ ] Wait 3-5 minutes for models to download/initialize

### Step 2: Verify Services
- [ ] Orchestrator health: `curl http://localhost:8000/health`
- [ ] Hotel Search health: `curl http://localhost:5000/health`
- [ ] Qdrant status: `curl http://localhost:6333/readyz`
- [ ] Check all status codes are 200

### Step 3: Model Initialization
- [ ] Wait for model-init service to complete
- [ ] Phi4 model pulling: Monitor `docker logs tbo-model-init`
- [ ] Llama2 model pulling: Monitor `docker logs tbo-model-init`
- [ ] Verify: `curl http://localhost:11434/api/tags`

### Step 4: Database Setup
- [ ] PostgreSQL container started: `docker logs tbo-postgres`
- [ ] Database initialized successfully
- [ ] Admin UI accessible: http://localhost:8080
- [ ] Can connect: user/password

### Step 5: Vector DB Setup
- [ ] Qdrant container running: `docker logs tbo-qdrant`
- [ ] Collections endpoint responds: `curl http://localhost:6333/collections`
- [ ] Storage volumes created
- [ ] Health status: healthy

## Post-Deployment Tests

### Functional Testing
- [ ] Run integration tests: `python test_integration.py`
- [ ] All 6 tests should pass:
  - [ ] Service Health Check
  - [ ] Hotel Search Engine
  - [ ] Qdrant Vector DB
  - [ ] JSON Query Processing
  - [ ] RAG Endpoint
  - [ ] Natural Language Query

### API Testing
- [ ] Health endpoint works
- [ ] JSON query endpoint works
- [ ] RAG endpoint responds
- [ ] Hotel search returns results
- [ ] LLM generates responses

### Performance Testing
- [ ] Hotel search: < 500ms
- [ ] RAG retrieval: < 1s
- [ ] LLM analysis: < 5s
- [ ] End-to-end: < 8s

## Monitoring Setup

- [ ] **Logging**
  - [ ] Logs directory accessible
  - [ ] Log rotation configured
  - [ ] Error logs monitored

- [ ] **Metrics**
  - [ ] Response times logged
  - [ ] Error rates tracked
  - [ ] Database query times monitored

- [ ] **Alerts**
  - [ ] Service failure alerts configured
  - [ ] High latency alerts set (> 10s)
  - [ ] Disk space alerts enabled

## Security Hardening

- [ ] **Credentials**
  - [ ] No credentials in git history
  - [ ] `.env` file is in `.gitignore`
  - [ ] Database password changed from default
  - [ ] API keys secured

- [ ] **Network**
  - [ ] Services not exposed unnecessarily
  - [ ] Firewall configured
  - [ ] TLS enabled for external traffic (production)
  - [ ] CORS settings reviewed

- [ ] **Access Control**
  - [ ] Database user restricted to necessary databases
  - [ ] API rate limiting configured (if needed)
  - [ ] Authentication enforced (production)
  - [ ] Admin UI secured

## Backup & Recovery

- [ ] **Backup Plan**
  - [ ] Database backup schedule configured
  - [ ] Vector DB snapshots scheduled
  - [ ] Backup storage location configured
  - [ ] Recovery procedure documented

- [ ] **Disaster Recovery**
  - [ ] Can restore from backup
  - [ ] RPO (Recovery Point Objective) defined
  - [ ] RTO (Recovery Time Objective) defined
  - [ ] Tested recovery process

## Production Deployment

### Pre-Production
- [ ] Feature flag testing complete
- [ ] Load testing done
- [ ] Security audit passed
- [ ] Documentation finalized

### Deployment
- [ ] Blue-green deployment planned (if handling traffic)
- [ ] Canary testing configured
- [ ] Rollback plan documented
- [ ] Maintenance window scheduled

### Post-Deployment
- [ ] Monitoring active
- [ ] Alerts all firing correctly
- [ ] Support team trained
- [ ] Incident response plan active

## Troubleshooting Checklist

### Startup Issues
- [ ] Docker daemon running
- [ ] Ports not in use: `netstat -an` (Windows)
- [ ] Disk space available: 20GB minimum
- [ ] RAM available: 4GB minimum

### Model Loading Issues
- [ ] Ollama service healthy
- [ ] Internet connectivity working
- [ ] Sufficient disk space for models (10GB+)
- [ ] Model pull logs: `docker logs tbo-model-init`

### Connection Issues
- [ ] All containers running: `docker ps`
- [ ] Network created: `docker network ls | grep tbo-network`
- [ ] DNS resolution working
- [ ] Port mappings correct: `docker port <container>`

### Database Issues
- [ ] PostgreSQL started: `docker logs tbo-postgres`
- [ ] Admin UI accessible: http://localhost:8080
- [ ] Credentials correct in `.env`
- [ ] Volume mounted: `docker inspect tbo-postgres`

### API Issues
- [ ] Service health check passing
- [ ] Request validation passing
- [ ] Response format valid JSON
- [ ] Logs showing errors

## Performance Tuning

- [ ] PostgreSQL indexes created
- [ ] Redis cache hit rate > 80%
- [ ] Qdrant query latency < 1s
- [ ] LLM response latency acceptable
- [ ] No memory leaks detected

## Documentation

- [ ] README.md updated
- [ ] API documentation current
- [ ] Configuration options documented
- [ ] Troubleshooting guide present
- [ ] Deployment procedure documented

## Sign-Off

- [ ] All checklist items completed
- [ ] Integration tests passing
- [ ] Performance acceptable
- [ ] Security audit passed
- [ ] **Ready for production** ✅

---

## Quick Reference Commands

```bash
# Start
docker-compose up --build

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Health check
curl http://localhost:8000/health

# Test integration
python test_integration.py

# Clean volumes
docker-compose down -v

# Restart service
docker-compose restart orchestrator-agent

# View database
# Visit: http://localhost:8080
# User: user
# Password: password
```

---

**Date**: March 1, 2026  
**Version**: 1.0.0
