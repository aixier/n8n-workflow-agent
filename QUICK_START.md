# 快速开始指南 Quick Start Guide 🚀

## 5分钟上手 n8n Workflow Agent

### 1️⃣ 一键安装和配置

```bash
cd /mnt/d/work/AI_Terminal/n8n-handbook/n8n-workflow-agent
bash scripts/quick_start.sh
```

### 2️⃣ 配置n8n连接

编辑 `config/.env`:

```env
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=你的API密钥
```

获取API密钥:
1. 打开n8n Web界面
2. 进入 Settings → API
3. 生成新的API密钥

### 3️⃣ 测试连接

```bash
python3 tools/n8n_workflow_manager.py test
```

## 🎯 常用命令速查

### 工作流管理

```bash
# 列出所有工作流
python3 tools/n8n_workflow_manager.py list

# 创建工作流
python3 tools/n8n_workflow_manager.py create workflow.json

# 激活工作流
python3 tools/n8n_workflow_manager.py deploy workflow_id

# 备份工作流
python3 tools/n8n_workflow_manager.py backup workflow_id
```

### 工作流分析

```bash
# 分析工作流
python3 tools/workflow_analyzer.py workflow.json

# 生成分析报告
python3 tools/workflow_analyzer.py workflow.json --output report.md
```

### 自动化测试

```bash
# 运行测试
python3 tools/test_runner.py test_suite.json

# 生成测试报告
python3 tools/test_runner.py test_suite.json --format html --output report.html
```

## 📝 快速创建工作流示例

### 方式1: 使用Python代码

```python
from tools.node_builder import NodeBuilder
from tools.n8n_workflow_manager import N8nWorkflowManager

# 创建节点
builder = NodeBuilder()
webhook = builder.build_webhook_node('/api/data')
process = builder.build_code_node('// Process data')
respond = builder.build_respond_node('json')

# 连接节点
builder.chain_nodes([webhook['id'], process['id'], respond['id']])

# 生成工作流
workflow = builder.build_workflow('My Workflow')

# 部署到n8n
manager = N8nWorkflowManager()
result = manager.create_workflow(workflow)
manager.deploy_workflow(result['id'])
```

### 方式2: 使用示例脚本

```bash
# 运行YouTube工作流示例
python3 examples/create_youtube_workflow.py
```

## 🔍 智能分析工作流程

### 1. AI分析需求

用户输入: "创建一个每天备份数据库的工作流"

AI分析输出:
- 触发器: Schedule (每天)
- 节点: Database → Backup → Notification
- 数据流: SQL → File → Email

### 2. 自动生成配置

```json
{
  "trigger": "schedule",
  "schedule": "0 2 * * *",
  "nodes": ["postgres", "write_file", "email"],
  "connections": [...]
}
```

### 3. 部署和测试

```bash
# 自动部署
python3 deploy_from_config.py config.json

# 自动测试
python3 run_tests.py workflow_id
```

## 📊 查看分析报告

```bash
# 生成完整分析
python3 tools/workflow_analyzer.py workflow.json

# 输出示例:
# ✅ Complexity: Medium (Score: 8)
# ⚠️  Performance Issues: 2
# 💡 Optimizations: 3
# 🔒 Security Checks: Passed
```

## 🛠️ 常见问题解决

### 问题1: 连接失败

```bash
# 检查n8n是否运行
curl http://localhost:5678/healthz

# 检查API密钥
cat config/.env | grep N8N_API_KEY
```

### 问题2: 导入错误

```bash
# 安装依赖
pip3 install -r requirements.txt

# 检查Python路径
python3 -c "import sys; print(sys.path)"
```

### 问题3: 权限问题

```bash
# 添加执行权限
chmod +x scripts/*.sh

# 创建必要目录
mkdir -p logs data backups temp
```

## 📚 深入学习

1. **阅读核心文档**:
   - [完整README](README.md)
   - [主智能体文档](docs/CLAUDE.md)
   - [分析模块文档](docs/)

2. **查看示例**:
   - [创建YouTube工作流](examples/create_youtube_workflow.py)
   - [工作流模板](templates/workflow_config.json)
   - [测试场景](templates/test_scenarios.json)

3. **学习API**:
   - [工作流管理器API](tools/n8n_workflow_manager.py)
   - [节点构建器API](tools/node_builder.py)
   - [测试运行器API](tools/test_runner.py)

## 🎉 恭喜!

现在您已经掌握了n8n Workflow Agent的基本使用方法。

**下一步建议**:
1. 尝试创建自己的工作流
2. 运行分析工具优化现有工作流
3. 编写自动化测试确保质量

需要帮助? 查看 [README.md](README.md) 或联系支持团队。

---
**Happy Workflow Building! 🚀**