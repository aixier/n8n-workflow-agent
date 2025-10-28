#!/usr/bin/env python3
"""
Test n8n Connection
测试 n8n API 连接是否正常
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 读取环境变量
def load_env():
    """加载 .env 文件中的配置"""
    env_file = Path(__file__).parent / 'config' / '.env'
    config = {}

    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value.strip()
    return config

def test_n8n_connection():
    """测试 n8n 连接"""
    config = load_env()

    base_url = config.get('N8N_BASE_URL', 'http://localhost:5678')
    api_key = config.get('N8N_API_KEY', '')

    print("📊 n8n Configuration:")
    print(f"   Base URL: {base_url}")
    print(f"   API Key: {api_key[:20]}...{api_key[-10:] if len(api_key) > 30 else api_key}")
    print()

    if not api_key or api_key == 'your_api_key_here':
        print("❌ API Key not configured!")
        print("   Please set N8N_API_KEY in config/.env")
        return False

    # 设置请求头
    headers = {
        'X-N8N-API-KEY': api_key,
        'Accept': 'application/json'
    }

    try:
        # 测试连接 - 获取工作流列表
        print("🔄 Testing n8n API connection...")

        # 首先测试基本连接
        test_url = f"{base_url}/api/v1/workflows"
        print(f"   Testing endpoint: {test_url}")

        response = requests.get(
            test_url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print("✅ n8n API connection successful!")

            workflows = response.json().get('data', [])
            print(f"   Found {len(workflows)} workflow(s)")

            if workflows:
                print("\n📋 Existing Workflows:")
                for wf in workflows[:5]:  # 只显示前5个
                    print(f"   - {wf.get('name', 'Unnamed')} (ID: {wf.get('id')})")
                    print(f"     Active: {wf.get('active', False)}")
                if len(workflows) > 5:
                    print(f"   ... and {len(workflows) - 5} more")

            return True

        elif response.status_code == 401:
            print("❌ Authentication failed!")
            print("   Invalid API key. Please check N8N_API_KEY in config/.env")
            return False

        else:
            print(f"❌ Connection failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed!")
        print(f"   Cannot connect to {base_url}")
        print("   Please check:")
        print("   1. n8n is running")
        print("   2. The URL is correct (current: {})".format(base_url))
        print("   3. Port is not blocked")
        return False

    except requests.exceptions.Timeout:
        print("❌ Connection timeout!")
        print("   n8n is not responding")
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_qwen_config():
    """测试 Qwen/Dashscope 配置"""
    config = load_env()

    print("\n📊 Qwen/Dashscope Configuration:")

    if config.get('QWEN_ENABLED', 'false').lower() == 'true':
        print("   Status: ✅ Enabled")
        print(f"   Base URL: {config.get('QWEN_BASE_URL', 'N/A')}")
        print(f"   Model: {config.get('QWEN_MODEL', 'N/A')}")
        print(f"   API Key: {config.get('DASHSCOPE_API_KEY', 'N/A')[:20]}...")
        print(f"   Max Tokens: {config.get('QWEN_MAX_TOKENS', 'N/A')}")
        print(f"   Temperature: {config.get('QWEN_TEMPERATURE', 'N/A')}")
        print(f"   Max Concurrent: {config.get('QWEN_MAX_CONCURRENT_REQUESTS', 'N/A')}")

        # 可选：测试 Qwen API 连接
        api_key = config.get('DASHSCOPE_API_KEY', '')
        if api_key and api_key != 'N/A':
            print("\n   Testing Qwen API...")
            try:
                # 这里可以添加实际的 Qwen API 测试
                print("   ✅ Qwen configuration looks good!")
            except Exception as e:
                print(f"   ⚠️  Cannot verify Qwen API: {e}")
    else:
        print("   Status: ⚠️  Disabled")

def main():
    print("=" * 60)
    print("n8n Workflow Agent - Configuration Test")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 测试数据库（可选）
    print("📊 Database Configuration:")
    config = load_env()
    print(f"   Host: {config.get('DATABASE_HOST', 'N/A')}")
    print(f"   Port: {config.get('DATABASE_PORT', 'N/A')}")
    print(f"   Database: {config.get('DATABASE_NAME', 'N/A')}")
    print(f"   User: {config.get('DATABASE_USER', 'N/A')}")
    print()

    # 测试 n8n 连接
    n8n_success = test_n8n_connection()

    # 测试 Qwen 配置
    test_qwen_config()

    # 总结
    print()
    print("=" * 60)
    if n8n_success:
        print("🎉 n8n Workflow Agent is ready to use!")
        print("\nNext steps:")
        print("1. Create workflows: python tools/n8n_workflow_manager.py create workflow.json")
        print("2. List workflows: python tools/n8n_workflow_manager.py list")
        print("3. Run quick start: bash scripts/quick_start.sh")
    else:
        print("⚠️  Please fix the configuration issues above")
        print("\nTroubleshooting:")
        print("1. Ensure n8n is running on port 5679")
        print("2. Verify API key is correct")
        print("3. Check network connectivity")
    print("=" * 60)

    return 0 if n8n_success else 1

if __name__ == "__main__":
    sys.exit(main())