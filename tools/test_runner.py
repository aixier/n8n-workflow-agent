#!/usr/bin/env python3
"""
n8n Workflow Test Runner
工作流自动化测试执行工具

Author: AI Terminal Team
Version: 1.0.0
"""

import json
import time
import requests
import argparse
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import logging
import asyncio
import aiohttp

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowTestRunner:
    """工作流测试运行器"""

    def __init__(self, base_url: str = None, api_key: str = None):
        """
        初始化测试运行器

        Args:
            base_url: n8n实例URL
            api_key: API密钥
        """
        self.base_url = base_url or os.getenv('N8N_BASE_URL', 'http://localhost:5678')
        self.api_key = api_key or os.getenv('N8N_API_KEY', '')
        self.headers = {
            'Content-Type': 'application/json'
        }

        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

        self.results = []
        self.start_time = None
        self.end_time = None

    def load_test_suite(self, suite_file: str) -> Dict[str, Any]:
        """
        加载测试套件

        Args:
            suite_file: 测试套件文件路径

        Returns:
            测试套件配置
        """
        try:
            with open(suite_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load test suite: {e}")
            return {}

    def run_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个测试用例

        Args:
            test_case: 测试用例配置

        Returns:
            测试结果
        """
        logger.info(f"Running test: {test_case.get('name', 'Unknown')}")
        start_time = time.time()

        result = {
            "test_id": test_case.get("id"),
            "name": test_case.get("name"),
            "category": test_case.get("category", "functional"),
            "start_time": datetime.now().isoformat(),
            "validations": []
        }

        try:
            # 准备请求
            method = test_case["input"].get("method", "POST")
            endpoint = test_case["input"].get("endpoint", "")
            url = f"{self.base_url}{endpoint}"
            headers = {**self.headers, **test_case["input"].get("headers", {})}

            # 发送请求
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=test_case["input"].get("body"),
                timeout=test_case.get("timeout", 30)
            )

            # 记录响应
            result["status_code"] = response.status_code
            result["response_time"] = time.time() - start_time

            if response.content:
                try:
                    result["response_body"] = response.json()
                except:
                    result["response_body"] = response.text

            # 执行验证
            if "expected" in test_case:
                result["validations"] = self.validate_response(
                    response,
                    test_case["expected"],
                    result.get("response_body")
                )

            # 判断测试是否通过
            result["passed"] = all(v.get("passed", False) for v in result["validations"])

            # 等待异步处理（如果需要）
            if test_case.get("wait_for_completion"):
                result["async_result"] = self.wait_for_completion(
                    result.get("response_body", {}).get("data", {}).get("taskId")
                )

        except requests.exceptions.Timeout:
            result["error"] = "Request timeout"
            result["passed"] = False
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection error"
            result["passed"] = False
        except Exception as e:
            result["error"] = str(e)
            result["passed"] = False

        result["end_time"] = datetime.now().isoformat()
        result["duration"] = time.time() - start_time

        self.results.append(result)

        # 输出测试结果
        status_emoji = "✅" if result["passed"] else "❌"
        logger.info(f"{status_emoji} Test {result['name']}: {'PASSED' if result['passed'] else 'FAILED'}")

        return result

    def validate_response(self, response, expected, response_body=None) -> List[Dict]:
        """
        验证响应

        Args:
            response: HTTP响应对象
            expected: 期望结果
            response_body: 响应体内容

        Returns:
            验证结果列表
        """
        validations = []

        # 验证状态码
        if "status" in expected:
            validations.append({
                "type": "status_code",
                "expected": expected["status"],
                "actual": response.status_code,
                "passed": response.status_code == expected["status"]
            })

        # 验证响应体
        if "response" in expected and response_body:
            for key, expected_value in expected["response"].items():
                actual_value = self.get_nested_value(response_body, key)

                # 处理不同类型的验证
                if isinstance(expected_value, dict) and "_type" in expected_value:
                    validation = self.validate_special_type(
                        key, actual_value, expected_value
                    )
                else:
                    validation = {
                        "type": f"response.{key}",
                        "expected": expected_value,
                        "actual": actual_value,
                        "passed": actual_value == expected_value
                    }

                validations.append(validation)

        # 验证响应头
        if "headers" in expected:
            for header, value in expected["headers"].items():
                actual = response.headers.get(header)
                validations.append({
                    "type": f"header.{header}",
                    "expected": value,
                    "actual": actual,
                    "passed": actual == value
                })

        return validations

    def validate_special_type(self, key: str, actual: Any, expected: Dict) -> Dict:
        """
        验证特殊类型

        Args:
            key: 字段名
            actual: 实际值
            expected: 期望配置

        Returns:
            验证结果
        """
        validation = {
            "type": f"response.{key}",
            "expected": expected,
            "actual": actual
        }

        type_check = expected["_type"]

        if type_check == "array":
            min_length = expected.get("min_length", 0)
            max_length = expected.get("max_length", float('inf'))

            if isinstance(actual, list):
                length = len(actual)
                validation["passed"] = min_length <= length <= max_length
                validation["message"] = f"Array length: {length}"
            else:
                validation["passed"] = False
                validation["message"] = "Not an array"

        elif type_check == "string":
            pattern = expected.get("pattern")
            if pattern:
                import re
                validation["passed"] = bool(re.match(pattern, str(actual)))
            else:
                validation["passed"] = isinstance(actual, str)

        elif type_check == "number":
            min_val = expected.get("min", float('-inf'))
            max_val = expected.get("max", float('inf'))

            if isinstance(actual, (int, float)):
                validation["passed"] = min_val <= actual <= max_val
            else:
                validation["passed"] = False

        return validation

    def get_nested_value(self, obj: Any, key_path: str) -> Any:
        """
        获取嵌套对象的值

        Args:
            obj: 对象
            key_path: 键路径（支持点号分隔）

        Returns:
            值
        """
        keys = key_path.split('.')
        value = obj

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None

        return value

    def wait_for_completion(self, task_id: str, max_wait: int = 60) -> Dict:
        """
        等待异步任务完成

        Args:
            task_id: 任务ID
            max_wait: 最大等待时间（秒）

        Returns:
            任务结果
        """
        if not task_id:
            return {"error": "No task ID provided"}

        start = time.time()

        while time.time() - start < max_wait:
            try:
                # 查询任务状态
                response = requests.get(
                    f"{self.base_url}/api/tasks/{task_id}",
                    headers=self.headers
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") in ["completed", "failed"]:
                        return data

            except:
                pass

            time.sleep(2)

        return {"error": "Timeout waiting for task completion"}

    def run_test_suite(self, test_cases: List[Dict], parallel: bool = False) -> Dict:
        """
        执行测试套件

        Args:
            test_cases: 测试用例列表
            parallel: 是否并行执行

        Returns:
            测试结果摘要
        """
        self.start_time = datetime.now()
        logger.info(f"Starting test suite with {len(test_cases)} tests")

        if parallel:
            # 并行执行测试
            asyncio.run(self.run_tests_parallel(test_cases))
        else:
            # 顺序执行测试
            for test_case in test_cases:
                self.run_test(test_case)

                # 测试间隔
                if test_case.get("delay_after"):
                    time.sleep(test_case["delay_after"])

        self.end_time = datetime.now()

        return self.generate_summary()

    async def run_tests_parallel(self, test_cases: List[Dict]):
        """
        并行执行测试

        Args:
            test_cases: 测试用例列表
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for test_case in test_cases:
                task = asyncio.create_task(
                    self.run_test_async(session, test_case)
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks)
            self.results.extend(results)

    async def run_test_async(self, session: aiohttp.ClientSession,
                            test_case: Dict) -> Dict:
        """
        异步执行测试

        Args:
            session: aiohttp会话
            test_case: 测试用例

        Returns:
            测试结果
        """
        # TODO: 实现异步测试执行
        pass

    def generate_summary(self) -> Dict:
        """
        生成测试摘要

        Returns:
            测试摘要
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get("passed", False))
        failed = total - passed

        # 按类别统计
        categories = {}
        for result in self.results:
            cat = result.get("category", "unknown")
            if cat not in categories:
                categories[cat] = {"total": 0, "passed": 0}
            categories[cat]["total"] += 1
            if result.get("passed"):
                categories[cat]["passed"] += 1

        # 计算性能指标
        response_times = [r.get("response_time", 0) for r in self.results]
        avg_response = sum(response_times) / len(response_times) if response_times else 0

        summary = {
            "execution": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration": (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
            },
            "results": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": (passed / total * 100) if total > 0 else 0
            },
            "categories": categories,
            "performance": {
                "average_response_time": avg_response,
                "min_response_time": min(response_times) if response_times else 0,
                "max_response_time": max(response_times) if response_times else 0
            },
            "failed_tests": [
                {
                    "id": r.get("test_id"),
                    "name": r.get("name"),
                    "error": r.get("error", "Validation failed")
                }
                for r in self.results if not r.get("passed")
            ]
        }

        return summary

    def generate_report(self, format: str = "json", output_file: str = None) -> str:
        """
        生成测试报告

        Args:
            format: 报告格式 (json, html, markdown)
            output_file: 输出文件路径

        Returns:
            报告内容或文件路径
        """
        summary = self.generate_summary()

        if format == "json":
            report = json.dumps({
                "summary": summary,
                "details": self.results
            }, indent=2, default=str)

        elif format == "markdown":
            report = self.generate_markdown_report(summary)

        elif format == "html":
            report = self.generate_html_report(summary)

        else:
            report = str(summary)

        # 保存到文件
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to: {output_file}")
            return output_file

        return report

    def generate_markdown_report(self, summary: Dict) -> str:
        """生成Markdown格式报告"""
        report = f"""# n8n Workflow Test Report

## Summary
- **Date**: {summary['execution']['start_time']}
- **Duration**: {summary['execution']['duration']:.2f} seconds
- **Total Tests**: {summary['results']['total']}
- **Passed**: {summary['results']['passed']} ✅
- **Failed**: {summary['results']['failed']} ❌
- **Pass Rate**: {summary['results']['pass_rate']:.1f}%

## Category Breakdown
| Category | Total | Passed | Pass Rate |
|----------|-------|--------|-----------|
"""

        for cat, stats in summary['categories'].items():
            pass_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            report += f"| {cat} | {stats['total']} | {stats['passed']} | {pass_rate:.1f}% |\n"

        report += f"""
## Performance Metrics
- Average Response Time: {summary['performance']['average_response_time']:.2f}s
- Min Response Time: {summary['performance']['min_response_time']:.2f}s
- Max Response Time: {summary['performance']['max_response_time']:.2f}s
"""

        if summary['failed_tests']:
            report += "\n## Failed Tests\n"
            for test in summary['failed_tests']:
                report += f"- **{test['name']}** ({test['id']}): {test['error']}\n"

        return report

    def generate_html_report(self, summary: Dict) -> str:
        """生成HTML格式报告"""
        # TODO: 实现HTML报告生成
        return "<html><body>Report</body></html>"


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='n8n Workflow Test Runner')
    parser.add_argument('test_suite', help='Test suite JSON file')
    parser.add_argument('--base-url', default=os.getenv('N8N_BASE_URL', 'http://localhost:5678'),
                      help='n8n base URL')
    parser.add_argument('--api-key', help='n8n API key')
    parser.add_argument('--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('--format', choices=['json', 'markdown', 'html'],
                      default='markdown', help='Report format')
    parser.add_argument('--output', help='Output file for report')

    args = parser.parse_args()

    # 初始化测试运行器
    runner = WorkflowTestRunner(args.base_url, args.api_key)

    # 加载测试套件
    suite = runner.load_test_suite(args.test_suite)

    if not suite:
        logger.error("Failed to load test suite")
        return

    # 执行测试
    test_cases = suite.get("test_cases", [])
    runner.run_test_suite(test_cases, args.parallel)

    # 生成报告
    report = runner.generate_report(args.format, args.output)

    if not args.output:
        print(report)


if __name__ == '__main__':
    main()