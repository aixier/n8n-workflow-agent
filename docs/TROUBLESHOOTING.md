# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Agent Not Creating Workflows

#### Symptom
Natural language input doesn't result in workflow creation.

#### Possible Causes & Solutions

1. **n8n Connection Issues**
   ```bash
   # Check n8n is running
   curl http://localhost:5679/api/v1/workflows

   # Verify API key in .env
   echo $N8N_API_KEY
   ```

2. **Invalid Requirements**
   - Ensure requirements are clear and specific
   - Check for supported node types
   - Verify the workflow type is supported

3. **Environment Configuration**
   ```bash
   # Verify all required environment variables
   python -c "from config import config; print(config.validate())"
   ```

### 🔴 Workflow Deployment Failures

#### Symptom
Workflow created but fails to deploy to n8n.

#### Solutions

1. **API Permission Issues**
   - Verify API key has correct permissions
   - Check n8n user role settings

2. **Port Configuration**
   ```bash
   # Check if port is correct (default changed from 5678 to 5679)
   grep N8N_BASE_URL config/.env
   ```

3. **Network Connectivity**
   ```bash
   # Test connection to n8n
   ping localhost
   netstat -an | grep 5679
   ```

### 🔴 Database Connection Errors

#### Symptom
PostgreSQL connection failures.

#### Solutions

1. **Check Docker Container**
   ```bash
   # Verify container is running
   docker ps | grep postgres

   # Check container logs
   docker logs [container_id]
   ```

2. **Test Database Connection**
   ```bash
   # Test connection
   PGPASSWORD=n8n_workflow_2024 psql -h localhost -p 5432 -U n8n_user -d n8n_workflow_db
   ```

3. **Verify Credentials**
   ```bash
   # Check .env file
   cat config/.env | grep DATABASE
   ```

### 🔴 Test Execution Failures

#### Symptom
Tests fail to run or produce unexpected results.

#### Solutions

1. **Missing Test Data**
   ```bash
   # Verify test files exist
   ls -la test_*.json
   ```

2. **Workflow Not Active**
   - Ensure workflow is activated in n8n
   - Check workflow status via API

3. **Timeout Issues**
   ```python
   # Increase timeout in test configuration
   {
     "timeout": 60000,  # 60 seconds
     "retries": 3
   }
   ```

### 🔴 Performance Issues

#### Symptom
Workflows run slowly or timeout.

#### Solutions

1. **Analyze Workflow**
   ```bash
   python tools/workflow_analyzer.py [workflow_id] --performance
   ```

2. **Optimize Data Processing**
   - Implement batching for large datasets
   - Use parallel branches where possible
   - Minimize Function node usage

3. **Resource Limits**
   ```bash
   # Check system resources
   free -h
   top -n 1
   df -h
   ```

## Error Messages

### "API Key Invalid"
```
Error: n8n API authentication failed
```
**Solution**: Regenerate API key in n8n settings and update .env file.

### "Node Type Not Found"
```
Error: Unknown node type 'customNode'
```
**Solution**: Verify node type exists in n8n installation or use supported alternative.

### "Workflow Already Exists"
```
Error: Workflow with name already exists
```
**Solution**: Use unique workflow names or update existing workflow.

### "Database Connection Refused"
```
Error: ECONNREFUSED 127.0.0.1:5432
```
**Solution**: Start PostgreSQL container or verify connection settings.

### "Rate Limit Exceeded"
```
Error: Too many requests to n8n API
```
**Solution**: Implement rate limiting or increase delay between requests.

## Debugging Tools

### 1. Enable Debug Logging
```bash
# Set debug mode in .env
DEBUG=true
LOG_LEVEL=debug

# Run with verbose output
python tools/n8n_workflow_manager.py --debug
```

### 2. Inspect Workflow JSON
```bash
# Export workflow for inspection
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
     http://localhost:5679/api/v1/workflows/[id] | jq '.'
```

### 3. Test Individual Components
```python
# Test node builder
from tools.node_builder import NodeBuilder
builder = NodeBuilder()
node = builder.create_node('webhook', {'path': '/test'})
print(node)

# Test workflow manager
from tools.n8n_workflow_manager import WorkflowManager
manager = WorkflowManager()
workflows = manager.list_workflows()
print(workflows)
```

### 4. Monitor n8n Logs
```bash
# View n8n container logs
docker logs -f n8n_container_name

# Check execution history
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
     http://localhost:5679/api/v1/executions
```

## Environment-Specific Issues

### Docker Environment

1. **Container Communication**
   ```bash
   # Use docker network
   docker network create n8n-network
   docker run --network n8n-network ...
   ```

2. **Volume Permissions**
   ```bash
   # Fix permission issues
   chmod -R 755 ./data
   chown -R 1000:1000 ./data
   ```

### Windows (WSL)

1. **Line Ending Issues**
   ```bash
   # Convert line endings
   dos2unix scripts/*.sh
   ```

2. **Path Issues**
   - Use forward slashes in paths
   - Avoid spaces in directory names

### MacOS

1. **Port Conflicts**
   ```bash
   # Find process using port
   lsof -i :5679
   ```

2. **Docker Desktop Memory**
   - Increase Docker Desktop memory allocation
   - Settings → Resources → Memory: 4GB minimum

## Recovery Procedures

### 1. Backup and Restore
```bash
# Backup all workflows
python tools/backup_manager.py backup --all

# Restore from backup
python tools/backup_manager.py restore --file backup_20250128.json
```

### 2. Reset Environment
```bash
# Clean reset
rm -rf data/
rm config/.env
cp config/.env.example config/.env
# Reconfigure environment
```

### 3. Rebuild Docker Containers
```bash
# Complete rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## Getting Help

### 1. Check Logs
Always check these logs first:
- Agent logs: `logs/agent.log`
- n8n logs: `docker logs n8n`
- Database logs: `docker logs postgres`

### 2. Diagnostic Commands
```bash
# Run full diagnostic
python tools/diagnostic.py --full

# Check system health
python tools/health_check.py
```

### 3. Community Support
- GitHub Issues: Report bugs and request features
- Discord: Real-time help from community
- Documentation: Check docs/ folder for detailed guides

### 4. Debug Checklist
- [ ] n8n is running and accessible
- [ ] API key is valid and has permissions
- [ ] Database is running and accessible
- [ ] All required Python packages installed
- [ ] Environment variables properly set
- [ ] Network connectivity verified
- [ ] Sufficient system resources available
- [ ] No firewall blocking connections
- [ ] Correct file permissions set
- [ ] Latest version of agent installed

## FAQ

**Q: Why is my workflow not triggering?**
A: Check if the workflow is activated and the trigger conditions are met.

**Q: Can I use custom n8n nodes?**
A: Yes, but they must be installed in your n8n instance first.

**Q: How do I update the agent?**
A: Pull latest changes: `git pull origin main` and reinstall dependencies.

**Q: Why are credentials not working?**
A: Credentials must be configured in n8n UI, not in the agent.

**Q: Can I run multiple agents?**
A: Yes, but use different API keys and be mindful of rate limits.