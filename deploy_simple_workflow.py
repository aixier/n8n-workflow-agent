#!/usr/bin/env python3
"""
Deploy the simplified YouTube2Post workflow to n8n
This version works with standard n8n nodes without external dependencies
"""

import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/.env')

def deploy_workflow():
    """Deploy the simplified YouTube2Post workflow to n8n"""

    # Get n8n configuration
    n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5679')
    api_key = os.getenv('N8N_API_KEY')

    if not api_key:
        print("❌ Error: N8N_API_KEY not found in environment")
        return False

    # Load the simplified workflow
    with open('youtube2post_simple_workflow.json', 'r') as f:
        workflow = json.load(f)

    # Prepare API request
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    # Clean workflow for API (remove read-only fields)
    fields_to_remove = ['id', 'createdAt', 'updatedAt', 'versionId', 'active']
    for field in fields_to_remove:
        if field in workflow:
            del workflow[field]

    # Create the workflow
    print(f"📤 Deploying simplified workflow to {n8n_url}...")

    try:
        response = requests.post(
            f"{n8n_url}/api/v1/workflows",
            headers=headers,
            json=workflow
        )

        if response.status_code in [200, 201]:
            result = response.json()
            workflow_id = result.get('id')
            print(f"✅ Workflow deployed successfully!")
            print(f"📋 Workflow ID: {workflow_id}")
            print(f"🔗 Workflow URL: {n8n_url}/workflow/{workflow_id}")

            # Try to activate using PUT with full workflow data
            print("\n🔄 Attempting to activate workflow...")

            # Get the current workflow data
            get_response = requests.get(
                f"{n8n_url}/api/v1/workflows/{workflow_id}",
                headers=headers
            )

            if get_response.status_code == 200:
                workflow_data = get_response.json()
                workflow_data['active'] = True

                # Update workflow with active=true
                activate_response = requests.put(
                    f"{n8n_url}/api/v1/workflows/{workflow_id}",
                    headers=headers,
                    json=workflow_data
                )

                if activate_response.status_code == 200:
                    print("✅ Workflow activated successfully!")
                    print(f"\n🎯 Webhook URL: {n8n_url}/webhook/youtube2post-simple")
                else:
                    print(f"⚠️  Could not activate workflow automatically")
                    print(f"    Please activate it manually in the n8n UI")
                    print(f"    Response: {activate_response.status_code}")

            return workflow_id

        else:
            print(f"❌ Failed to deploy workflow")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error deploying workflow: {e}")
        return None

def test_workflow(workflow_id=None):
    """Provide test instructions for the deployed workflow"""
    n8n_url = os.getenv('N8N_BASE_URL', 'http://localhost:5679')

    print("\n" + "="*60)
    print("🧪 Test Instructions")
    print("="*60)

    print("\n1️⃣  First, activate the workflow in n8n UI:")
    print(f"   {n8n_url}/workflow/{workflow_id if workflow_id else 'YOUR_WORKFLOW_ID'}")
    print("   Click the 'Active' toggle in the top-right corner")

    print("\n2️⃣  Then test with this command:")
    print(f"""
curl -X POST {n8n_url}/webhook/youtube2post-simple \\
  -H "Content-Type: application/json" \\
  -d '{{
    "youtube_url": "https://youtube.com/shorts/rLhoe1ZjW-s",
    "language": "zh-CN"
  }}'
""")

    print("\n3️⃣  Expected response:")
    print("""
{
  "success": true,
  "data": {
    "videoId": "rLhoe1ZjW-s",
    "quotes": [...],
    "metadata": {...}
  },
  "message": "Successfully processed video..."
}
""")

def main():
    print("🚀 YouTube2Post Simple Workflow Deployer")
    print("="*50)
    print("This deploys a working version without external dependencies\n")

    workflow_id = deploy_workflow()

    if workflow_id:
        test_workflow(workflow_id)
        print("\n✨ Deployment complete!")
        print("📝 Note: This is a simplified version for testing.")
        print("    It returns mock data instead of actual video processing.")
        return 0
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit(main())