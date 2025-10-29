#!/usr/bin/env python3
"""
Test Active YouTube Webhook Endpoints
"""

import requests
import json
import time
from datetime import datetime

def test_webhook(name, url, test_data):
    """Test a single webhook endpoint"""
    print(f"\n📌 Testing: {name}")
    print(f"   URL: {url}")
    print(f"   Payload: {json.dumps(test_data, ensure_ascii=False)}")

    try:
        start_time = time.time()
        response = requests.post(url, json=test_data, timeout=15)
        elapsed_time = time.time() - start_time

        print(f"   Status Code: {response.status_code}")
        print(f"   Response Time: {elapsed_time:.2f}s")

        if response.status_code == 200:
            print(f"   ✅ SUCCESS!")
            result = response.json()
            print(f"   Response Preview: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
            return True, result
        elif response.status_code == 404:
            print(f"   ❌ WEBHOOK NOT FOUND")
            print(f"   Message: {response.text[:200]}")
            return False, response.text
        else:
            print(f"   ⚠️ UNEXPECTED RESPONSE: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return False, response.text

    except requests.exceptions.Timeout:
        print(f"   ⏱️ REQUEST TIMEOUT (>15s)")
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        print(f"   ❌ CONNECTION ERROR")
        return False, "Connection Error"
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)[:200]}")
        return False, str(e)

def main():
    """Main test execution"""
    print("=" * 70)
    print("🧪 YouTube Webhook Testing Suite")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")

    base_url = "http://localhost:5679"

    # Define test cases
    test_cases = [
        {
            "name": "YouTube2Post Simple - Working Version",
            "url": f"{base_url}/webhook/youtube2post-simple",
            "active": True
        },
        {
            "name": "YouTube Processor Test",
            "url": f"{base_url}/webhook/youtube-processor-20251029111823",
            "active": True
        },
        {
            "name": "YouTube2Post - Video to Article Generator",
            "url": f"{base_url}/webhook/youtube2post",
            "active": True
        }
    ]

    # Test data variations
    test_data_sets = [
        {
            "name": "Standard YouTube URL",
            "data": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "language": "zh-CN"
            }
        },
        {
            "name": "YouTube Shorts URL",
            "data": {
                "youtube_url": "https://youtube.com/shorts/abcdefghijk",
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

    results = []

    # Test each active webhook
    for webhook in test_cases:
        if not webhook["active"]:
            continue

        print(f"\n{'='*70}")
        print(f"🔧 Testing Webhook: {webhook['name']}")
        print(f"{'='*70}")

        webhook_results = []

        # Test with different data sets
        for test_data in test_data_sets:
            success, response = test_webhook(
                test_data["name"],
                webhook["url"],
                test_data["data"]
            )

            webhook_results.append({
                "test": test_data["name"],
                "success": success,
                "response": response
            })

            # Small delay between tests
            time.sleep(1)

        results.append({
            "webhook": webhook["name"],
            "url": webhook["url"],
            "tests": webhook_results
        })

    # Generate summary report
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY REPORT")
    print("=" * 70)

    total_tests = 0
    successful_tests = 0

    for result in results:
        print(f"\n📍 {result['webhook']}")
        for test in result["tests"]:
            total_tests += 1
            status = "✅" if test["success"] else "❌"
            print(f"   {status} {test['test']}")
            if test["success"]:
                successful_tests += 1

    print(f"\n📈 Overall Results:")
    print(f"   Total Tests: {total_tests}")
    print(f"   Successful: {successful_tests}")
    print(f"   Failed: {total_tests - successful_tests}")
    print(f"   Success Rate: {(successful_tests/total_tests*100):.1f}%")

    # Test with invalid data
    print("\n" + "=" * 70)
    print("🔒 ERROR HANDLING TEST")
    print("=" * 70)

    error_test_data = [
        {
            "name": "Missing YouTube URL",
            "data": {"language": "zh-CN"}
        },
        {
            "name": "Invalid YouTube URL",
            "data": {"youtube_url": "not-a-youtube-url", "language": "en-US"}
        },
        {
            "name": "Empty Request",
            "data": {}
        }
    ]

    # Test error handling on one active webhook
    if test_cases:
        active_webhook = test_cases[0]
        print(f"\nTesting error handling on: {active_webhook['name']}")

        for error_test in error_test_data:
            success, response = test_webhook(
                error_test["name"],
                active_webhook["url"],
                error_test["data"]
            )
            time.sleep(1)

    print("\n" + "=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()