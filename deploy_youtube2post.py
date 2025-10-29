#!/usr/bin/env python3
"""
Deploy YouTube2Post workflow to n8n
"""

import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

def deploy_workflow():
    """Deploy the YouTube2Post workflow to n8n"""

    # Get n8n configuration
    n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5679')
    api_key = os.getenv('N8N_API_KEY')

    if not api_key:
        print("❌ Error: N8N_API_KEY not found in environment")
        return False

    # Load the workflow
    with open('youtube2post_workflow.json', 'r') as f:
        workflow = json.load(f)

    # Prepare API request
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    # Remove fields that n8n doesn't accept in creation
    fields_to_remove = ['id', 'updatedAt', 'createdAt', 'versionId', 'triggerCount', 'tags', 'staticData']
    for field in fields_to_remove:
        if field in workflow:
            del workflow[field]

    # Fix settings to only include valid properties
    if 'settings' in workflow:
        valid_settings = {}
        if 'saveDataSuccessExecution' in workflow['settings']:
            valid_settings['saveDataSuccessExecution'] = workflow['settings']['saveDataSuccessExecution']
        if 'saveExecutionProgress' in workflow['settings']:
            valid_settings['saveExecutionProgress'] = workflow['settings']['saveExecutionProgress']
        if 'saveManualExecutions' in workflow['settings']:
            valid_settings['saveManualExecutions'] = workflow['settings']['saveManualExecutions']
        workflow['settings'] = valid_settings

    # Create the workflow
    print(f"📤 Deploying workflow to {n8n_url}...")

    try:
        response = requests.post(
            f"{n8n_url}/api/v1/workflows",
            headers=headers,
            json=workflow
        )

        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            workflow_id = result.get('id')
            print(f"✅ Workflow deployed successfully!")
            print(f"📋 Workflow ID: {workflow_id}")
            print(f"🔗 Workflow URL: {n8n_url}/workflow/{workflow_id}")

            # Activate the workflow
            print("\n🔄 Activating workflow...")
            activate_response = requests.patch(
                f"{n8n_url}/api/v1/workflows/{workflow_id}",
                headers=headers,
                json={"active": True}
            )

            if activate_response.status_code == 200:
                print("✅ Workflow activated!")
                print(f"\n🎯 Webhook URL: {n8n_url}/webhook/youtube2post")
                return True
            else:
                print(f"⚠️ Could not activate workflow: {activate_response.text}")
                return True  # Workflow created but not activated

        else:
            print(f"❌ Failed to deploy workflow")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error deploying workflow: {e}")
        return False

def test_workflow():
    """Test the deployed workflow"""
    n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5679')

    print("\n🧪 Testing workflow...")
    print("You can test the workflow with:")
    print(f"""
curl -X POST {n8n_url}/webhook/youtube2post \\
  -H "Content-Type: application/json" \\
  -d '{{"youtube_url": "https://youtu.be/bJFtcwLSNxI", "language": "zh-CN"}}'
    """)

if __name__ == "__main__":
    if deploy_workflow():
        test_workflow()
        print("\n✨ YouTube2Post workflow is ready to use!")