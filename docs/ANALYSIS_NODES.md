# 节点分析模块 Node Analysis Module

Version: 1.0.0
Module Type: AI Analysis
Parent: CLAUDE.md
Previous: ANALYSIS_REQUIREMENTS.md

## 模块职责 Module Responsibilities

本模块负责根据需求规格选择合适的n8n节点，配置节点参数，设计节点连接关系。

## n8n节点分类体系 Node Classification System

### 1. 触发器节点 (Trigger Nodes)
```javascript
const triggerNodes = {
  // 时间触发
  "schedule": {
    name: "Schedule Trigger",
    use_case: "定时执行",
    config: { cron: "* * * * *", timezone: "UTC" }
  },

  // Web触发
  "webhook": {
    name: "Webhook",
    use_case: "接收HTTP请求",
    config: { path: "/webhook", method: "POST", responseMode: "lastNode" }
  },

  // 表单触发
  "form": {
    name: "Form Trigger",
    use_case: "Web表单输入",
    config: { formFields: [], formTitle: "", formDescription: "" }
  },

  // 邮件触发
  "emailTrigger": {
    name: "Email Trigger (IMAP)",
    use_case: "接收邮件",
    config: { pollInterval: 1, simple: true }
  },

  // 文件触发
  "fileTrigger": {
    name: "Local File Trigger",
    use_case: "监控文件变化",
    config: { path: "", events: ["create", "change"] }
  }
};
```

### 2. 数据节点 (Data Nodes)
```javascript
const dataNodes = {
  // 数据库
  "postgres": {
    name: "PostgreSQL",
    operations: ["select", "insert", "update", "delete"],
    config: { database: "", query: "" }
  },

  "mysql": {
    name: "MySQL",
    operations: ["select", "insert", "update", "delete"],
    config: { database: "", query: "" }
  },

  "mongodb": {
    name: "MongoDB",
    operations: ["find", "insert", "update", "delete"],
    config: { collection: "", query: {} }
  },

  // 文件系统
  "readBinaryFile": {
    name: "Read Binary File",
    use_case: "读取文件",
    config: { filePath: "", dataPropertyName: "data" }
  },

  "writeBinaryFile": {
    name: "Write Binary File",
    use_case: "写入文件",
    config: { fileName: "", dataPropertyName: "data" }
  },

  // 云存储
  "s3": {
    name: "AWS S3",
    operations: ["upload", "download", "delete", "list"],
    config: { bucket: "", region: "" }
  }
};
```

### 3. 处理节点 (Processing Nodes)
```javascript
const processingNodes = {
  // 数据转换
  "set": {
    name: "Set",
    use_case: "设置字段值",
    config: { values: {}, options: {} }
  },

  "code": {
    name: "Code",
    use_case: "自定义JavaScript代码",
    config: { jsCode: "", nodeVersion: 1 }
  },

  "function": {
    name: "Function",
    use_case: "JavaScript函数",
    config: { functionCode: "" }
  },

  // 数据操作
  "merge": {
    name: "Merge",
    use_case: "合并数据",
    config: { mode: "append", joinMode: "inner" }
  },

  "splitInBatches": {
    name: "Split In Batches",
    use_case: "批量处理",
    config: { batchSize: 10, options: {} }
  },

  "filter": {
    name: "Filter",
    use_case: "过滤数据",
    config: { conditions: [], combineConditions: "all" }
  },

  // 格式转换
  "spreadsheet": {
    name: "Spreadsheet File",
    use_case: "Excel文件处理",
    config: { operation: "read", fileFormat: "xlsx" }
  },

  "xml": {
    name: "XML",
    use_case: "XML解析/生成",
    config: { mode: "jsonToXml", options: {} }
  },

  "html": {
    name: "HTML",
    use_case: "HTML处理",
    config: { operation: "extractHTMLContent" }
  }
};
```

### 4. 集成节点 (Integration Nodes)
```javascript
const integrationNodes = {
  // HTTP/API
  "httpRequest": {
    name: "HTTP Request",
    use_case: "API调用",
    config: {
      method: "GET",
      url: "",
      authentication: "none",
      responseFormat: "json"
    }
  },

  // 通信
  "email": {
    name: "Email",
    use_case: "发送邮件",
    config: {
      subject: "",
      emailType: "html",
      attachments: []
    }
  },

  "slack": {
    name: "Slack",
    use_case: "Slack消息",
    config: {
      channel: "",
      messageType: "text",
      blocks: []
    }
  },

  // AI服务
  "openAi": {
    name: "OpenAI",
    use_case: "AI文本处理",
    config: {
      resource: "chat",
      model: "gpt-3.5-turbo",
      messages: []
    }
  },

  // 版本控制
  "github": {
    name: "GitHub",
    use_case: "GitHub操作",
    operations: ["create", "get", "update", "delete"],
    config: { owner: "", repository: "", resource: "issue" }
  }
};
```

### 5. 控制流节点 (Control Flow Nodes)
```javascript
const controlFlowNodes = {
  "if": {
    name: "IF",
    use_case: "条件判断",
    config: { conditions: [], combineConditions: "all" }
  },

  "switch": {
    name: "Switch",
    use_case: "多分支判断",
    config: { mode: "expression", output: "allBranches" }
  },

  "loop": {
    name: "Loop Over Items",
    use_case: "循环处理",
    config: { options: {} }
  },

  "wait": {
    name: "Wait",
    use_case: "延时等待",
    config: { amount: 1, unit: "seconds" }
  },

  "stopAndError": {
    name: "Stop and Error",
    use_case: "错误处理",
    config: { errorMessage: "" }
  }
};
```

## 节点选择策略 Node Selection Strategy

### 策略1: 基于需求类型选择
```javascript
function selectNodesByRequirement(requirement) {
  const nodeSelection = {
    triggers: [],
    processors: [],
    outputs: []
  };

  // 根据触发类型选择
  switch(requirement.trigger.type) {
    case 'schedule':
      nodeSelection.triggers.push('schedule');
      break;
    case 'webhook':
      nodeSelection.triggers.push('webhook');
      break;
    case 'manual':
      nodeSelection.triggers.push('manualTrigger');
      break;
  }

  // 根据数据处理需求选择
  if (requirement.data.database) {
    nodeSelection.processors.push(requirement.data.database);
  }

  if (requirement.data.transformation) {
    nodeSelection.processors.push('code', 'set');
  }

  // 根据输出需求选择
  if (requirement.output.email) {
    nodeSelection.outputs.push('email');
  }

  return nodeSelection;
}
```

### 策略2: 基于数据流选择
```javascript
function selectNodesByDataFlow(dataFlow) {
  const nodes = [];

  dataFlow.forEach(step => {
    switch(step.type) {
      case 'fetch':
        nodes.push('httpRequest');
        break;
      case 'transform':
        nodes.push('code');
        break;
      case 'filter':
        nodes.push('filter');
        break;
      case 'store':
        nodes.push('postgres');
        break;
    }
  });

  return nodes;
}
```

## 节点配置模板 Node Configuration Templates

### Template 1: Webhook + Process + Response
```json
{
  "nodes": [
    {
      "id": "webhook_1",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "path": "={{$parameter[\"webhookPath\"]}}",
        "method": "POST",
        "responseMode": "responseNode",
        "options": {}
      }
    },
    {
      "id": "process_1",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [450, 300],
      "parameters": {
        "jsCode": "// Process incoming data\nconst items = $input.all();\nreturn items.map(item => ({\n  json: {\n    processed: true,\n    data: item.json\n  }\n}));"
      }
    },
    {
      "id": "respond_1",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1,
      "position": [650, 300],
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{$json}}",
        "options": {}
      }
    }
  ],
  "connections": {
    "webhook_1": {
      "main": [["process_1"]]
    },
    "process_1": {
      "main": [["respond_1"]]
    }
  }
}
```

### Template 2: Schedule + Database + Email
```json
{
  "nodes": [
    {
      "id": "schedule_1",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 300],
      "parameters": {
        "rule": {
          "interval": [{
            "triggerAtHour": 9,
            "triggerAtMinute": 0
          }]
        }
      }
    },
    {
      "id": "postgres_1",
      "type": "n8n-nodes-base.postgres",
      "position": [450, 300],
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM orders WHERE created_at >= NOW() - INTERVAL '1 day'",
        "options": {}
      }
    },
    {
      "id": "email_1",
      "type": "n8n-nodes-base.emailSend",
      "position": [650, 300],
      "parameters": {
        "fromEmail": "noreply@company.com",
        "toEmail": "manager@company.com",
        "subject": "Daily Order Report",
        "emailType": "html",
        "htmlBody": "Report attached",
        "attachments": "data"
      }
    }
  ]
}
```

## 节点参数配置指南 Node Parameter Configuration Guide

### 1. Schedule Trigger配置
```json
{
  "rule": {
    "interval": [
      {
        "field": "hours",
        "hoursInterval": 1
      }
    ]
  },
  // 或使用Cron表达式
  "rule": {
    "cronExpression": "0 9 * * 1-5"  // 工作日9点
  }
}
```

### 2. Database节点配置
```json
{
  "operation": "executeQuery",
  "query": "={{$parameter[\"sqlQuery\"]}}",
  "options": {
    "queryBatching": true,
    "queryReplacement": "={{$json}}"
  }
}
```

### 3. HTTP Request配置
```json
{
  "method": "POST",
  "url": "https://api.example.com/endpoint",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "data",
        "value": "={{$json}}"
      }
    ]
  },
  "options": {
    "timeout": 10000,
    "retry": 3,
    "batching": false
  }
}
```

### 4. Code节点配置
```javascript
// 标准Code节点模板
const items = $input.all();

// 数据处理逻辑
const processedItems = items.map(item => {
  // 访问输入数据
  const inputData = item.json;

  // 处理逻辑
  const result = {
    ...inputData,
    processed: true,
    timestamp: new Date().toISOString()
  };

  // 返回处理结果
  return {
    json: result,
    binary: item.binary || {}
  };
});

return processedItems;
```

## 节点连接规则 Node Connection Rules

### Rule 1: 数据类型匹配
```javascript
const connectionRules = {
  // 主输出连接
  "main": {
    from: ["*"],  // 任何节点
    to: ["*"]     // 任何节点
  },

  // 二进制数据连接
  "binary": {
    from: ["readBinaryFile", "httpRequest", "s3"],
    to: ["writeBinaryFile", "s3", "email"]
  },

  // 错误输出连接
  "error": {
    from: ["*"],
    to: ["errorWorkflow", "stopAndError", "email"]
  }
};
```

### Rule 2: 节点顺序约束
```javascript
const sequenceConstraints = [
  // 触发器必须在最前
  { rule: "trigger_first", nodes: ["webhook", "schedule", "form"] },

  // 响应节点必须在最后
  { rule: "response_last", nodes: ["respondToWebhook"] },

  // 批处理节点成对出现
  { rule: "batch_pair", nodes: ["splitInBatches", "loop"] }
];
```

## 节点优化建议 Node Optimization Suggestions

### 1. 性能优化
```javascript
const performanceOptimizations = {
  // 使用批处理
  largeDataset: {
    use: "splitInBatches",
    config: { batchSize: 100 }
  },

  // 并行处理
  multipleAPIs: {
    use: "parallel branches",
    avoid: "sequential calls"
  },

  // 缓存策略
  frequentData: {
    use: "staticData node",
    cache: "results"
  }
};
```

### 2. 错误处理
```javascript
const errorHandling = {
  // 添加错误捕获
  criticalNodes: {
    wrap_with: "try-catch in code node",
    fallback: "error workflow"
  },

  // 重试机制
  unreliableAPIs: {
    add: "retry logic",
    config: { attempts: 3, delay: 1000 }
  },

  // 超时设置
  longRunning: {
    set: "timeout",
    max: 30000
  }
};
```

## 常用节点组合 Common Node Combinations

### Combo 1: API数据同步
```
HTTP Request → Code (Transform) → Database (Insert)
```

### Combo 2: 文件处理流水线
```
Read File → Code (Process) → Write File → Email (Notify)
```

### Combo 3: 条件分支处理
```
Webhook → IF (Condition) → [Branch A | Branch B] → Merge → Response
```

### Combo 4: 批量处理模式
```
Database (Query) → Split In Batches → Process → Loop → Aggregate
```

## 输出格式 Output Format

### 最终输出: node_config.json
```json
{
  "workflow_id": "REQ_20250128_001",
  "node_analysis": {
    "total_nodes": 5,
    "complexity": "medium",
    "estimated_execution_time": "30s"
  },
  "nodes": [
    {
      "id": "node_1",
      "type": "n8n-nodes-base.scheduleTrigger",
      "name": "Daily Trigger",
      "position": [250, 300],
      "parameters": {
        "rule": {
          "cronExpression": "0 9 * * *"
        }
      },
      "credentials": {},
      "disabled": false,
      "notes": "Triggers every day at 9 AM"
    }
  ],
  "connections": {
    "node_1": {
      "main": [
        [{"node": "node_2", "type": "main", "index": 0}]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1",
    "saveManualExecutions": true,
    "callerPolicy": "workflowsFromSameOwner",
    "errorWorkflow": ""
  },
  "validation": {
    "all_nodes_connected": true,
    "required_credentials_set": false,
    "has_trigger": true,
    "has_output": true
  }
}
```

## 与其他模块的接口 Interface with Other Modules

### 输入自: ANALYSIS_REQUIREMENTS.md
```json
{
  "required_nodes": ["schedule", "postgres", "email"],
  "trigger_type": "schedule",
  "processing_steps": 3
}
```

### 输出到: ANALYSIS_DATAFLOW.md
```json
{
  "node_sequence": ["trigger", "fetch", "transform", "output"],
  "data_types": ["trigger_data", "sql_results", "formatted_data", "email"]
}
```

### 输出到: node_builder.py
```json
{
  "nodes_to_create": 5,
  "connections_to_establish": 4,
  "credentials_required": ["postgres", "smtp"]
}
```

---

**模块状态**: Active
**下一步**: 执行 ANALYSIS_DATAFLOW.md