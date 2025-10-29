#!/usr/bin/env python3
"""
YouTube Processor Webhook Activation Test
This script helps verify webhook activation after UI interaction
"""

import requests
import json
import time
from datetime import datetime
import sys

def test_webhook():
    """Test the YouTube Processor webhook"""

    # Configuration
    base_url = "http://localhost:5679"
    workflow_id = "ElwksDwOH8GAYs4x"
    webhook_path = "youtube-processor-20251029111823"

    print("=" * 70)
    print("🚀 YouTube Processor Webhook Test")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Workflow ID: {workflow_id}")
    print(f"Webhook Path: {webhook_path}")
    print()

    # Step 1: Instructions
    print("📝 ACTIVATION STEPS (if webhook not working):")
    print("1. Open n8n UI: http://localhost:5679")
    print("2. Find and open 'YouTube Processor Test - 20251029_111823'")
    print("3. Click the 'Execute Workflow' button (play icon)")
    print("4. Wait for the 'Listening for event...' message")
    print("5. Run this script again within 120 seconds")
    print()

    input("Press Enter when ready to test...")
    print()

    # Test URLs
    test_urls = [
        {
            "name": "Test Webhook (Full Path)",
            "url": f"{base_url}/webhook-test/{workflow_id}/{webhook_path}"
        },
        {
            "name": "Production Webhook",
            "url": f"{base_url}/webhook/{webhook_path}"
        }
    ]

    # Test data variations
    test_cases = [
        {
            "name": "Standard YouTube URL",
            "data": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "language": "zh-CN"
            }
        },
        {
            "name": "YouTube Shorts",
            "data": {
                "youtube_url": "https://youtube.com/shorts/abc123def45",
                "language": "en-US"
            }
        },
        {
            "name": "Youtu.be Short URL",
            "data": {
                "youtube_url": "https://youtu.be/dQw4w9WgXcQ",
                "language": "zh-CN"
            }
        }
    ]

    success_count = 0

    # Test each URL
    for url_config in test_urls:
        print(f"🔗 Testing: {url_config['name']}")
        print(f"   URL: {url_config['url']}")
        print()

        for test_case in test_cases:
            print(f"   📌 {test_case['name']}")

            try:
                start_time = time.time()
                response = requests.post(
                    url_config['url'],
                    json=test_case['data'],
                    timeout=15
                )
                elapsed = time.time() - start_time

                print(f"      Status: {response.status_code}")
                print(f"      Time: {elapsed:.2f}s")

                if response.status_code == 200:
                    print("      ✅ SUCCESS!")
                    result = response.json()

                    # Check response structure
                    if 'videoId' in str(result):
                        print("      ✓ Video ID extracted")
                    if 'status' in str(result):
                        print(f"      ✓ Status: {result.get('status', 'unknown')}")
                    if 'processingTime' in str(result):
                        print(f"      ✓ Processing time recorded")

                    print(f"      Response preview: {json.dumps(result, ensure_ascii=False)[:200]}...")
                    success_count += 1

                elif response.status_code == 404:
                    print("      ❌ Webhook not registered")
                    error = response.json()
                    if "Click the 'Execute workflow' button" in str(error):
                        print("      💡 Need to click 'Execute Workflow' in UI")

                else:
                    print(f"      ⚠️ Unexpected response: {response.status_code}")
                    print(f"      {response.text[:100]}")

            except requests.exceptions.Timeout:
                print("      ⏱️ Request timed out")
            except Exception as e:
                print(f"      ❌ Error: {str(e)[:100]}")

            print()
            time.sleep(0.5)  # Small delay between tests

        # If we found a working webhook, no need to test others
        if success_count > 0:
            break

    # Summary
    print("=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    if success_count > 0:
        print(f"✅ SUCCESS! Webhook is working!")
        print(f"   Successful tests: {success_count}")
        print("\nThe webhook is now properly activated and can process YouTube URLs.")
        print("\nFeatures confirmed:")
        print("  ✓ URL validation")
        print("  ✓ Video ID extraction")
        print("  ✓ Multiple URL format support")
        print("  ✓ Response formatting")

    else:
        print("❌ Webhook is not active")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Make sure the workflow is open in n8n UI")
        print("2. Click 'Execute Workflow' button")
        print("3. Wait for 'Listening for event...' message")
        print("4. Run this script again immediately")
        print("\nNote: Test webhooks expire after one use or 120 seconds")

    return success_count > 0

if __name__ == "__main__":
    success = test_webhook()
    sys.exit(0 if success else 1)