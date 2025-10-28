# API Reference

## Overview

The n8n Workflow Intelligence Agent provides a comprehensive API for workflow management, node configuration, and testing.

## Core APIs

### Workflow Manager API

#### `create_workflow(config: dict) -> str`
Creates a new workflow from configuration.

**Parameters:**
- `config`: Workflow configuration dictionary

**Returns:**
- Workflow ID string

**Example:**
```python
from tools.n8n_workflow_manager import WorkflowManager

manager = WorkflowManager()
workflow_id = manager.create_workflow({
    "name": "My Workflow",
    "trigger": "webhook",
    "nodes": [...]
})
```

#### `update_workflow(workflow_id: str, changes: dict) -> bool`
Updates an existing workflow.

**Parameters:**
- `workflow_id`: ID of the workflow to update
- `changes`: Dictionary of changes to apply

**Returns:**
- Success boolean

#### `delete_workflow(workflow_id: str) -> bool`
Deletes a workflow.

**Parameters:**
- `workflow_id`: ID of the workflow to delete

**Returns:**
- Success boolean

#### `get_workflow(workflow_id: str) -> dict`
Retrieves workflow configuration.

**Parameters:**
- `workflow_id`: ID of the workflow to retrieve

**Returns:**
- Workflow configuration dictionary

### Node Builder API

#### `create_node(node_type: str, parameters: dict) -> dict`
Creates a node configuration.

**Parameters:**
- `node_type`: Type of node (e.g., 'webhook', 'http', 'function')
- `parameters`: Node-specific parameters

**Returns:**
- Node configuration dictionary

**Example:**
```python
from tools.node_builder import NodeBuilder

builder = NodeBuilder()
node = builder.create_node('http', {
    'method': 'GET',
    'url': 'https://api.example.com/data'
})
```

#### `connect_nodes(source: dict, target: dict, output: str = 'main') -> dict`
Creates a connection between nodes.

**Parameters:**
- `source`: Source node configuration
- `target`: Target node configuration
- `output`: Output pin name (default: 'main')

**Returns:**
- Connection configuration dictionary

### Test Runner API

#### `run_tests(test_suite: dict) -> dict`
Executes a test suite.

**Parameters:**
- `test_suite`: Test suite configuration

**Returns:**
- Test results dictionary

**Example:**
```python
from tools.test_runner import TestRunner

runner = TestRunner()
results = runner.run_tests({
    "workflow_id": "abc123",
    "scenarios": [
        {
            "name": "Happy path",
            "input": {...},
            "expected": {...}
        }
    ]
})
```

### Workflow Analyzer API

#### `analyze_workflow(workflow_id: str) -> dict`
Analyzes workflow performance and structure.

**Parameters:**
- `workflow_id`: ID of the workflow to analyze

**Returns:**
- Analysis results dictionary

#### `optimize_workflow(workflow_id: str) -> dict`
Suggests optimizations for a workflow.

**Parameters:**
- `workflow_id`: ID of the workflow to optimize

**Returns:**
- Optimization suggestions dictionary

## n8n API Integration

### Authentication

Set your n8n credentials in the environment configuration:

```env
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your-api-key-here
```

### Base Endpoints

- `GET /api/v1/workflows` - List all workflows
- `POST /api/v1/workflows` - Create workflow
- `GET /api/v1/workflows/{id}` - Get workflow
- `PUT /api/v1/workflows/{id}` - Update workflow
- `DELETE /api/v1/workflows/{id}` - Delete workflow
- `POST /api/v1/workflows/{id}/activate` - Activate workflow
- `POST /api/v1/workflows/{id}/deactivate` - Deactivate workflow

## Error Handling

All APIs follow consistent error handling:

```python
try:
    result = api_call()
except WorkflowError as e:
    print(f"Workflow error: {e.message}")
except NodeError as e:
    print(f"Node error: {e.message}")
except APIError as e:
    print(f"API error: {e.message}")
```

## Rate Limiting

The n8n API has rate limits. The agent automatically handles rate limiting with exponential backoff.

## Webhooks

For webhook-triggered workflows:

```python
webhook_url = manager.get_webhook_url(workflow_id)
# Returns: https://your-n8n-instance/webhook/workflow-id
```

## Response Formats

All API responses follow this structure:

```json
{
    "success": true,
    "data": {...},
    "message": "Operation successful"
}
```

Error responses:

```json
{
    "success": false,
    "error": "Error message",
    "code": "ERROR_CODE"
}
```