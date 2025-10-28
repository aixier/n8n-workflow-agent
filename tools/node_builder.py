#!/usr/bin/env python3
"""
n8n Node Builder
节点配置和连接构建工具

Author: AI Terminal Team
Version: 1.0.0
"""

import json
import uuid
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NodeBuilder:
    """n8n节点构建器"""

    # 节点类型映射
    NODE_TYPES = {
        # 触发器
        'webhook': 'n8n-nodes-base.webhook',
        'schedule': 'n8n-nodes-base.scheduleTrigger',
        'form': 'n8n-nodes-base.formTrigger',
        'email_trigger': 'n8n-nodes-base.emailTriggerImap',
        'file_trigger': 'n8n-nodes-base.localFileTrigger',

        # 数据节点
        'postgres': 'n8n-nodes-base.postgres',
        'mysql': 'n8n-nodes-base.mySql',
        'mongodb': 'n8n-nodes-base.mongoDb',
        'redis': 'n8n-nodes-base.redis',

        # 文件操作
        'read_file': 'n8n-nodes-base.readBinaryFile',
        'write_file': 'n8n-nodes-base.writeBinaryFile',
        'spreadsheet': 'n8n-nodes-base.spreadsheetFile',

        # 数据处理
        'code': 'n8n-nodes-base.code',
        'set': 'n8n-nodes-base.set',
        'merge': 'n8n-nodes-base.merge',
        'filter': 'n8n-nodes-base.filter',
        'split_batch': 'n8n-nodes-base.splitInBatches',

        # 控制流
        'if': 'n8n-nodes-base.if',
        'switch': 'n8n-nodes-base.switch',
        'wait': 'n8n-nodes-base.wait',
        'loop': 'n8n-nodes-base.loopOverItems',
        'stop_error': 'n8n-nodes-base.stopAndError',

        # 集成
        'http': 'n8n-nodes-base.httpRequest',
        'email': 'n8n-nodes-base.emailSend',
        'slack': 'n8n-nodes-base.slack',
        'github': 'n8n-nodes-base.github',

        # 响应
        'respond': 'n8n-nodes-base.respondToWebhook'
    }

    def __init__(self):
        """初始化节点构建器"""
        self.nodes = []
        self.connections = {}
        self.node_counter = 0
        self.position_x = 250
        self.position_y = 300

    def create_node(self, node_type: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        创建节点

        Args:
            node_type: 节点类型
            config: 节点配置

        Returns:
            节点对象
        """
        self.node_counter += 1

        # 生成节点ID
        node_id = config.get('id') if config else None
        if not node_id:
            node_id = f"node_{self.node_counter}"

        # 获取节点类型
        type_name = self.NODE_TYPES.get(node_type, node_type)

        # 创建节点
        node = {
            "id": node_id,
            "name": config.get('name', node_type.replace('_', ' ').title()) if config else node_type.replace('_', ' ').title(),
            "type": type_name,
            "typeVersion": config.get('typeVersion', 1) if config else 1,
            "position": config.get('position', [self.position_x, self.position_y]) if config else [self.position_x, self.position_y],
            "parameters": config.get('parameters', {}) if config else {}
        }

        # 添加凭证（如果需要）
        if config and 'credentials' in config:
            node['credentials'] = config['credentials']

        # 添加备注（如果有）
        if config and 'notes' in config:
            node['notes'] = config['notes']

        # 更新位置（为下一个节点）
        self.position_x += 200

        self.nodes.append(node)
        logger.info(f"✅ Created node: {node_id} ({node_type})")

        return node

    def connect_nodes(self, source_id: str, target_id: str,
                     source_output: str = 'main', target_input: str = 'main',
                     output_index: int = 0, input_index: int = 0) -> bool:
        """
        连接两个节点

        Args:
            source_id: 源节点ID
            target_id: 目标节点ID
            source_output: 源输出名称
            target_input: 目标输入名称
            output_index: 输出索引
            input_index: 输入索引

        Returns:
            是否成功连接
        """
        try:
            # 初始化源节点连接
            if source_id not in self.connections:
                self.connections[source_id] = {}

            if source_output not in self.connections[source_id]:
                self.connections[source_id][source_output] = []

            # 确保有足够的输出索引
            while len(self.connections[source_id][source_output]) <= output_index:
                self.connections[source_id][source_output].append([])

            # 添加连接
            connection = {
                "node": target_id,
                "type": target_input,
                "index": input_index
            }

            self.connections[source_id][source_output][output_index].append(connection)

            logger.info(f"✅ Connected: {source_id} → {target_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect nodes: {e}")
            return False

    def configure_node(self, node_id: str, parameters: Dict[str, Any]) -> bool:
        """
        配置节点参数

        Args:
            node_id: 节点ID
            parameters: 参数配置

        Returns:
            是否成功配置
        """
        try:
            # 查找节点
            node = next((n for n in self.nodes if n['id'] == node_id), None)

            if not node:
                logger.error(f"❌ Node not found: {node_id}")
                return False

            # 更新参数
            node['parameters'].update(parameters)

            logger.info(f"✅ Configured node: {node_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to configure node: {e}")
            return False

    def validate_node(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证节点配置

        Args:
            node: 节点对象

        Returns:
            验证结果
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # 检查必需字段
        required_fields = ['id', 'name', 'type', 'position']
        for field in required_fields:
            if field not in node:
                validation["valid"] = False
                validation["errors"].append(f"Missing required field: {field}")

        # 检查节点类型
        if node.get('type') and node['type'] not in self.NODE_TYPES.values():
            # 检查是否是完整的节点类型名称
            if not node['type'].startswith('n8n-nodes-'):
                validation["warnings"].append(f"Unknown node type: {node['type']}")

        # 检查位置
        if 'position' in node:
            if not isinstance(node['position'], list) or len(node['position']) != 2:
                validation["errors"].append("Position must be [x, y] array")

        # 检查特定节点类型的必需参数
        node_type = node.get('type', '')

        if 'webhook' in node_type:
            if 'path' not in node.get('parameters', {}):
                validation["warnings"].append("Webhook node missing 'path' parameter")

        if 'httpRequest' in node_type:
            if 'url' not in node.get('parameters', {}):
                validation["warnings"].append("HTTP Request node missing 'url' parameter")

        return validation

    def build_webhook_node(self, path: str = '/webhook', method: str = 'POST') -> Dict[str, Any]:
        """构建Webhook节点"""
        return self.create_node('webhook', {
            'name': 'Webhook Trigger',
            'parameters': {
                'path': path,
                'method': method,
                'responseMode': 'responseNode',
                'options': {}
            }
        })

    def build_schedule_node(self, cron: str = None, interval: Dict = None) -> Dict[str, Any]:
        """构建定时触发器节点"""
        parameters = {}

        if cron:
            parameters['rule'] = {
                'cronExpression': cron
            }
        elif interval:
            parameters['rule'] = {
                'interval': [interval]
            }
        else:
            # 默认每天9点
            parameters['rule'] = {
                'interval': [{
                    'triggerAtHour': 9,
                    'triggerAtMinute': 0
                }]
            }

        return self.create_node('schedule', {
            'name': 'Schedule Trigger',
            'parameters': parameters
        })

    def build_code_node(self, js_code: str, name: str = 'Code') -> Dict[str, Any]:
        """构建代码节点"""
        return self.create_node('code', {
            'name': name,
            'parameters': {
                'jsCode': js_code
            }
        })

    def build_http_node(self, url: str, method: str = 'GET', headers: Dict = None) -> Dict[str, Any]:
        """构建HTTP请求节点"""
        parameters = {
            'method': method,
            'url': url,
            'options': {}
        }

        if headers:
            parameters['sendHeaders'] = True
            parameters['headerParameters'] = {
                'parameters': [
                    {'name': k, 'value': v} for k, v in headers.items()
                ]
            }

        return self.create_node('http', {
            'name': 'HTTP Request',
            'parameters': parameters
        })

    def build_database_node(self, db_type: str, operation: str, query: str = None) -> Dict[str, Any]:
        """构建数据库节点"""
        parameters = {
            'operation': operation
        }

        if query:
            parameters['query'] = query

        return self.create_node(db_type, {
            'name': f'{db_type.title()} Database',
            'parameters': parameters
        })

    def build_if_node(self, conditions: List[Dict]) -> Dict[str, Any]:
        """构建IF条件节点"""
        return self.create_node('if', {
            'name': 'IF Condition',
            'parameters': {
                'conditions': {
                    'boolean': [],
                    'string': conditions,
                    'number': []
                },
                'combineConditions': 'all'
            }
        })

    def build_email_node(self, to: str, subject: str, body: str, from_email: str = None) -> Dict[str, Any]:
        """构建邮件发送节点"""
        parameters = {
            'toEmail': to,
            'subject': subject,
            'emailType': 'html',
            'htmlBody': body
        }

        if from_email:
            parameters['fromEmail'] = from_email

        return self.create_node('email', {
            'name': 'Send Email',
            'parameters': parameters
        })

    def build_respond_node(self, response_type: str = 'json') -> Dict[str, Any]:
        """构建响应节点"""
        return self.create_node('respond', {
            'name': 'Respond to Webhook',
            'parameters': {
                'respondWith': response_type,
                'responseBody': '={{$json}}' if response_type == 'json' else '',
                'options': {}
            }
        })

    def chain_nodes(self, node_ids: List[str]) -> bool:
        """
        链式连接多个节点

        Args:
            node_ids: 节点ID列表

        Returns:
            是否成功连接
        """
        if len(node_ids) < 2:
            logger.warning("Need at least 2 nodes to chain")
            return False

        for i in range(len(node_ids) - 1):
            if not self.connect_nodes(node_ids[i], node_ids[i + 1]):
                return False

        return True

    def build_workflow(self, name: str = None, description: str = None) -> Dict[str, Any]:
        """
        构建完整的工作流

        Args:
            name: 工作流名称
            description: 工作流描述

        Returns:
            工作流配置
        """
        workflow = {
            "name": name or f"Workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "nodes": self.nodes,
            "connections": self.connections,
            "active": False,
            "settings": {
                "executionOrder": "v1",
                "saveManualExecutions": True,
                "callerPolicy": "workflowsFromSameOwner"
            },
            "tags": []
        }

        if description:
            workflow["description"] = description

        # 验证工作流
        validation = self.validate_workflow(workflow)

        if not validation["valid"]:
            logger.warning(f"⚠️ Workflow validation failed: {validation['errors']}")

        return workflow

    def validate_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证工作流配置

        Args:
            workflow: 工作流配置

        Returns:
            验证结果
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }

        # 检查是否有节点
        if not workflow.get('nodes'):
            validation["valid"] = False
            validation["errors"].append("No nodes in workflow")
            return validation

        # 检查是否有触发器
        trigger_types = ['webhook', 'schedule', 'form', 'emailTrigger', 'fileTrigger']
        has_trigger = any(
            any(t in node.get('type', '') for t in trigger_types)
            for node in workflow['nodes']
        )

        if not has_trigger:
            validation["warnings"].append("No trigger node found")

        # 验证每个节点
        for node in workflow['nodes']:
            node_validation = self.validate_node(node)
            if not node_validation["valid"]:
                validation["valid"] = False
                validation["errors"].extend(node_validation["errors"])
            validation["warnings"].extend(node_validation["warnings"])

        # 检查连接
        if workflow.get('connections'):
            # 检查所有连接的节点是否存在
            node_ids = {node['id'] for node in workflow['nodes']}

            for source_id, outputs in workflow['connections'].items():
                if source_id not in node_ids:
                    validation["errors"].append(f"Connection from non-existent node: {source_id}")

                for output_type, connections_list in outputs.items():
                    for connections in connections_list:
                        for conn in connections:
                            if conn['node'] not in node_ids:
                                validation["errors"].append(f"Connection to non-existent node: {conn['node']}")

        return validation

    def save_workflow(self, filepath: str, workflow: Dict[str, Any] = None) -> bool:
        """
        保存工作流到文件

        Args:
            filepath: 文件路径
            workflow: 工作流配置（如果为None，使用当前构建的工作流）

        Returns:
            是否成功保存
        """
        try:
            if workflow is None:
                workflow = self.build_workflow()

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Workflow saved to: {filepath}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save workflow: {e}")
            return False

    def load_workflow(self, filepath: str) -> Dict[str, Any]:
        """
        从文件加载工作流

        Args:
            filepath: 文件路径

        Returns:
            工作流配置
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                workflow = json.load(f)

            # 加载节点和连接
            self.nodes = workflow.get('nodes', [])
            self.connections = workflow.get('connections', {})

            logger.info(f"✅ Workflow loaded from: {filepath}")
            return workflow

        except Exception as e:
            logger.error(f"❌ Failed to load workflow: {e}")
            return {}


def create_sample_workflow():
    """创建示例工作流"""
    builder = NodeBuilder()

    # 创建节点
    webhook = builder.build_webhook_node('/test')
    code = builder.build_code_node("""
const items = $input.all();
return items.map(item => ({
    json: {
        ...item.json,
        processed: true,
        timestamp: new Date().toISOString()
    }
}));
""", 'Process Data')
    respond = builder.build_respond_node('json')

    # 连接节点
    builder.chain_nodes([webhook['id'], code['id'], respond['id']])

    # 构建工作流
    workflow = builder.build_workflow('Sample Workflow', 'A simple webhook processing workflow')

    return workflow


if __name__ == '__main__':
    # 创建示例工作流
    workflow = create_sample_workflow()

    # 保存到文件
    builder = NodeBuilder()
    builder.nodes = workflow['nodes']
    builder.connections = workflow['connections']
    builder.save_workflow('sample_workflow.json', workflow)

    print(json.dumps(workflow, indent=2))