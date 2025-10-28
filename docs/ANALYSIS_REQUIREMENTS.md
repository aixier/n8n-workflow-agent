# 需求分析模块 Requirements Analysis Module

Version: 1.0.0
Module Type: AI Analysis
Parent: CLAUDE.md

## 模块职责 Module Responsibilities

本模块负责将用户的自然语言需求转换为结构化的工作流需求规格，是整个智能体系统的第一步。

## 分析流程 Analysis Process

```
用户需求输入
    ↓
1. 需求解析 (Requirement Parsing)
    ├── 识别动词和动作
    ├── 提取数据源和目标
    ├── 确定触发条件
    └── 识别约束条件
    ↓
2. 业务逻辑分析 (Business Logic Analysis)
    ├── 流程步骤分解
    ├── 决策点识别
    ├── 异常情况处理
    └── 性能要求分析
    ↓
3. 数据需求分析 (Data Requirements)
    ├── 输入数据格式
    ├── 输出数据格式
    ├── 数据转换需求
    └── 数据验证规则
    ↓
4. 集成需求分析 (Integration Requirements)
    ├── 外部系统接口
    ├── API认证需求
    ├── Webhook配置
    └── 通知渠道
    ↓
输出: requirements_spec.json
```

## 需求分类 Requirement Categories

### Category 1: 数据处理类 (Data Processing)
**特征**: ETL, 数据转换, 报表生成
**常见需求**:
- "从数据库导出数据到Excel"
- "合并多个CSV文件"
- "清洗和格式化数据"

**分析要点**:
```json
{
  "data_source": "数据来源",
  "data_format": "数据格式",
  "transformation": "转换规则",
  "output_format": "输出格式",
  "schedule": "执行频率"
}
```

### Category 2: 自动化通知类 (Automated Notifications)
**特征**: 监控, 告警, 通知
**常见需求**:
- "监控网站状态并告警"
- "新订单自动发送通知"
- "定时发送报告"

**分析要点**:
```json
{
  "trigger": "触发条件",
  "monitoring_target": "监控目标",
  "notification_channel": "通知渠道",
  "recipients": "接收人",
  "message_template": "消息模板"
}
```

### Category 3: 内容处理类 (Content Processing)
**特征**: 文件处理, 内容生成, 媒体处理
**常见需求**:
- "YouTube视频转文章"
- "批量图片压缩"
- "文档格式转换"

**分析要点**:
```json
{
  "content_type": "内容类型",
  "processing_steps": "处理步骤",
  "quality_settings": "质量设置",
  "output_destination": "输出位置"
}
```

### Category 4: 系统集成类 (System Integration)
**特征**: API连接, 系统同步, 数据迁移
**常见需求**:
- "同步CRM和邮件系统"
- "GitHub自动部署"
- "多平台数据同步"

**分析要点**:
```json
{
  "source_system": "源系统",
  "target_system": "目标系统",
  "sync_frequency": "同步频率",
  "mapping_rules": "映射规则",
  "conflict_resolution": "冲突处理"
}
```

## 需求解析规则 Parsing Rules

### Rule 1: 动作识别 (Action Recognition)
```javascript
const actionKeywords = {
  create: ["创建", "生成", "新建", "制作"],
  read: ["读取", "获取", "查询", "监控"],
  update: ["更新", "修改", "编辑", "同步"],
  delete: ["删除", "清理", "移除", "归档"],
  transform: ["转换", "处理", "格式化", "翻译"],
  notify: ["通知", "告警", "发送", "提醒"]
};
```

### Rule 2: 触发条件识别 (Trigger Recognition)
```javascript
const triggerPatterns = {
  schedule: ["每天", "每周", "每月", "定时", "定期"],
  webhook: ["当...时", "接收到", "触发", "调用"],
  manual: ["手动", "按需", "执行", "运行"],
  event: ["新增", "更新", "删除", "变化"]
};
```

### Rule 3: 数据源识别 (Data Source Recognition)
```javascript
const dataSourcePatterns = {
  database: ["数据库", "MySQL", "PostgreSQL", "MongoDB"],
  file: ["文件", "CSV", "Excel", "JSON", "XML"],
  api: ["API", "接口", "服务", "端点"],
  form: ["表单", "输入", "用户提交"],
  email: ["邮件", "邮箱", "收件箱"]
};
```

## 需求模板 Requirement Templates

### Template 1: 基础需求模板
```json
{
  "requirement_id": "REQ_001",
  "title": "需求标题",
  "description": "详细描述",
  "category": "数据处理|通知|内容|集成",
  "priority": "high|medium|low",
  "trigger": {
    "type": "schedule|webhook|manual|event",
    "config": {}
  },
  "process": {
    "steps": [],
    "conditions": [],
    "error_handling": {}
  },
  "data": {
    "input": {},
    "output": {},
    "transformation": {}
  },
  "integration": {
    "systems": [],
    "apis": [],
    "credentials": []
  }
}
```

### Template 2: YouTube2Post需求示例
```json
{
  "requirement_id": "REQ_YT2P",
  "title": "YouTube视频转文章",
  "description": "下载YouTube视频，提取字幕，生成文章",
  "category": "内容处理",
  "priority": "high",
  "trigger": {
    "type": "webhook",
    "config": {
      "method": "POST",
      "path": "/youtube2post"
    }
  },
  "process": {
    "steps": [
      "验证URL",
      "下载视频",
      "提取字幕",
      "AI分析",
      "生成文章",
      "截图"
    ],
    "conditions": [
      "URL必须是YouTube",
      "视频长度<60分钟"
    ],
    "error_handling": {
      "retry": 3,
      "fallback": "返回错误信息"
    }
  },
  "data": {
    "input": {
      "url": "string",
      "language": "string",
      "template": "string"
    },
    "output": {
      "article": "markdown",
      "quotes": "array",
      "screenshots": "array"
    }
  },
  "integration": {
    "systems": ["YouTube", "Qwen AI"],
    "apis": ["yt-dlp", "DashScope"],
    "credentials": ["QWEN_API_KEY"]
  }
}
```

## 分析步骤详解 Detailed Analysis Steps

### Step 1: 需求分解 (Requirement Decomposition)
```
输入: "创建一个每天早上9点从数据库导出昨日订单并发送邮件的工作流"

分解结果:
1. 触发器: 每天早上9点 (Schedule Trigger)
2. 数据源: 数据库 (Database Query)
3. 数据范围: 昨日订单 (Date Filter)
4. 处理: 导出 (Data Export)
5. 输出: 发送邮件 (Email Send)

关键参数:
- cron: "0 9 * * *"
- query: "SELECT * FROM orders WHERE date = YESTERDAY"
- format: "CSV/Excel"
- recipients: [待确定]
```

### Step 2: 依赖关系分析 (Dependency Analysis)
```
节点依赖链:
Schedule → Database → Transform → Email
    ↓         ↓          ↓         ↓
  触发    查询数据    格式转换   发送

数据依赖:
- Database需要: 连接信息, 查询语句
- Transform需要: 输入数据, 转换规则
- Email需要: 文件附件, 收件人, 模板
```

### Step 3: 异常处理设计 (Error Handling Design)
```
可能的异常:
1. 数据库连接失败 → 重试3次 → 发送告警
2. 查询结果为空 → 发送"无数据"通知
3. 邮件发送失败 → 使用备用SMTP → 记录日志
4. 超时 → 终止执行 → 发送超时通知
```

## 输出格式 Output Format

### 最终输出: requirements_spec.json
```json
{
  "meta": {
    "version": "1.0.0",
    "created_at": "2025-01-28T10:00:00Z",
    "analyst": "AI Requirements Analyzer",
    "confidence": 0.95
  },
  "requirement": {
    "id": "REQ_20250128_001",
    "title": "订单日报自动化",
    "description": "每日自动导出订单并邮件发送",
    "category": "数据处理+通知",
    "priority": "high"
  },
  "workflow": {
    "name": "daily_order_report",
    "description": "Daily order report automation",
    "trigger": {
      "type": "schedule",
      "cron": "0 9 * * *",
      "timezone": "Asia/Shanghai"
    },
    "nodes": [
      {
        "id": "trigger_1",
        "type": "schedule",
        "name": "每天9点触发"
      },
      {
        "id": "db_1",
        "type": "postgres",
        "name": "查询订单数据",
        "config": {
          "operation": "select",
          "query": "SELECT * FROM orders WHERE created_at >= NOW() - INTERVAL '1 day'"
        }
      },
      {
        "id": "transform_1",
        "type": "spreadsheet",
        "name": "转换为Excel",
        "config": {
          "operation": "create",
          "format": "xlsx"
        }
      },
      {
        "id": "email_1",
        "type": "email",
        "name": "发送邮件",
        "config": {
          "subject": "每日订单报告 - {{date}}",
          "attachments": true
        }
      }
    ],
    "connections": [
      ["trigger_1", "db_1"],
      ["db_1", "transform_1"],
      ["transform_1", "email_1"]
    ]
  },
  "validation": {
    "required_credentials": ["postgres", "smtp"],
    "required_nodes": ["schedule", "postgres", "spreadsheet", "email"],
    "estimated_runtime": "30-60 seconds",
    "test_data_available": true
  },
  "risks": [
    {
      "type": "performance",
      "description": "大数据量可能导致超时",
      "mitigation": "添加分页查询"
    },
    {
      "type": "security",
      "description": "数据库凭证暴露风险",
      "mitigation": "使用环境变量"
    }
  ]
}
```

## 分析约束 Analysis Constraints

### ✅ 必须执行的分析
1. 完整性检查: 确保所有必需参数都已识别
2. 可行性验证: 确认n8n支持所需功能
3. 安全性评估: 识别潜在安全风险
4. 性能预估: 评估执行时间和资源需求

### ❌ 禁止的操作
1. 不能假设未明确的需求
2. 不能忽略错误处理
3. 不能跳过依赖关系分析
4. 不能省略测试数据设计

## 常见需求模式 Common Requirement Patterns

### Pattern 1: ETL模式
```
触发 → 提取 → 转换 → 加载 → 通知
Schedule → Database → Transform → Database → Email
```

### Pattern 2: 监控告警模式
```
触发 → 检查 → 判断 → 告警
Schedule → HTTP Request → IF → Slack/Email
```

### Pattern 3: 文件处理模式
```
触发 → 读取 → 处理 → 保存 → 通知
Webhook → Read File → Process → Save → Notify
```

### Pattern 4: API集成模式
```
触发 → 认证 → 调用 → 处理 → 响应
Webhook → OAuth2 → API Call → Transform → Response
```

## 质量检查清单 Quality Checklist

- [ ] 需求描述是否清晰完整？
- [ ] 所有输入输出是否已定义？
- [ ] 触发条件是否明确？
- [ ] 错误处理是否完善？
- [ ] 性能要求是否可达？
- [ ] 安全需求是否满足？
- [ ] 测试用例是否完整？
- [ ] 文档是否充分？

## 与其他模块的接口 Interface with Other Modules

### 输出到: ANALYSIS_NODES.md
```json
{
  "required_nodes": ["schedule", "postgres", "email"],
  "node_count": 4,
  "complexity": "medium"
}
```

### 输出到: ANALYSIS_DATAFLOW.md
```json
{
  "data_flow": "linear",
  "data_formats": ["sql_result", "xlsx", "email"],
  "transformations": ["sql_to_spreadsheet"]
}
```

### 输出到: ANALYSIS_TESTING.md
```json
{
  "test_scenarios": 3,
  "test_data_required": true,
  "performance_baseline": "60s"
}
```

---

**模块状态**: Active
**下一步**: 执行 ANALYSIS_NODES.md