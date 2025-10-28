#!/bin/bash

# n8n Workflow Agent Quick Start Script
# 快速启动和配置脚本

set -e

echo "=========================================="
echo "n8n Workflow Agent - Quick Start"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python版本
check_python() {
    echo "🔍 Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

        # 检查版本是否>=3.8
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3,8) else 1)'; then
            echo -e "${GREEN}✓${NC} Python version is compatible"
        else
            echo -e "${RED}✗${NC} Python 3.8+ is required"
            exit 1
        fi
    else
        echo -e "${RED}✗${NC} Python3 not found. Please install Python 3.8+"
        exit 1
    fi
}

# 安装依赖
install_dependencies() {
    echo ""
    echo "📦 Installing dependencies..."

    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt --quiet
        echo -e "${GREEN}✓${NC} Dependencies installed"
    else
        echo -e "${RED}✗${NC} requirements.txt not found"
        exit 1
    fi
}

# 配置环境
setup_environment() {
    echo ""
    echo "⚙️  Setting up environment..."

    # 检查.env文件
    if [ ! -f "config/.env" ]; then
        if [ -f "config/.env.example" ]; then
            cp config/.env.example config/.env
            echo -e "${YELLOW}!${NC} Created config/.env from template"
            echo "   Please edit config/.env and set your n8n API key"
        else
            echo -e "${RED}✗${NC} config/.env.example not found"
            exit 1
        fi
    else
        echo -e "${GREEN}✓${NC} config/.env already exists"
    fi

    # 创建必要的目录
    mkdir -p logs data backups temp
    echo -e "${GREEN}✓${NC} Created necessary directories"
}

# 测试n8n连接
test_connection() {
    echo ""
    echo "🔌 Testing n8n connection..."

    # 检查是否设置了API密钥
    if grep -q "your_api_key_here" config/.env; then
        echo -e "${YELLOW}!${NC} n8n API key not configured"
        echo ""
        read -p "Enter your n8n API key (or press Enter to skip): " API_KEY

        if [ ! -z "$API_KEY" ]; then
            # 更新.env文件
            if [[ "$OSTYPE" == "darwin"* ]]; then
                # macOS
                sed -i '' "s/your_api_key_here/$API_KEY/" config/.env
            else
                # Linux
                sed -i "s/your_api_key_here/$API_KEY/" config/.env
            fi
            echo -e "${GREEN}✓${NC} API key configured"
        else
            echo -e "${YELLOW}!${NC} Skipping connection test"
            return
        fi
    fi

    # 测试连接
    python3 -c "
import sys
sys.path.append('.')
from tools.n8n_workflow_manager import N8nWorkflowManager
manager = N8nWorkflowManager()
if manager.test_connection():
    print('\033[0;32m✓\033[0m Successfully connected to n8n')
else:
    print('\033[0;31m✗\033[0m Failed to connect to n8n')
    print('  Please check your n8n instance is running and API key is correct')
" 2>/dev/null || echo -e "${YELLOW}!${NC} Connection test skipped"
}

# 运行示例
run_example() {
    echo ""
    echo "🎯 Would you like to run an example? (y/n)"
    read -p "> " RUN_EXAMPLE

    if [ "$RUN_EXAMPLE" = "y" ] || [ "$RUN_EXAMPLE" = "Y" ]; then
        echo ""
        echo "📋 Available examples:"
        echo "1. Create YouTube workflow"
        echo "2. Analyze existing workflow"
        echo "3. Run test suite"

        read -p "Select an example (1-3): " EXAMPLE

        case $EXAMPLE in
            1)
                echo "Running YouTube workflow example..."
                cd examples && python3 create_youtube_workflow.py
                ;;
            2)
                echo "Workflow analysis example..."
                if [ -f "templates/workflow_config.json" ]; then
                    python3 tools/workflow_analyzer.py templates/workflow_config.json
                else
                    echo -e "${RED}✗${NC} Template workflow not found"
                fi
                ;;
            3)
                echo "Running test suite..."
                if [ -f "templates/test_scenarios.json" ]; then
                    python3 tools/test_runner.py templates/test_scenarios.json --format markdown
                else
                    echo -e "${RED}✗${NC} Test scenarios not found"
                fi
                ;;
            *)
                echo "Invalid selection"
                ;;
        esac
    fi
}

# 显示下一步
show_next_steps() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ Setup Complete!${NC}"
    echo "=========================================="
    echo ""
    echo "📚 Next steps:"
    echo ""
    echo "1. Configure n8n connection:"
    echo "   nano config/.env"
    echo ""
    echo "2. Test connection:"
    echo "   python3 tools/n8n_workflow_manager.py test"
    echo ""
    echo "3. Create your first workflow:"
    echo "   python3 examples/create_youtube_workflow.py"
    echo ""
    echo "4. Read the documentation:"
    echo "   cat README.md"
    echo ""
    echo "5. Explore the analysis modules:"
    echo "   ls docs/"
    echo ""
    echo "For more help, see: https://github.com/ai-terminal/n8n-workflow-agent"
    echo ""
}

# 主流程
main() {
    # 切换到项目目录
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    cd "$SCRIPT_DIR/.."

    check_python
    install_dependencies
    setup_environment
    test_connection
    run_example
    show_next_steps
}

# 运行主流程
main