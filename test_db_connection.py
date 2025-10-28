#!/usr/bin/env python3
"""
Test Database Connection
测试数据库连接是否正常
"""

import os
import sys
from pathlib import Path

# 尝试导入 psycopg2 或其他 PostgreSQL 库
try:
    import psycopg2
    has_psycopg2 = True
except ImportError:
    has_psycopg2 = False
    print("⚠️  psycopg2 not installed. Run: pip install psycopg2-binary")

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

def test_connection():
    """测试数据库连接"""
    config = load_env()

    print("📊 Database Configuration:")
    print(f"   Host: {config.get('DATABASE_HOST', 'N/A')}")
    print(f"   Port: {config.get('DATABASE_PORT', 'N/A')}")
    print(f"   Database: {config.get('DATABASE_NAME', 'N/A')}")
    print(f"   User: {config.get('DATABASE_USER', 'N/A')}")
    print(f"   Password: {'*' * len(config.get('DATABASE_PASSWORD', '')) if config.get('DATABASE_PASSWORD') else 'N/A'}")
    print()

    if not has_psycopg2:
        print("❌ Cannot test connection - psycopg2 not installed")
        print("   Install it with: pip install psycopg2-binary")
        return False

    try:
        # 连接数据库
        print("🔄 Testing connection...")
        conn = psycopg2.connect(
            host=config.get('DATABASE_HOST', 'localhost'),
            port=config.get('DATABASE_PORT', '5432'),
            database=config.get('DATABASE_NAME', 'n8n'),
            user=config.get('DATABASE_USER', 'n8n'),
            password=config.get('DATABASE_PASSWORD', '')
        )

        # 测试查询
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        print("✅ Connection successful!")
        print(f"   PostgreSQL version: {version}")

        # 检查表
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        print(f"   Tables in database: {table_count}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("n8n Workflow Agent - Database Connection Test")
    print("=" * 60)
    print()

    success = test_connection()

    print()
    print("=" * 60)
    if success:
        print("🎉 Database is ready for n8n Workflow Agent!")
    else:
        print("⚠️  Please check your database configuration")
    print("=" * 60)

    sys.exit(0 if success else 1)