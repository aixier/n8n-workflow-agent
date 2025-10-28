# 测试分析模块 Testing Analysis Module

Version: 1.0.0
Module Type: AI Analysis
Parent: CLAUDE.md
Previous: ANALYSIS_DATAFLOW.md

## 模块职责 Module Responsibilities

本模块负责生成测试策略，设计测试用例，准备测试数据，定义验证规则，确保工作流质量。

## 测试策略框架 Testing Strategy Framework

### 1. 测试层级 (Testing Levels)
```
Level 1: 单元测试 (Unit Testing)
  └── 测试单个节点功能

Level 2: 集成测试 (Integration Testing)
  └── 测试节点间数据传递

Level 3: 端到端测试 (E2E Testing)
  └── 测试完整工作流

Level 4: 性能测试 (Performance Testing)
  └── 测试负载和响应时间

Level 5: 安全测试 (Security Testing)
  └── 测试安全漏洞和权限
```

### 2. 测试类型矩阵 (Test Type Matrix)
```javascript
const testMatrix = {
  functional: {
    coverage: ["happy_path", "edge_cases", "error_cases"],
    priority: "high",
    automated: true
  },

  performance: {
    metrics: ["response_time", "throughput", "resource_usage"],
    priority: "medium",
    automated: true
  },

  security: {
    checks: ["authentication", "authorization", "injection", "encryption"],
    priority: "high",
    automated: false
  },

  reliability: {
    scenarios: ["network_failure", "timeout", "rate_limit", "retry"],
    priority: "medium",
    automated: true
  }
};
```

## 测试用例生成 Test Case Generation

### 1. 正常流程测试 (Happy Path Testing)
```json
{
  "test_case": {
    "id": "TC_001",
    "name": "正常YouTube视频处理",
    "category": "functional",
    "priority": "high",
    "preconditions": [
      "n8n工作流已激活",
      "YouTube API可访问",
      "Qwen API配置正确"
    ],
    "input": {
      "method": "POST",
      "endpoint": "/webhook/youtube2post",
      "headers": {
        "Content-Type": "application/json"
      },
      "body": {
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "language": "en",
        "templateId": "default",
        "options": {
          "quality": "high",
          "subtitles": true,
          "screenshots": 5
        }
      }
    },
    "steps": [
      "发送POST请求到webhook",
      "验证返回状态码200",
      "检查响应包含taskId",
      "等待处理完成",
      "验证输出文件存在"
    ],
    "expected": {
      "status": 200,
      "response": {
        "success": true,
        "message": "Task completed",
        "data": {
          "taskId": "string",
          "status": "completed",
          "result": {
            "quotes": "array[5]",
            "screenshots": "array[5]",
            "summary": "string"
          }
        }
      },
      "files": [
        "template_data.json",
        "summary.md",
        "screenshots/*.jpg"
      ]
    },
    "validation": [
      "assert response.success === true",
      "assert response.data.result.quotes.length >= 5",
      "assert files.screenshots.length === 5"
    ]
  }
}
```

### 2. 边界条件测试 (Edge Case Testing)
```json
{
  "edge_cases": [
    {
      "id": "TC_EDGE_001",
      "name": "超长视频处理",
      "input": {
        "url": "https://youtube.com/watch?v=LONG_VIDEO",
        "duration": "3:00:00"
      },
      "expected": {
        "behavior": "分批处理",
        "timeout": 600000,
        "memory_limit": "2GB"
      }
    },
    {
      "id": "TC_EDGE_002",
      "name": "无字幕视频",
      "input": {
        "url": "https://youtube.com/watch?v=NO_SUBTITLES",
        "subtitles": false
      },
      "expected": {
        "behavior": "使用音频转文字",
        "fallback": "speech_to_text"
      }
    },
    {
      "id": "TC_EDGE_003",
      "name": "并发请求",
      "input": {
        "concurrent_requests": 10,
        "same_video": true
      },
      "expected": {
        "behavior": "队列处理",
        "rate_limit": "5/minute"
      }
    },
    {
      "id": "TC_EDGE_004",
      "name": "最小输入",
      "input": {
        "url": "https://youtube.com/watch?v=xxx"
      },
      "expected": {
        "behavior": "使用默认配置",
        "defaults_applied": true
      }
    }
  ]
}
```

### 3. 错误处理测试 (Error Case Testing)
```json
{
  "error_cases": [
    {
      "id": "TC_ERR_001",
      "name": "无效URL",
      "input": {
        "url": "not_a_valid_url"
      },
      "expected": {
        "status": 400,
        "error": "Invalid URL format"
      }
    },
    {
      "id": "TC_ERR_002",
      "name": "视频不存在",
      "input": {
        "url": "https://youtube.com/watch?v=NONEXISTENT"
      },
      "expected": {
        "status": 404,
        "error": "Video not found"
      }
    },
    {
      "id": "TC_ERR_003",
      "name": "API限额超出",
      "scenario": "Qwen API rate limit",
      "expected": {
        "status": 429,
        "error": "Rate limit exceeded",
        "retry_after": 60
      }
    },
    {
      "id": "TC_ERR_004",
      "name": "认证失败",
      "headers": {
        "Authorization": "Invalid"
      },
      "expected": {
        "status": 401,
        "error": "Unauthorized"
      }
    }
  ]
}
```

## 测试数据生成 Test Data Generation

### 1. 模拟数据模板 (Mock Data Templates)
```javascript
const mockDataTemplates = {
  // YouTube视频元数据
  youtube_video: {
    videoId: "{{random.alphaNumeric(11)}}",
    title: "{{lorem.sentence()}}",
    description: "{{lorem.paragraph()}}",
    duration: "{{random.number({min:60, max:3600})}}",
    uploadDate: "{{date.past()}}",
    channelName: "{{name.fullName()}}",
    viewCount: "{{random.number({min:1000, max:1000000})}}",
    subtitles: {
      available: true,
      languages: ["en", "zh", "es"]
    }
  },

  // 数据库记录
  database_record: {
    id: "{{random.uuid()}}",
    created_at: "{{date.recent()}}",
    updated_at: "{{date.recent()}}",
    status: "{{random.arrayElement(['pending','processing','completed'])}}",
    data: {
      field1: "{{lorem.word()}}",
      field2: "{{random.number()}}",
      field3: "{{random.boolean()}}"
    }
  },

  // API响应
  api_response: {
    success: "{{random.boolean()}}",
    message: "{{lorem.sentence()}}",
    data: "{{json.object()}}",
    timestamp: "{{date.now()}}"
  }
};
```

### 2. 测试数据集 (Test Data Sets)
```json
{
  "test_datasets": {
    "small": {
      "size": 10,
      "description": "基础功能测试",
      "use_case": "快速验证"
    },
    "medium": {
      "size": 100,
      "description": "标准测试集",
      "use_case": "日常测试"
    },
    "large": {
      "size": 1000,
      "description": "压力测试",
      "use_case": "性能测试"
    },
    "edge": {
      "size": 50,
      "description": "边界值测试",
      "includes": [
        "empty_values",
        "null_values",
        "max_length_strings",
        "special_characters",
        "unicode_characters"
      ]
    }
  }
}
```

### 3. 数据生成器配置 (Data Generator Config)
```javascript
const dataGenerator = {
  // 生成YouTube URLs
  generateYouTubeUrls: (count) => {
    const videoIds = [
      "dQw4w9WgXcQ", // 正常视频
      "INVALID_ID",  // 无效ID
      "PRIVATE_VID", // 私有视频
      "DELETED_VID", // 已删除
      "LONG_VIDEO",  // 长视频
    ];

    return Array(count).fill(null).map((_, i) => ({
      url: `https://youtube.com/watch?v=${videoIds[i % videoIds.length]}`,
      type: ["valid", "invalid", "private", "deleted", "long"][i % 5]
    }));
  },

  // 生成表单数据
  generateFormData: (fields) => {
    return fields.map(field => ({
      name: field.name,
      value: faker[field.type][field.method](),
      validation: field.validation
    }));
  },

  // 生成批量数据
  generateBatch: (template, count) => {
    return Array(count).fill(null).map(() =>
      JSON.parse(faker.fake(JSON.stringify(template)))
    );
  }
};
```

## 性能测试策略 Performance Testing Strategy

### 1. 性能指标 (Performance Metrics)
```javascript
const performanceMetrics = {
  response_time: {
    target: "< 2000ms",
    p95: "< 5000ms",
    p99: "< 10000ms"
  },

  throughput: {
    target: "> 100 req/min",
    sustained: "> 50 req/min",
    peak: "> 200 req/min"
  },

  resource_usage: {
    cpu: "< 80%",
    memory: "< 1GB",
    disk_io: "< 100MB/s"
  },

  error_rate: {
    target: "< 1%",
    acceptable: "< 5%",
    critical: "> 10%"
  }
};
```

### 2. 负载测试场景 (Load Test Scenarios)
```json
{
  "load_scenarios": [
    {
      "name": "渐进负载",
      "pattern": "ramp-up",
      "stages": [
        { "duration": "1m", "target": 10 },
        { "duration": "2m", "target": 50 },
        { "duration": "3m", "target": 100 },
        { "duration": "2m", "target": 50 },
        { "duration": "1m", "target": 0 }
      ]
    },
    {
      "name": "峰值负载",
      "pattern": "spike",
      "stages": [
        { "duration": "30s", "target": 10 },
        { "duration": "10s", "target": 200 },
        { "duration": "30s", "target": 10 }
      ]
    },
    {
      "name": "持续负载",
      "pattern": "steady",
      "stages": [
        { "duration": "10m", "target": 50 }
      ]
    }
  ]
}
```

## 自动化测试脚本 Automated Test Scripts

### 1. 测试执行器模板 (Test Runner Template)
```python
# test_runner_template.py

import json
import time
import requests
from typing import Dict, List, Any

class WorkflowTestRunner:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.results = []

    def run_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个测试用例"""
        start_time = time.time()

        try:
            # 发送请求
            response = requests.request(
                method=test_case["input"]["method"],
                url=f"{self.base_url}{test_case['input']['endpoint']}",
                headers={**self.headers, **test_case["input"].get("headers", {})},
                json=test_case["input"].get("body"),
                timeout=30
            )

            # 记录响应
            result = {
                "test_id": test_case["id"],
                "name": test_case["name"],
                "status_code": response.status_code,
                "response_time": time.time() - start_time,
                "response_body": response.json() if response.content else None
            }

            # 验证响应
            result["validations"] = self.validate_response(
                response,
                test_case["expected"]
            )

            result["passed"] = all(v["passed"] for v in result["validations"])

        except Exception as e:
            result = {
                "test_id": test_case["id"],
                "name": test_case["name"],
                "error": str(e),
                "passed": False
            }

        self.results.append(result)
        return result

    def validate_response(self, response, expected):
        """验证响应是否符合预期"""
        validations = []

        # 验证状态码
        validations.append({
            "check": "status_code",
            "expected": expected.get("status"),
            "actual": response.status_code,
            "passed": response.status_code == expected.get("status", 200)
        })

        # 验证响应体
        if "response" in expected and response.content:
            response_data = response.json()
            for key, value in expected["response"].items():
                actual_value = response_data.get(key)
                validations.append({
                    "check": f"response.{key}",
                    "expected": value,
                    "actual": actual_value,
                    "passed": actual_value == value
                })

        return validations

    def run_test_suite(self, test_cases: List[Dict]) -> Dict[str, Any]:
        """执行测试套件"""
        suite_start = time.time()

        for test_case in test_cases:
            self.run_test(test_case)

        return {
            "total_tests": len(test_cases),
            "passed": sum(1 for r in self.results if r["passed"]),
            "failed": sum(1 for r in self.results if not r["passed"]),
            "total_time": time.time() - suite_start,
            "results": self.results
        }

    def generate_report(self) -> str:
        """生成测试报告"""
        passed = sum(1 for r in self.results if r["passed"])
        failed = len(self.results) - passed

        report = f"""
# Test Report
## Summary
- Total Tests: {len(self.results)}
- Passed: {passed}
- Failed: {failed}
- Pass Rate: {passed/len(self.results)*100:.2f}%

## Details
"""
        for result in self.results:
            status = "✅" if result["passed"] else "❌"
            report += f"\n### {status} {result['name']}\n"
            report += f"- Test ID: {result['test_id']}\n"
            report += f"- Response Time: {result.get('response_time', 'N/A'):.2f}s\n"

            if "error" in result:
                report += f"- Error: {result['error']}\n"

        return report
```

### 2. 测试数据准备脚本 (Test Data Preparation)
```python
# prepare_test_data.py

def prepare_youtube_test_data():
    """准备YouTube测试数据"""
    return {
        "valid_videos": [
            {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "title": "Rick Astley - Never Gonna Give You Up",
                "duration": 213,
                "has_subtitles": True
            }
        ],
        "invalid_urls": [
            "not_a_url",
            "http://not-youtube.com/video",
            "https://youtube.com/watch?v="
        ],
        "edge_cases": [
            {
                "url": "https://youtube.com/watch?v=VERY_LONG_VIDEO",
                "description": "3+ hour video"
            },
            {
                "url": "https://youtube.com/watch?v=NO_SUBS",
                "description": "Video without subtitles"
            }
        ]
    }

def prepare_database_test_data():
    """准备数据库测试数据"""
    return {
        "insert_data": [
            {"id": 1, "name": "Test 1", "value": 100},
            {"id": 2, "name": "Test 2", "value": 200}
        ],
        "update_data": [
            {"id": 1, "value": 150}
        ],
        "query_tests": [
            "SELECT * FROM test_table",
            "SELECT * FROM test_table WHERE value > 100",
            "SELECT COUNT(*) FROM test_table"
        ]
    }
```

## 测试验证规则 Test Validation Rules

### 1. 响应验证 (Response Validation)
```javascript
const validationRules = {
  // 结构验证
  structure: {
    check: "response_schema",
    schema: {
      type: "object",
      required: ["success", "data"],
      properties: {
        success: { type: "boolean" },
        data: { type: "object" }
      }
    }
  },

  // 业务逻辑验证
  business: {
    rules: [
      "if success=true, data must exist",
      "if error exists, success=false",
      "taskId must be unique"
    ]
  },

  // 数据完整性
  integrity: {
    checks: [
      "no null in required fields",
      "dates in ISO format",
      "URLs are valid"
    ]
  }
};
```

### 2. 文件验证 (File Validation)
```javascript
const fileValidation = {
  // 检查文件存在
  existence: {
    files: [
      "output/template_data.json",
      "output/summary.md",
      "output/screenshots/*.jpg"
    ]
  },

  // 检查文件格式
  format: {
    "*.json": "valid JSON",
    "*.md": "valid Markdown",
    "*.jpg": "valid JPEG"
  },

  // 检查文件大小
  size: {
    "screenshots/*.jpg": "< 500KB",
    "summary.md": "> 0 bytes"
  }
};
```

## 测试环境配置 Test Environment Configuration

### 1. 环境隔离 (Environment Isolation)
```json
{
  "environments": {
    "development": {
      "url": "http://localhost:5678",
      "database": "test_db",
      "api_keys": "test_keys",
      "data_cleanup": true
    },
    "staging": {
      "url": "https://staging.example.com",
      "database": "staging_db",
      "api_keys": "staging_keys",
      "data_cleanup": false
    },
    "production": {
      "url": "https://api.example.com",
      "database": "prod_db",
      "api_keys": "prod_keys",
      "data_cleanup": false,
      "restricted": true
    }
  }
}
```

### 2. 测试配置 (Test Configuration)
```yaml
# test_config.yaml
test_settings:
  parallel_execution: true
  max_parallel: 5
  timeout_default: 30000
  retry_failed: true
  retry_count: 3

logging:
  level: INFO
  output: test_results.log
  format: json

reporting:
  generate_html: true
  generate_json: true
  send_email: false

cleanup:
  remove_temp_files: true
  reset_database: true
  clear_cache: true
```

## 测试报告模板 Test Report Template

### 最终输出: test_report.json
```json
{
  "test_execution": {
    "id": "TEST_RUN_20250128_001",
    "workflow": "youtube2post",
    "environment": "development",
    "start_time": "2025-01-28T10:00:00Z",
    "end_time": "2025-01-28T10:05:00Z",
    "duration": "5 minutes"
  },
  "summary": {
    "total_tests": 25,
    "passed": 23,
    "failed": 2,
    "skipped": 0,
    "pass_rate": "92%"
  },
  "categories": {
    "functional": {
      "total": 15,
      "passed": 14,
      "failed": 1
    },
    "performance": {
      "total": 5,
      "passed": 5,
      "failed": 0
    },
    "security": {
      "total": 5,
      "passed": 4,
      "failed": 1
    }
  },
  "failed_tests": [
    {
      "id": "TC_ERR_003",
      "name": "API限额超出",
      "reason": "Rate limit not properly handled",
      "severity": "medium"
    },
    {
      "id": "TC_SEC_002",
      "name": "SQL注入测试",
      "reason": "Input sanitization missing",
      "severity": "high"
    }
  ],
  "performance_metrics": {
    "average_response_time": "1.2s",
    "p95_response_time": "3.5s",
    "throughput": "120 req/min",
    "error_rate": "0.8%"
  },
  "recommendations": [
    "Add rate limiting handling",
    "Implement input sanitization",
    "Optimize database queries",
    "Add more edge case tests"
  ],
  "artifacts": {
    "logs": "logs/test_run_20250128_001.log",
    "screenshots": "screenshots/",
    "reports": "reports/test_report.html"
  }
}
```

## 与其他模块的接口 Interface with Other Modules

### 输入自: ANALYSIS_DATAFLOW.md
```json
{
  "data_flow_paths": ["happy_path", "error_path"],
  "test_data_requirements": {
    "formats": ["json", "csv", "xml"],
    "volumes": ["small", "medium", "large"]
  }
}
```

### 输出到: test_runner.py
```json
{
  "test_suite": "youtube2post_test_suite.json",
  "test_data": "test_data/",
  "execution_plan": {
    "order": "sequential",
    "parallel": false,
    "environments": ["dev"]
  }
}
```

### 输出到: CLAUDE.md
```json
{
  "testing_complete": true,
  "quality_gate": "passed",
  "ready_for_deployment": true
}
```

---

**模块状态**: Active
**下一步**: 执行工具脚本创建