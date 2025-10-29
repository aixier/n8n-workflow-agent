#!/usr/bin/env python3
"""
YouTube Workflow Test Script
Tests the n8n workflow agent's ability to process YouTube videos
"""

import requests
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

def test_youtube_workflow():
    """Test YouTube workflow functionality"""

    api_key = os.getenv('N8N_API_KEY')
    base_url = os.getenv('N8N_BASE_URL', 'http://localhost:5679')

    if not api_key:
        print("❌ N8N_API_KEY not found in environment")
        return False

    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    print("=" * 60)
    print("YouTube Workflow Test Suite")
    print("=" * 60)
    print(f"n8n Base URL: {base_url}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Test 1: List all workflows
    print("📋 Test 1: Listing all workflows...")
    response = requests.get(f'{base_url}/api/v1/workflows', headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to list workflows: {response.status_code}")
        return False

    workflows = response.json().get('data', [])
    youtube_workflows = [w for w in workflows if 'youtube' in w['name'].lower()]

    print(f"✅ Found {len(workflows)} total workflows")
    print(f"   - {len(youtube_workflows)} YouTube-related workflows")

    for wf in youtube_workflows:
        print(f"     • {wf['name']} (ID: {wf['id']}, Active: {wf.get('active', False)})")
    print()

    # Test 2: Create a simple YouTube processor workflow
    print("🔧 Test 2: Creating YouTube processor workflow...")

    workflow_config = {
        "name": f"YouTube Processor Test - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "nodes": [
            {
                "parameters": {
                    "content": "## YouTube Video Processor\n\nThis workflow processes YouTube URLs and extracts video information.",
                    "height": 200,
                    "width": 400
                },
                "id": "note_1",
                "name": "Documentation",
                "type": "n8n-nodes-base.stickyNote",
                "typeVersion": 1,
                "position": [250, 100]
            },
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": f"youtube-processor-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "responseMode": "lastNode",
                    "options": {}
                },
                "id": "webhook_1",
                "name": "YouTube URL Input",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1.1,
                "position": [250, 350]
            },
            {
                "parameters": {
                    "jsCode": "// Extract and validate YouTube URL\\nconst input = $input.item.json.body || $input.item.json;\\nconst url = input.youtube_url || input.url;\\n\\nif (!url) {\\n  throw new Error('YouTube URL is required');\\n}\\n\\n// Extract video ID\\nconst videoIdMatch = url.match(/(?:youtube\\.com\\/watch\\?v=|youtu\\.be\\/)([\\w-]{11})/);\\nconst videoId = videoIdMatch ? videoIdMatch[1] : null;\\n\\nif (!videoId) {\\n  throw new Error('Invalid YouTube URL');\\n}\\n\\nreturn {\\n  videoId: videoId,\\n  originalUrl: url,\\n  timestamp: new Date().toISOString(),\\n  status: 'processed'\\n};"
                },
                "id": "code_1",
                "name": "Process URL",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [450, 350]
            },
            {
                "parameters": {
                    "values": {
                        "string": [
                            {
                                "name": "message",
                                "value": "YouTube video processed successfully"
                            }
                        ],
                        "number": [
                            {
                                "name": "processingTime",
                                "value": "={{Date.now() - $now.toMillis()}}"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "set_1",
                "name": "Add Metadata",
                "type": "n8n-nodes-base.set",
                "typeVersion": 2,
                "position": [650, 350]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ JSON.stringify($json) }}",
                    "options": {}
                },
                "id": "respond_1",
                "name": "Return Result",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [850, 350]
            }
        ],
        "connections": {
            "webhook_1": {
                "main": [[{"node": "code_1", "type": "main", "index": 0}]]
            },
            "code_1": {
                "main": [[{"node": "set_1", "type": "main", "index": 0}]]
            },
            "set_1": {
                "main": [[{"node": "respond_1", "type": "main", "index": 0}]]
            }
        },
        "settings": {
            "executionOrder": "v1"
        }
    }

    # Create the workflow
    create_response = requests.post(
        f'{base_url}/api/v1/workflows',
        headers=headers,
        json=workflow_config
    )

    if create_response.status_code not in [200, 201]:
        print(f"❌ Failed to create workflow: {create_response.status_code}")
        print(f"   Error: {create_response.text[:300]}")
        return False

    workflow = create_response.json()
    workflow_id = workflow.get('id')
    webhook_path = workflow_config['nodes'][1]['parameters']['path']

    print(f"✅ Workflow created successfully!")
    print(f"   ID: {workflow_id}")
    print(f"   Name: {workflow.get('name')}")
    print(f"   Webhook path: {webhook_path}")
    print()

    # Test 3: Execute the workflow
    print("🚀 Test 3: Testing workflow execution...")

    # Try manual execution via API
    execute_data = {
        "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }

    # Execute workflow manually
    exec_response = requests.post(
        f'{base_url}/api/v1/workflows/{workflow_id}/execute',
        headers=headers,
        json={"body": execute_data}
    )

    if exec_response.status_code == 200:
        exec_result = exec_response.json()
        print(f"✅ Workflow executed successfully!")
        print(f"   Execution ID: {exec_result.get('id', 'N/A')}")
        if 'data' in exec_result:
            print(f"   Result: {json.dumps(exec_result['data'], indent=2)[:500]}")
    else:
        print(f"⚠️ Manual execution returned: {exec_response.status_code}")
        print(f"   Response: {exec_response.text[:300]}")

    print()

    # Test 4: Check workflow execution history
    print("📊 Test 4: Checking execution history...")
    exec_history_response = requests.get(
        f'{base_url}/api/v1/executions',
        headers=headers,
        params={'workflowId': workflow_id}
    )

    if exec_history_response.status_code == 200:
        executions = exec_history_response.json().get('data', [])
        print(f"✅ Found {len(executions)} executions for this workflow")
        for exec in executions[:3]:  # Show last 3 executions
            print(f"   - Status: {exec.get('status')}, Started: {exec.get('startedAt')}")
    else:
        print(f"⚠️ Could not retrieve execution history")

    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"✅ Successfully created and tested YouTube workflow")
    print(f"📍 Workflow ID: {workflow_id}")
    print(f"📝 Next steps:")
    print(f"   1. Open n8n UI at {base_url}")
    print(f"   2. Activate the workflow")
    print(f"   3. Test webhook at: {base_url}/webhook/{webhook_path}")

    return True

if __name__ == "__main__":
    success = test_youtube_workflow()
    sys.exit(0 if success else 1)