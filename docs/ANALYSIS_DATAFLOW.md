# 数据流分析模块 Data Flow Analysis Module

Version: 1.0.0
Module Type: AI Analysis
Parent: CLAUDE.md
Previous: ANALYSIS_NODES.md

## 模块职责 Module Responsibilities

本模块负责设计工作流中的数据流向，定义数据转换规则，处理数据格式映射，确保数据在节点间正确传递。

## 数据流模型 Data Flow Models

### Model 1: 线性数据流 (Linear Flow)
```
Input → Process A → Process B → Process C → Output
  ↓         ↓           ↓           ↓          ↓
[raw]   [cleaned]  [transformed] [validated] [final]
```

### Model 2: 分支数据流 (Branched Flow)
```
           ┌→ Process A → Output A
Input → Split
           └→ Process B → Output B
```

### Model 3: 合并数据流 (Merged Flow)
```
Input A →┐
         ├→ Merge → Process → Output
Input B →┘
```

### Model 4: 循环数据流 (Loop Flow)
```
Input → Split → Process → Check → [Loop Back | Continue] → Output
          ↑                  ↓
          └──────────────────┘
```

## 数据类型系统 Data Type System

### 1. n8n核心数据类型
```typescript
interface INodeExecutionData {
  json: {                    // JSON数据
    [key: string]: any
  },
  binary?: {                 // 二进制数据
    [key: string]: {
      data: string,         // Base64编码
      mimeType: string,
      fileName?: string,
      fileExtension?: string
    }
  },
  error?: {                  // 错误信息
    message: string,
    stack?: string
  }
}
```

### 2. 常见数据格式转换
```javascript
const dataTransformations = {
  // CSV → JSON
  "csv_to_json": {
    input: "text/csv",
    output: "application/json",
    node: "spreadsheetFile",
    config: { headerRow: true }
  },

  // JSON → Excel
  "json_to_excel": {
    input: "application/json",
    output: "application/vnd.ms-excel",
    node: "spreadsheetFile",
    config: { operation: "write" }
  },

  // SQL Results → Array
  "sql_to_array": {
    input: "sql_result_set",
    output: "json_array",
    node: "code",
    transform: "items.map(item => item.json)"
  },

  // HTML → Text
  "html_to_text": {
    input: "text/html",
    output: "text/plain",
    node: "html",
    config: { operation: "extractText" }
  },

  // XML → JSON
  "xml_to_json": {
    input: "text/xml",
    output: "application/json",
    node: "xml",
    config: { mode: "xmlToJson" }
  }
};
```

## 数据映射规则 Data Mapping Rules

### Rule 1: 字段映射 (Field Mapping)
```javascript
const fieldMapping = {
  // 直接映射
  direct: {
    source: "user.email",
    target: "contact.email_address"
  },

  // 表达式映射
  expression: {
    source: "{{$json.firstName}} {{$json.lastName}}",
    target: "fullName"
  },

  // 条件映射
  conditional: {
    source: "$json.status",
    target: "isActive",
    transform: "status === 'active' ? true : false"
  },

  // 数组映射
  array: {
    source: "items",
    target: "products",
    transform: "items.map(i => ({ id: i.sku, name: i.title }))"
  }
};
```

### Rule 2: 数据验证 (Data Validation)
```javascript
const dataValidation = {
  // 类型验证
  typeCheck: {
    field: "age",
    type: "number",
    required: true
  },

  // 格式验证
  formatCheck: {
    field: "email",
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: "Invalid email format"
  },

  // 范围验证
  rangeCheck: {
    field: "quantity",
    min: 1,
    max: 100
  },

  // 枚举验证
  enumCheck: {
    field: "status",
    values: ["pending", "processing", "completed", "failed"]
  }
};
```

## 数据流分析步骤 Data Flow Analysis Steps

### Step 1: 输入数据分析
```json
{
  "input_analysis": {
    "source": "webhook",
    "format": "json",
    "schema": {
      "url": "string",
      "options": {
        "language": "string",
        "quality": "string"
      }
    },
    "validation": {
      "url": "required|url",
      "options.language": "required|in:en,zh",
      "options.quality": "optional|in:high,medium,low"
    },
    "sample_data": {
      "url": "https://youtube.com/watch?v=xxx",
      "options": {
        "language": "zh",
        "quality": "high"
      }
    }
  }
}
```

### Step 2: 中间数据转换
```json
{
  "transformations": [
    {
      "step": 1,
      "from": "webhook_input",
      "to": "video_metadata",
      "operation": "extract",
      "transform": {
        "video_id": "extractVideoId($json.url)",
        "language": "$json.options.language",
        "timestamp": "new Date().toISOString()"
      }
    },
    {
      "step": 2,
      "from": "video_metadata",
      "to": "download_config",
      "operation": "prepare",
      "transform": {
        "url": "$json.url",
        "format": "mp4",
        "quality": "$json.options.quality || 'medium'",
        "subtitles": true
      }
    },
    {
      "step": 3,
      "from": "download_result",
      "to": "ai_input",
      "operation": "format",
      "transform": {
        "text": "$json.subtitles",
        "metadata": {
          "duration": "$json.duration",
          "title": "$json.title"
        }
      }
    }
  ]
}
```

### Step 3: 输出数据格式化
```json
{
  "output_formatting": {
    "target": "webhook_response",
    "format": "json",
    "schema": {
      "success": "boolean",
      "message": "string",
      "data": {
        "taskId": "string",
        "status": "string",
        "result": {
          "quotes": "array",
          "summary": "string",
          "files": "object"
        }
      }
    },
    "transformation": {
      "success": "!$json.error",
      "message": "$json.error ? $json.error.message : 'Task completed'",
      "data": {
        "taskId": "$json.taskId",
        "status": "$json.status",
        "result": "$json.result"
      }
    }
  }
}
```

## 数据流模板 Data Flow Templates

### Template 1: ETL数据流
```json
{
  "name": "ETL_DataFlow",
  "stages": [
    {
      "stage": "Extract",
      "node": "database",
      "output": {
        "type": "array",
        "schema": "sql_result_set"
      }
    },
    {
      "stage": "Transform",
      "node": "code",
      "input": "sql_result_set",
      "operations": [
        "filter",
        "map",
        "aggregate"
      ],
      "output": {
        "type": "array",
        "schema": "transformed_data"
      }
    },
    {
      "stage": "Load",
      "node": "database",
      "input": "transformed_data",
      "operation": "bulk_insert"
    }
  ]
}
```

### Template 2: API集成数据流
```json
{
  "name": "API_Integration_Flow",
  "stages": [
    {
      "stage": "Receive",
      "node": "webhook",
      "validation": true,
      "output": "raw_request"
    },
    {
      "stage": "Authenticate",
      "node": "code",
      "operation": "verify_token",
      "output": "authenticated_request"
    },
    {
      "stage": "Process",
      "node": "httpRequest",
      "mapping": {
        "headers": {
          "Authorization": "Bearer {{$json.token}}"
        },
        "body": "{{$json.data}}"
      },
      "output": "api_response"
    },
    {
      "stage": "Response",
      "node": "respondToWebhook",
      "format": "json",
      "status": 200
    }
  ]
}
```

### Template 3: 文件处理数据流
```json
{
  "name": "File_Processing_Flow",
  "stages": [
    {
      "stage": "Upload",
      "node": "webhook",
      "accepts": "multipart/form-data",
      "output": "binary_file"
    },
    {
      "stage": "Parse",
      "node": "spreadsheetFile",
      "operation": "read",
      "output": "json_data"
    },
    {
      "stage": "Validate",
      "node": "code",
      "operations": ["check_format", "validate_data"],
      "output": "validated_data"
    },
    {
      "stage": "Process",
      "node": "code",
      "operations": ["transform", "enrich"],
      "output": "processed_data"
    },
    {
      "stage": "Export",
      "node": "spreadsheetFile",
      "operation": "write",
      "format": "xlsx",
      "output": "output_file"
    }
  ]
}
```

## 数据流优化策略 Data Flow Optimization

### 1. 减少数据传输
```javascript
const optimizations = {
  // 只传递必要字段
  selectFields: {
    before: "SELECT * FROM users",
    after: "SELECT id, name, email FROM users"
  },

  // 本地过滤而非远程
  filterLocal: {
    before: "API call for all → filter",
    after: "API call with query params"
  },

  // 数据分页
  pagination: {
    use: "LIMIT and OFFSET",
    batchSize: 100
  }
};
```

### 2. 并行处理
```javascript
const parallelProcessing = {
  // 并行API调用
  multipleAPIs: {
    pattern: "split → parallel branches → merge",
    benefit: "减少总执行时间"
  },

  // 并行数据处理
  dataProcessing: {
    pattern: "split in batches → parallel process → aggregate",
    benefit: "提高处理速度"
  }
};
```

### 3. 缓存策略
```javascript
const cachingStrategy = {
  // 静态数据缓存
  staticData: {
    node: "staticData",
    ttl: 3600,
    use: "配置数据、查找表"
  },

  // 结果缓存
  resultCache: {
    storage: "redis",
    key: "hash(input)",
    ttl: 300
  }
};
```

## 错误处理数据流 Error Handling Flow

### 错误捕获和处理
```json
{
  "error_handling": {
    "strategy": "try-catch-finally",
    "flow": [
      {
        "try": {
          "nodes": ["main_process"],
          "on_success": "continue"
        }
      },
      {
        "catch": {
          "nodes": ["error_handler"],
          "operations": [
            "log_error",
            "send_notification",
            "save_to_error_queue"
          ]
        }
      },
      {
        "finally": {
          "nodes": ["cleanup"],
          "operations": ["close_connections", "clear_temp_files"]
        }
      }
    ]
  }
}
```

## 数据流监控 Data Flow Monitoring

### 监控指标
```json
{
  "metrics": {
    "throughput": {
      "measure": "records/second",
      "threshold": 1000
    },
    "latency": {
      "measure": "ms",
      "threshold": 500
    },
    "error_rate": {
      "measure": "percentage",
      "threshold": 1
    },
    "data_quality": {
      "measure": "validation_pass_rate",
      "threshold": 95
    }
  }
}
```

## 数据安全 Data Security

### 敏感数据处理
```javascript
const securityMeasures = {
  // 数据脱敏
  masking: {
    fields: ["password", "credit_card", "ssn"],
    method: "hash|encrypt|mask"
  },

  // 传输加密
  encryption: {
    protocol: "HTTPS",
    headers: "encrypted",
    body: "encrypted"
  },

  // 访问控制
  accessControl: {
    authentication: "required",
    authorization: "role-based",
    audit: "all_access_logged"
  }
};
```

## 数据流测试 Data Flow Testing

### 测试场景
```json
{
  "test_scenarios": [
    {
      "name": "正常流程",
      "input": {
        "valid": true,
        "complete": true
      },
      "expected_flow": ["input", "process", "output"],
      "expected_output": {
        "success": true
      }
    },
    {
      "name": "错误处理",
      "input": {
        "valid": false
      },
      "expected_flow": ["input", "validation", "error_handler"],
      "expected_output": {
        "success": false,
        "error": "Validation failed"
      }
    },
    {
      "name": "边界条件",
      "input": {
        "size": "maximum"
      },
      "expected_flow": ["input", "batch_process", "output"],
      "expected_output": {
        "success": true,
        "batches_processed": 10
      }
    }
  ]
}
```

## 输出格式 Output Format

### 最终输出: dataflow_config.json
```json
{
  "workflow_id": "REQ_20250128_001",
  "dataflow_analysis": {
    "model": "linear",
    "stages": 5,
    "transformations": 3,
    "estimated_data_size": "10MB",
    "bottlenecks": ["database_query", "api_call"]
  },
  "flow_definition": {
    "input": {
      "source": "webhook",
      "format": "json",
      "schema": {},
      "validation": {}
    },
    "stages": [
      {
        "id": "stage_1",
        "name": "Data Extraction",
        "input_format": "json",
        "output_format": "array",
        "transformation": {},
        "error_handling": {}
      }
    ],
    "output": {
      "target": "email",
      "format": "attachment",
      "schema": {}
    }
  },
  "optimizations": [
    {
      "type": "batch_processing",
      "location": "stage_2",
      "benefit": "50% faster"
    }
  ],
  "data_mappings": [
    {
      "source": "input.user.email",
      "target": "output.recipient",
      "transform": "toLowerCase()"
    }
  ],
  "validation_rules": [
    {
      "field": "email",
      "rules": ["required", "email"]
    }
  ]
}
```

## 与其他模块的接口 Interface with Other Modules

### 输入自: ANALYSIS_NODES.md
```json
{
  "node_sequence": ["webhook", "database", "transform", "email"],
  "node_outputs": {
    "webhook": "json",
    "database": "array",
    "transform": "processed_array",
    "email": "success_status"
  }
}
```

### 输出到: ANALYSIS_TESTING.md
```json
{
  "test_data_requirements": {
    "input_samples": 3,
    "edge_cases": 2,
    "error_cases": 2
  },
  "data_flow_paths": ["happy_path", "error_path", "edge_case_path"]
}
```

### 输出到: workflow_analyzer.py
```json
{
  "flow_validation": {
    "all_paths_connected": true,
    "data_types_compatible": true,
    "transformations_valid": true
  }
}
```

---

**模块状态**: Active
**下一步**: 执行 ANALYSIS_TESTING.md