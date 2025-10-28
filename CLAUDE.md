# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important Documentation

**Essential documents to read for complete context:**
- **README.md** - Complete project documentation with features, architecture, and usage examples
- **QUICK_START.md** - Quick start guide with common commands and troubleshooting

When users ask about project usage, installation, or need detailed examples, read these documents first:
```bash
Read /mnt/d/work/AI_Terminal/n8n-handbook/n8n-workflow-agent/README.md
Read /mnt/d/work/AI_Terminal/n8n-handbook/n8n-workflow-agent/QUICK_START.md
```

## Project Overview

**n8n Workflow Intelligence Agent** - An AI-powered system for creating, deploying, modifying, and testing n8n workflows through intelligent analysis and automated execution.

**Key Architecture**:
- **Analysis-First Approach**: Four mandatory analysis modules (Requirements → Nodes → DataFlow → Testing) must be processed sequentially before any workflow creation
- **Python Tool Suite**: Core functionality implemented in Python scripts under `tools/` directory
- **Template-Based Generation**: JSON templates in `templates/` provide base configurations for workflows, nodes, and test scenarios

## Critical Workflow Pattern

**IMPORTANT**: When users ask about:
- How to use this project → First read README.md and QUICK_START.md
- Installation or setup → First read QUICK_START.md
- Project features or capabilities → First read README.md
- Examples or tutorials → First read QUICK_START.md and check examples/ directory

When users request any n8n workflow task, you MUST follow this exact sequence:

1. **Identify Task Type**: CREATE | MODIFY | TEST | OPTIMIZE
2. **Execute Analysis Phase** (mandatory, manual):
   ```bash
   # Read each analysis module in order - DO NOT skip or automate
   Read docs/ANALYSIS_REQUIREMENTS.md  # Parse user requirements
   Read docs/ANALYSIS_NODES.md         # Design node configuration
   Read docs/ANALYSIS_DATAFLOW.md      # Plan data transformations
   Read docs/ANALYSIS_TESTING.md       # Generate test scenarios
   ```
3. **Generate Configuration**:
   ```bash
   Write workflow_config.json  # Based on analysis results
   ```
4. **Execute Implementation**:
   ```bash
   python tools/n8n_workflow_manager.py create workflow_config.json --activate
   python tools/test_runner.py test_scenarios.json
   ```

## Essential Commands

### Environment Setup
```bash
# Initial setup (from project root)
cd /mnt/d/work/AI_Terminal/n8n-handbook/n8n-workflow-agent

# One-line quick setup (recommended)
bash scripts/quick_start.sh

# Or manual setup:
cp config/.env.example config/.env
nano config/.env  # Set N8N_BASE_URL and N8N_API_KEY
pip install -r requirements.txt

# Test n8n connection
python tools/n8n_workflow_manager.py test

# For detailed setup instructions, see QUICK_START.md
```

### Workflow Management
```bash
# List all workflows
python tools/n8n_workflow_manager.py list

# Create new workflow from config
python tools/n8n_workflow_manager.py create workflow_config.json --activate

# Update existing workflow
python tools/n8n_workflow_manager.py update WORKFLOW_ID changes.json

# Backup workflow
python tools/n8n_workflow_manager.py backup WORKFLOW_ID

# Deploy/activate workflow
python tools/n8n_workflow_manager.py deploy WORKFLOW_ID

# Import workflow
python tools/n8n_workflow_manager.py import workflow.json
```

### Node Building
```bash
# Build nodes programmatically
python tools/node_builder.py

# In Python code:
from tools.node_builder import NodeBuilder
builder = NodeBuilder()
webhook = builder.build_webhook_node('/api/webhook')
process = builder.build_code_node('// Process data')
builder.chain_nodes([webhook['id'], process['id']])
workflow = builder.build_workflow('My Workflow')
```

### Workflow Analysis & Optimization
```bash
# Analyze workflow for issues
python tools/workflow_analyzer.py workflow.json --output report.md

# Analysis includes:
# - Complexity metrics
# - Performance bottlenecks
# - Security vulnerabilities
# - Optimization suggestions
```

### Testing
```bash
# Run test suite
python tools/test_runner.py test_scenarios.json

# Parallel testing
python tools/test_runner.py test_scenarios.json --parallel

# Generate HTML report
python tools/test_runner.py test_scenarios.json --format html --output report.html
```

## Core Architecture

### Analysis Modules (`docs/`)
Each module is a structured markdown document that guides the analysis phase:
- **ANALYSIS_REQUIREMENTS.md**: Converts natural language to workflow specifications
- **ANALYSIS_NODES.md**: Maps requirements to n8n node configurations
- **ANALYSIS_DATAFLOW.md**: Designs data transformation pipelines
- **ANALYSIS_TESTING.md**: Generates comprehensive test scenarios

### Python Tools (`tools/`)
- **n8n_workflow_manager.py**: Workflow lifecycle management (create, deploy, backup, import/export)
- **node_builder.py**: Programmatic node construction and connection
- **workflow_analyzer.py**: Static analysis for performance, security, and optimization
- **test_runner.py**: Automated testing with parallel execution and reporting

### Configuration Templates (`templates/`)
- **workflow_config.json**: Base workflow structure with trigger, nodes, connections
- **node_mappings.json**: Node type definitions and parameter schemas
- **test_scenarios.json**: Test case templates with input/output expectations

### Environment Configuration (`config/`)
- **.env.example**: Template for environment variables
- Required variables: `N8N_BASE_URL`, `N8N_API_KEY`
- Optional: Database config, AI service keys, notification webhooks

## Implementation Patterns

### Workflow Creation Pattern
```python
# 1. Analyze requirements
requirements = analyze_user_request(user_input)

# 2. Design nodes based on requirements
nodes = [
    {"type": "webhook", "path": "/trigger"},
    {"type": "code", "script": process_logic},
    {"type": "respondToWebhook", "response": output}
]

# 3. Build connections
connections = chain_nodes(nodes)

# 4. Generate workflow config
config = {
    "name": workflow_name,
    "nodes": nodes,
    "connections": connections,
    "settings": workflow_settings
}

# 5. Deploy and test
manager.create_workflow(config)
runner.run_tests(test_scenarios)
```

### Error Handling Pattern
All workflows must include:
- Error handler nodes for each critical operation
- Retry logic with exponential backoff
- Notification nodes for failure alerts
- Logging nodes for debugging

### Data Flow Pattern
```json
{
  "input_validation": "Schema validation node",
  "transformation": "Code/Function nodes",
  "error_handling": "Error workflow reference",
  "output_formatting": "Set/Transform nodes"
}
```

## Key Constraints

### Mandatory Requirements
1. **Analysis Phase**: Never skip or automate the analysis module reading
2. **Manual Configuration**: Always create config files manually using Write tool
3. **Testing**: Every workflow must have test scenarios before deployment
4. **Backup**: Always backup before modifying existing workflows
5. **Error Handling**: All workflows must include error handler nodes

### Security Requirements
- Never hardcode credentials - use environment variables
- Always validate input data with schema validation nodes
- Implement rate limiting for webhook endpoints
- Use authentication nodes for external API access
- Run security analysis with workflow_analyzer.py

## Response Templates

When creating workflows, structure responses as:
```
📋 Analysis Complete:
- Trigger: [type]
- Required Nodes: [list]
- Data Flow: [description]

🔧 Creating Workflow...
[Show each step]

✅ Workflow Created:
- ID: [workflow_id]
- Webhook URL: [if applicable]
- Status: Active
```

## Troubleshooting

### Common Issues
- **Connection Failed**: Verify N8N_BASE_URL and N8N_API_KEY in config/.env
- **Workflow Creation Failed**: Check node configuration and connection mappings
- **Test Timeout**: Increase TEST_TIMEOUT in environment variables
- **Import Failed**: Validate JSON structure against workflow schema

### Debug Commands
```bash
# Check n8n connection
python tools/n8n_workflow_manager.py test

# Validate workflow JSON
python -m json.tool workflow_config.json

# Run analyzer for detailed diagnostics
python tools/workflow_analyzer.py workflow.json --verbose
```

## Dependencies

**Python Requirements** (requirements.txt):
- Core: requests, aiohttp, python-dotenv, pyyaml, click
- Analysis: networkx, matplotlib, numpy
- Testing: pytest, pytest-asyncio, pytest-cov
- Data: pandas, jsonschema, jinja2

**Environment**: Python 3.8+, n8n instance with API access enabled

## Key Project Files

**Documentation Files** (always read when users ask about usage):
- `README.md` - Full project documentation
- `QUICK_START.md` - Quick start guide with examples
- `docs/CLAUDE.md` - Main AI agent instructions (deprecated, use this file instead)
- `docs/ANALYSIS_*.md` - Analysis module documentation

**Core Python Tools**:
- `tools/n8n_workflow_manager.py` - Main workflow management
- `tools/node_builder.py` - Node construction utilities
- `tools/workflow_analyzer.py` - Analysis and optimization
- `tools/test_runner.py` - Automated testing

**Configuration**:
- `config/.env.example` - Environment template
- `templates/workflow_config.json` - Workflow template
- `templates/node_mappings.json` - Node type mappings
- `templates/test_scenarios.json` - Test templates

**Examples**:
- `examples/create_youtube_workflow.py` - Complete workflow creation example
- `scripts/quick_start.sh` - Automated setup script

---

**Critical Note**: This is an AI-driven workflow management system. The analysis phase is intentionally manual and sequential to ensure proper understanding and validation of user requirements before automation begins.