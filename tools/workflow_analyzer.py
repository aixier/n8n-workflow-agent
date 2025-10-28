#!/usr/bin/env python3
"""
n8n Workflow Analyzer
工作流分析和优化工具

Author: AI Terminal Team
Version: 1.0.0
"""

import json
import os
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import networkx as nx
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WorkflowAnalyzer:
    """工作流分析器"""

    def __init__(self):
        """初始化分析器"""
        self.workflow = None
        self.graph = None
        self.analysis_results = {}

    def load_workflow(self, workflow_path: str) -> bool:
        """
        加载工作流

        Args:
            workflow_path: 工作流文件路径

        Returns:
            是否成功加载
        """
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
            logger.info(f"Loaded workflow: {self.workflow.get('name', 'Unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to load workflow: {e}")
            return False

    def analyze_workflow(self, workflow: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        分析工作流

        Args:
            workflow: 工作流对象（可选，默认使用已加载的工作流）

        Returns:
            分析结果
        """
        if workflow:
            self.workflow = workflow

        if not self.workflow:
            return {"error": "No workflow loaded"}

        logger.info("Starting workflow analysis...")

        # 构建图结构
        self.build_graph()

        # 执行各种分析
        self.analysis_results = {
            "basic_info": self.analyze_basic_info(),
            "structure": self.analyze_structure(),
            "complexity": self.analyze_complexity(),
            "performance": self.analyze_performance(),
            "bottlenecks": self.find_bottlenecks(),
            "optimizations": self.suggest_optimizations(),
            "validation": self.validate_connections(),
            "security": self.analyze_security(),
            "best_practices": self.check_best_practices()
        }

        return self.analysis_results

    def build_graph(self):
        """构建工作流的图结构"""
        self.graph = nx.DiGraph()

        # 添加节点
        for node in self.workflow.get('nodes', []):
            self.graph.add_node(
                node['id'],
                data=node,
                type=node.get('type', ''),
                name=node.get('name', '')
            )

        # 添加边（连接）
        for source_id, outputs in self.workflow.get('connections', {}).items():
            for output_type, connections_list in outputs.items():
                for connections in connections_list:
                    for conn in connections:
                        target_id = conn['node']
                        self.graph.add_edge(
                            source_id,
                            target_id,
                            output_type=output_type,
                            input_type=conn.get('type', 'main')
                        )

    def analyze_basic_info(self) -> Dict[str, Any]:
        """分析基本信息"""
        nodes = self.workflow.get('nodes', [])

        # 统计节点类型
        node_types = {}
        for node in nodes:
            node_type = node.get('type', 'unknown')
            base_type = node_type.split('.')[-1] if '.' in node_type else node_type
            node_types[base_type] = node_types.get(base_type, 0) + 1

        return {
            "name": self.workflow.get('name', 'Unnamed'),
            "node_count": len(nodes),
            "connection_count": sum(
                len(conns) for outputs in self.workflow.get('connections', {}).values()
                for conns_list in outputs.values()
                for conns in conns_list
            ),
            "node_types": node_types,
            "is_active": self.workflow.get('active', False),
            "has_trigger": any('trigger' in node.get('type', '').lower()
                             for node in nodes),
            "has_error_handling": any('error' in node.get('type', '').lower()
                                    for node in nodes)
        }

    def analyze_structure(self) -> Dict[str, Any]:
        """分析工作流结构"""
        if not self.graph:
            return {}

        # 找出入口和出口节点
        entry_nodes = [n for n in self.graph.nodes()
                      if self.graph.in_degree(n) == 0]
        exit_nodes = [n for n in self.graph.nodes()
                     if self.graph.out_degree(n) == 0]

        # 检查是否有环
        has_cycles = not nx.is_directed_acyclic_graph(self.graph)

        # 计算最长路径
        longest_path = []
        if not has_cycles:
            try:
                longest_path = nx.dag_longest_path(self.graph)
            except:
                pass

        # 分析分支
        branch_points = [n for n in self.graph.nodes()
                        if self.graph.out_degree(n) > 1]
        merge_points = [n for n in self.graph.nodes()
                       if self.graph.in_degree(n) > 1]

        return {
            "entry_nodes": entry_nodes,
            "exit_nodes": exit_nodes,
            "has_cycles": has_cycles,
            "longest_path_length": len(longest_path),
            "longest_path": longest_path,
            "branch_points": branch_points,
            "merge_points": merge_points,
            "is_connected": nx.is_weakly_connected(self.graph),
            "components": list(nx.weakly_connected_components(self.graph))
        }

    def analyze_complexity(self) -> Dict[str, Any]:
        """分析工作流复杂度"""
        nodes = self.workflow.get('nodes', [])
        connections = self.workflow.get('connections', {})

        # 计算循环复杂度 (类似McCabe复杂度)
        # V(G) = E - N + 2P
        # E = 边数, N = 节点数, P = 连通分量数
        edge_count = sum(
            len(conns) for outputs in connections.values()
            for conns_list in outputs.values()
            for conns in conns_list
        )
        node_count = len(nodes)
        components = len(list(nx.weakly_connected_components(self.graph))) if self.graph else 1

        cyclomatic_complexity = edge_count - node_count + 2 * components

        # 计算认知复杂度
        cognitive_complexity = self.calculate_cognitive_complexity()

        # 复杂度等级
        complexity_level = self.get_complexity_level(cyclomatic_complexity)

        return {
            "cyclomatic_complexity": cyclomatic_complexity,
            "cognitive_complexity": cognitive_complexity,
            "complexity_level": complexity_level,
            "edge_count": edge_count,
            "node_count": node_count,
            "average_connections": edge_count / node_count if node_count > 0 else 0,
            "max_node_connections": max(
                self.graph.degree(n) for n in self.graph.nodes()
            ) if self.graph and self.graph.nodes() else 0
        }

    def calculate_cognitive_complexity(self) -> int:
        """计算认知复杂度"""
        complexity = 0

        for node in self.workflow.get('nodes', []):
            node_type = node.get('type', '')

            # 条件节点增加复杂度
            if 'if' in node_type.lower():
                complexity += 2
            elif 'switch' in node_type.lower():
                complexity += 3
            elif 'loop' in node_type.lower():
                complexity += 3

            # 错误处理增加复杂度
            if 'error' in node_type.lower():
                complexity += 1

            # 复杂的数据处理
            if 'code' in node_type.lower():
                complexity += 2
            elif 'function' in node_type.lower():
                complexity += 2

        # 分支增加复杂度
        if self.graph:
            branch_points = [n for n in self.graph.nodes()
                           if self.graph.out_degree(n) > 1]
            complexity += len(branch_points)

        return complexity

    def get_complexity_level(self, cyclomatic_complexity: int) -> str:
        """获取复杂度等级"""
        if cyclomatic_complexity <= 5:
            return "Simple"
        elif cyclomatic_complexity <= 10:
            return "Moderate"
        elif cyclomatic_complexity <= 20:
            return "Complex"
        else:
            return "Very Complex"

    def analyze_performance(self) -> Dict[str, Any]:
        """分析性能特征"""
        performance_issues = []
        estimated_time = 0

        for node in self.workflow.get('nodes', []):
            node_type = node.get('type', '')

            # 检查潜在的性能问题
            if 'httpRequest' in node_type:
                performance_issues.append({
                    "node": node['id'],
                    "issue": "External API call - potential latency",
                    "severity": "medium"
                })
                estimated_time += 2  # 估计2秒

            elif 'database' in node_type.lower():
                performance_issues.append({
                    "node": node['id'],
                    "issue": "Database operation - check query optimization",
                    "severity": "medium"
                })
                estimated_time += 1

            elif 'loop' in node_type.lower():
                performance_issues.append({
                    "node": node['id'],
                    "issue": "Loop operation - potential performance bottleneck",
                    "severity": "high"
                })
                estimated_time += 5

            elif 'wait' in node_type.lower():
                wait_time = node.get('parameters', {}).get('amount', 1)
                performance_issues.append({
                    "node": node['id'],
                    "issue": f"Wait operation - {wait_time}s delay",
                    "severity": "low"
                })
                estimated_time += wait_time

        # 检查并行化机会
        parallelization_opportunities = self.find_parallelization_opportunities()

        return {
            "estimated_execution_time": f"{estimated_time}s",
            "performance_issues": performance_issues,
            "parallelization_opportunities": parallelization_opportunities,
            "has_batch_processing": any('batch' in n.get('type', '').lower()
                                       for n in self.workflow.get('nodes', [])),
            "has_caching": any('cache' in str(n)
                             for n in self.workflow.get('nodes', []))
        }

    def find_bottlenecks(self) -> List[Dict[str, Any]]:
        """查找瓶颈"""
        bottlenecks = []

        if not self.graph:
            return bottlenecks

        # 查找关键路径上的节点
        if nx.is_directed_acyclic_graph(self.graph):
            try:
                critical_path = nx.dag_longest_path(self.graph)
                for node_id in critical_path:
                    node = next((n for n in self.workflow.get('nodes', [])
                               if n['id'] == node_id), None)
                    if node:
                        node_type = node.get('type', '')
                        if any(slow in node_type.lower()
                              for slow in ['http', 'database', 'loop', 'wait']):
                            bottlenecks.append({
                                "node_id": node_id,
                                "node_name": node.get('name', ''),
                                "type": "performance",
                                "reason": "Slow operation on critical path"
                            })
            except:
                pass

        # 查找高度连接的节点（可能成为瓶颈）
        for node_id in self.graph.nodes():
            degree = self.graph.degree(node_id)
            if degree > 5:
                bottlenecks.append({
                    "node_id": node_id,
                    "type": "structural",
                    "reason": f"High connectivity ({degree} connections)"
                })

        return bottlenecks

    def suggest_optimizations(self) -> List[Dict[str, Any]]:
        """建议优化"""
        optimizations = []

        # 检查是否可以添加批处理
        if not any('batch' in n.get('type', '').lower()
                  for n in self.workflow.get('nodes', [])):
            loop_nodes = [n for n in self.workflow.get('nodes', [])
                         if 'loop' in n.get('type', '').lower()]
            if loop_nodes:
                optimizations.append({
                    "type": "batch_processing",
                    "suggestion": "Consider using Split In Batches node for better performance",
                    "nodes": [n['id'] for n in loop_nodes]
                })

        # 检查并行化机会
        parallel_ops = self.find_parallelization_opportunities()
        if parallel_ops:
            optimizations.append({
                "type": "parallelization",
                "suggestion": "These operations can run in parallel",
                "nodes": parallel_ops
            })

        # 检查错误处理
        if not any('error' in n.get('type', '').lower()
                  for n in self.workflow.get('nodes', [])):
            optimizations.append({
                "type": "error_handling",
                "suggestion": "Add error handling nodes for better reliability",
                "priority": "high"
            })

        # 检查缓存机会
        repeated_api_calls = self.find_repeated_operations()
        if repeated_api_calls:
            optimizations.append({
                "type": "caching",
                "suggestion": "Consider caching results for repeated operations",
                "nodes": repeated_api_calls
            })

        return optimizations

    def find_parallelization_opportunities(self) -> List[List[str]]:
        """查找可并行化的操作"""
        parallel_groups = []

        if not self.graph:
            return parallel_groups

        # 查找可以并行执行的节点组
        for node in self.graph.nodes():
            siblings = []
            # 获取所有前驱节点
            predecessors = list(self.graph.predecessors(node))
            if predecessors:
                for pred in predecessors:
                    # 获取前驱节点的所有后继节点
                    successors = list(self.graph.successors(pred))
                    if len(successors) > 1:
                        # 这些节点可以并行执行
                        siblings = successors
                        if len(siblings) > 1 and siblings not in parallel_groups:
                            parallel_groups.append(siblings)

        return parallel_groups

    def find_repeated_operations(self) -> List[str]:
        """查找重复的操作"""
        repeated = []
        node_types = {}

        for node in self.workflow.get('nodes', []):
            node_type = node.get('type', '')
            if 'http' in node_type.lower():
                # 检查是否有相同的URL
                url = node.get('parameters', {}).get('url', '')
                if url:
                    if url in node_types:
                        node_types[url].append(node['id'])
                    else:
                        node_types[url] = [node['id']]

        # 找出重复的
        for url, nodes in node_types.items():
            if len(nodes) > 1:
                repeated.extend(nodes)

        return repeated

    def validate_connections(self) -> Dict[str, Any]:
        """验证连接"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # 检查断开的节点
        if self.graph:
            isolated_nodes = list(nx.isolates(self.graph))
            if isolated_nodes:
                validation_results["warnings"].append({
                    "type": "isolated_nodes",
                    "nodes": isolated_nodes,
                    "message": "These nodes are not connected to the workflow"
                })

        # 检查必需的连接
        for node in self.workflow.get('nodes', []):
            node_type = node.get('type', '')
            node_id = node['id']

            # Webhook响应节点必须有输入
            if 'respondToWebhook' in node_type:
                if self.graph and self.graph.in_degree(node_id) == 0:
                    validation_results["errors"].append({
                        "type": "missing_input",
                        "node": node_id,
                        "message": "Respond to Webhook node needs input"
                    })
                    validation_results["valid"] = False

        # 检查循环引用
        if self.graph and not nx.is_directed_acyclic_graph(self.graph):
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                validation_results["warnings"].append({
                    "type": "cycles",
                    "cycles": cycles,
                    "message": "Workflow contains cycles"
                })

        return validation_results

    def analyze_security(self) -> Dict[str, Any]:
        """分析安全性"""
        security_issues = []

        for node in self.workflow.get('nodes', []):
            node_type = node.get('type', '')
            params = node.get('parameters', {})

            # 检查硬编码的凭证
            params_str = json.dumps(params)
            if any(sensitive in params_str.lower()
                  for sensitive in ['password', 'api_key', 'secret', 'token']):
                security_issues.append({
                    "node": node['id'],
                    "issue": "Possible hardcoded credentials",
                    "severity": "high"
                })

            # 检查SQL注入风险
            if 'database' in node_type.lower():
                query = params.get('query', '')
                if '{{' in query and 'prepare' not in params:
                    security_issues.append({
                        "node": node['id'],
                        "issue": "Potential SQL injection risk",
                        "severity": "high",
                        "suggestion": "Use prepared statements"
                    })

            # 检查不安全的HTTP
            if 'http' in node_type.lower():
                url = params.get('url', '')
                if url.startswith('http://'):
                    security_issues.append({
                        "node": node['id'],
                        "issue": "Using insecure HTTP",
                        "severity": "medium",
                        "suggestion": "Use HTTPS"
                    })

        return {
            "issues": security_issues,
            "has_authentication": any('auth' in str(n).lower()
                                    for n in self.workflow.get('nodes', [])),
            "uses_credentials": any('credentials' in n
                                  for n in self.workflow.get('nodes', []))
        }

    def check_best_practices(self) -> List[Dict[str, str]]:
        """检查最佳实践"""
        recommendations = []

        # 检查命名
        for node in self.workflow.get('nodes', []):
            if node.get('name', '') == node.get('type', '').split('.')[-1]:
                recommendations.append({
                    "node": node['id'],
                    "issue": "Node using default name",
                    "suggestion": "Give descriptive names to nodes"
                })

        # 检查工作流名称
        if self.workflow.get('name', '') == '':
            recommendations.append({
                "issue": "Workflow has no name",
                "suggestion": "Give a descriptive name to the workflow"
            })

        # 检查错误处理
        if not any('error' in n.get('type', '').lower()
                  for n in self.workflow.get('nodes', [])):
            recommendations.append({
                "issue": "No error handling",
                "suggestion": "Add error handling for reliability"
            })

        # 检查日志记录
        if not any('log' in str(n).lower()
                  for n in self.workflow.get('nodes', [])):
            recommendations.append({
                "issue": "No logging",
                "suggestion": "Consider adding logging for debugging"
            })

        return recommendations

    def generate_report(self, output_file: str = None) -> str:
        """
        生成分析报告

        Args:
            output_file: 输出文件路径

        Returns:
            报告内容
        """
        report = f"""# Workflow Analysis Report

Generated: {datetime.now().isoformat()}

## Basic Information
- **Name**: {self.analysis_results.get('basic_info', {}).get('name', 'Unknown')}
- **Nodes**: {self.analysis_results.get('basic_info', {}).get('node_count', 0)}
- **Connections**: {self.analysis_results.get('basic_info', {}).get('connection_count', 0)}
- **Active**: {self.analysis_results.get('basic_info', {}).get('is_active', False)}

## Complexity Analysis
- **Cyclomatic Complexity**: {self.analysis_results.get('complexity', {}).get('cyclomatic_complexity', 0)}
- **Cognitive Complexity**: {self.analysis_results.get('complexity', {}).get('cognitive_complexity', 0)}
- **Level**: {self.analysis_results.get('complexity', {}).get('complexity_level', 'Unknown')}

## Performance Analysis
- **Estimated Execution Time**: {self.analysis_results.get('performance', {}).get('estimated_execution_time', 'Unknown')}
- **Performance Issues**: {len(self.analysis_results.get('performance', {}).get('performance_issues', []))}

## Bottlenecks
"""
        for bottleneck in self.analysis_results.get('bottlenecks', []):
            report += f"- {bottleneck.get('node_id', '')}: {bottleneck.get('reason', '')}\n"

        report += "\n## Optimization Suggestions\n"
        for opt in self.analysis_results.get('optimizations', []):
            report += f"- **{opt.get('type', '')}**: {opt.get('suggestion', '')}\n"

        report += "\n## Security Analysis\n"
        security = self.analysis_results.get('security', {})
        for issue in security.get('issues', []):
            report += f"- **{issue.get('severity', '')}**: {issue.get('issue', '')} (Node: {issue.get('node', '')})\n"

        # 保存报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info(f"Report saved to: {output_file}")

        return report


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='n8n Workflow Analyzer')
    parser.add_argument('workflow_file', help='Workflow JSON file to analyze')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--format', choices=['text', 'json'],
                      default='text', help='Report format')

    args = parser.parse_args()

    # 创建分析器
    analyzer = WorkflowAnalyzer()

    # 加载工作流
    if not analyzer.load_workflow(args.workflow_file):
        return

    # 分析工作流
    results = analyzer.analyze_workflow()

    # 生成报告
    if args.format == 'json':
        report = json.dumps(results, indent=2, default=str)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
        else:
            print(report)
    else:
        report = analyzer.generate_report(args.output)
        if not args.output:
            print(report)


if __name__ == '__main__':
    main()