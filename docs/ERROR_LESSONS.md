# Error Lessons Documentation

This document records errors encountered, their root causes, and solutions applied during n8n workflow development and management.

---

## Webhook Configuration

### Webhook Not Registered (404 Error) - Updated: 2025-10-29
**Context**: Production webhook endpoints returning 404 despite active workflow
**Error Message**: `"The requested webhook \"POST webhook-path\" is not registered"`
**Root Cause**:
- n8n webhook registration may fail silently after workflow creation via API
- Webhooks created via API may not register until manually saved in UI
- Service restart may be required for webhook registration
- Test webhooks (`/webhook-test/`) also require UI interaction ("Execute workflow" button)
- **CONFIRMED**: Even when workflow shows "active: true" in API, webhooks still return 404

**Solution Applied**:
1. Open workflow in n8n UI (http://localhost:5679)
2. Click on webhook node to verify configuration
3. Save workflow manually (Ctrl+S) - **CRITICAL STEP**
4. Verify workflow is activated (toggle in top-right)
5. If still not working, restart n8n service

**Alternative Solutions**:
- Use manual workflow execution via API (limited support)
- Create workflows through UI first, then manage via API
- Use n8n's CLI tools if available
- Create comprehensive activation guide (see WEBHOOK_ACTIVATION_GUIDE.md)

**Test Results (2025-10-29)**:
- Tested 3 active workflows with 9 different webhook calls
- All returned 404 despite showing as active in API
- No executions recorded in workflow history
- Test webhooks also failed without UI interaction
- **YouTube Processor Test (ElwksDwOH8GAYs4x)**: Active but webhooks not registered
- Created activation test script (activate_webhook_test.py) for guided testing

**Prevention Strategy**:
- Always verify webhook registration after API-based workflow creation
- Use test webhook URLs during development
- Include webhook verification in deployment scripts
- Consider using n8n's internal execution API for testing
- Document webhook activation requirements prominently

**Code Example**:
```python
# Comprehensive webhook testing
def test_webhook_activation(workflow_id, webhook_path):
    # Test production webhook
    prod_url = f"{base_url}/webhook/{webhook_path}"
    response = requests.post(prod_url, json=test_data, timeout=5)

    if response.status_code == 404:
        print("❌ Production webhook not registered")

        # Try test webhook
        test_url = f"{base_url}/webhook-test/{workflow_id}/{webhook_path}"
        test_response = requests.post(test_url, json=test_data, timeout=5)

        if test_response.status_code == 404:
            print("❌ Test webhook also not active")
            print("📝 Required: Manual save in n8n UI")
            return False

    return response.status_code == 200
```

---

## API Errors

### Read-Only Fields in Workflow Creation - Updated: 2025-10-29
**Context**: Creating workflows via n8n API
**Error Message**: `"additional properties are not allowed"`
**Root Cause**: Including read-only fields like 'active' or 'id' in POST request
**Solution Applied**: Remove read-only fields before API submission
```python
# Remove read-only fields
workflow_data.pop('active', None)
workflow_data.pop('id', None)
workflow_data.pop('createdAt', None)
workflow_data.pop('updatedAt', None)
```
**Prevention Strategy**: Create clean workflow objects with only required fields

### Port Configuration Mismatch - Updated: 2025-10-29
**Context**: n8n API connection failures
**Error Message**: Connection refused or timeout
**Root Cause**: Using wrong port (5678 instead of 5679)
**Solution Applied**: Update N8N_BASE_URL in .env to correct port
**Prevention Strategy**: Verify n8n instance URL and port before configuration

### HTTP 405 Method Not Allowed - Updated: 2025-10-29
**Context**: Attempting to activate/deactivate workflows via API
**Error Message**: `405 Method Not Allowed`
**Root Cause**: Using incorrect HTTP method or endpoint for workflow activation
**Solution Applied**: Use correct PATCH endpoint with proper payload
```python
# Correct method for activation (Note: May still fail with n8n versions)
requests.patch(
    f'{base_url}/api/v1/workflows/{workflow_id}',
    headers=headers,
    json={'active': True}
)
```
**Important Note**: Workflow activation via API is not fully supported in all n8n versions
**Alternative**: Activate workflows manually through the n8n UI
**Prevention Strategy**: Refer to n8n API documentation for correct endpoints

### Workflow Execution API Limitations - Updated: 2025-10-29
**Context**: Attempting to execute workflows programmatically via API
**Error Message**: `404 not found` when calling `/api/v1/workflows/{id}/execute`
**Root Cause**: n8n API has limited support for direct workflow execution
**Solution Applied**:
- Use webhook triggers for automated execution
- Execute workflows through n8n UI
- Use n8n CLI if available
**Prevention Strategy**: Design workflows with webhook triggers for external automation

---

## GitHub Integration

### SSH Key Permission Denied - Updated: 2025-10-29
**Context**: Pushing to GitHub repository
**Error Message**: `Permission denied (publickey)`
**Root Cause**: SSH keys not configured or not added to GitHub account
**Solution Applied**: Switch to HTTPS URL for repository
```bash
git remote set-url origin https://github.com/username/repo.git
```
**Prevention Strategy**: Use HTTPS URLs in automated environments or configure SSH keys properly

### Environment File Committed Accidentally - Updated: 2025-10-29
**Context**: Sensitive .env file pushed to repository
**Error Message**: No error, but security issue
**Root Cause**: .gitignore not configured before initial commit
**Solution Applied**:
1. Remove file from repository history
2. Update .gitignore
3. Force push cleaned history
**Prevention Strategy**: Always configure .gitignore before first commit

---

## Workflow Execution

### Workflow ID Not Found - Updated: 2025-10-29
**Context**: Accessing workflow details via API
**Error Message**: `404 Not Found`
**Root Cause**: Using incorrect or outdated workflow ID
**Solution Applied**: List all workflows to get current IDs
```python
response = requests.get(f'{base_url}/api/v1/workflows', headers=headers)
workflows = response.json().get('data', [])
```
**Prevention Strategy**: Store and verify workflow IDs after creation

---

## Python Environment

### Module Import Errors - Updated: 2025-10-29
**Context**: Running Python tools for workflow management
**Error Message**: `ModuleNotFoundError`
**Root Cause**: Missing dependencies or incorrect Python path
**Solution Applied**: Install requirements and verify Python environment
```bash
pip install -r requirements.txt
python -m tools.n8n_workflow_manager test
```
**Prevention Strategy**: Use virtual environment and document dependencies

### AttributeError in NodeBuilder - Updated: 2025-10-29
**Context**: Using NodeBuilder class for programmatic node creation
**Error Message**: `AttributeError: 'NodeBuilder' object has no attribute 'generate_node_id'`
**Root Cause**: Method name mismatch or outdated API
**Solution Applied**: Use correct method names or UUID directly
```python
import uuid
node_id = str(uuid.uuid4())
```
**Prevention Strategy**: Check class documentation and available methods

---

## Database Connection

### PostgreSQL Connection Refused - Updated: 2025-10-29
**Context**: Connecting to PostgreSQL in Docker container
**Error Message**: `connection refused`
**Root Cause**: Container not running or incorrect port mapping
**Solution Applied**: Verify container status and port mapping
```bash
docker ps | grep postgres
docker exec -it container_id psql -U postgres
```
**Prevention Strategy**: Include connection verification in setup scripts

---

## Testing Issues

### Timeout in Webhook Tests - Updated: 2025-10-29
**Context**: Testing webhook endpoints
**Error Message**: Request timeout
**Root Cause**: Workflow processing taking too long or infinite loop
**Solution Applied**: Add timeout parameter and handle gracefully
```python
try:
    response = requests.post(url, json=data, timeout=15)
except requests.exceptions.Timeout:
    print("Request timed out - workflow may be processing")
```
**Prevention Strategy**: Design workflows with response time in mind

---

## Notes

- Each error entry should include the exact error message for searchability
- Focus on root cause analysis to prevent recurrence
- Include code examples for both the error and the solution
- Update entries when new information is discovered
- Track frequency of errors to identify systemic issues