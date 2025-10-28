#!/usr/bin/env python3
"""
n8n Workflow Manager
工作流生命周期管理工具

Author: AI Terminal Team
Version: 1.0.0
"""

import json
import os
import sys
import time
import requests
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class N8nWorkflowManager:
    """n8n工作流管理器"""

    def __init__(self, base_url: str = None, api_key: str = None):
        """
        初始化工作流管理器

        Args:
            base_url: n8n实例URL (默认从环境变量读取)
            api_key: API密钥 (默认从环境变量读取)
        """
        self.base_url = base_url or os.getenv('N8N_BASE_URL', 'http://localhost:5678')
        self.api_key = api_key or os.getenv('N8N_API_KEY', '')

        if not self.api_key:
            # 尝试从.env.local文件读取
            env_file = Path(__file__).parent / '.env.local'
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('N8N_API_KEY='):
                            self.api_key = line.split('=', 1)[1].strip()
                            break

        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

        self.api_url = f"{self.base_url}/api/v1"

    def test_connection(self) -> bool:
        """测试n8n连接"""
        try:
            response = requests.get(
                f"{self.api_url}/workflows",
                headers=self.headers,
                timeout=5
            )
            if response.status_code == 200:
                logger.info("✅ Successfully connected to n8n")
                return True
            else:
                logger.error(f"❌ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Connection error: {e}")
            return False

    def create_workflow(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新工作流

        Args:
            config: 工作流配置

        Returns:
            创建的工作流信息
        """
        try:
            # 准备工作流数据
            workflow_data = {
                "name": config.get("name", f"Workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                "nodes": config.get("nodes", []),
                "connections": config.get("connections", {}),
                "active": config.get("active", False),
                "settings": config.get("settings", {
                    "executionOrder": "v1",
                    "saveManualExecutions": True,
                    "callerPolicy": "workflowsFromSameOwner"
                }),
                "staticData": config.get("staticData", None),
                "tags": config.get("tags", [])
            }

            # 发送创建请求
            response = requests.post(
                f"{self.api_url}/workflows",
                headers=self.headers,
                json=workflow_data
            )

            if response.status_code in [200, 201]:
                workflow = response.json()
                logger.info(f"✅ Workflow created successfully: {workflow.get('id')}")
                return workflow
            else:
                logger.error(f"❌ Failed to create workflow: {response.text}")
                return {"error": response.text, "status_code": response.status_code}

        except Exception as e:
            logger.error(f"❌ Error creating workflow: {e}")
            return {"error": str(e)}

    def deploy_workflow(self, workflow: Dict[str, Any]) -> bool:
        """
        部署工作流（激活）

        Args:
            workflow: 工作流对象或ID

        Returns:
            是否成功激活
        """
        try:
            workflow_id = workflow if isinstance(workflow, str) else workflow.get('id')

            # 激活工作流
            response = requests.patch(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers,
                json={"active": True}
            )

            if response.status_code == 200:
                logger.info(f"✅ Workflow {workflow_id} deployed successfully")
                return True
            else:
                logger.error(f"❌ Failed to deploy workflow: {response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ Error deploying workflow: {e}")
            return False

    def update_workflow(self, workflow_id: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        更新工作流

        Args:
            workflow_id: 工作流ID
            changes: 要更新的内容

        Returns:
            更新后的工作流
        """
        try:
            # 获取现有工作流
            response = requests.get(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers
            )

            if response.status_code != 200:
                return {"error": f"Workflow not found: {workflow_id}"}

            workflow = response.json()

            # 应用更改
            for key, value in changes.items():
                if key == "nodes" and isinstance(value, list):
                    # 添加或更新节点
                    workflow["nodes"] = value
                elif key == "connections":
                    # 更新连接
                    workflow["connections"] = value
                elif key == "add_node":
                    # 添加单个节点
                    workflow["nodes"].append(value)
                elif key == "remove_node":
                    # 移除节点
                    workflow["nodes"] = [n for n in workflow["nodes"] if n["id"] != value]
                else:
                    workflow[key] = value

            # 更新工作流
            response = requests.patch(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers,
                json=workflow
            )

            if response.status_code == 200:
                logger.info(f"✅ Workflow {workflow_id} updated successfully")
                return response.json()
            else:
                logger.error(f"❌ Failed to update workflow: {response.text}")
                return {"error": response.text}

        except Exception as e:
            logger.error(f"❌ Error updating workflow: {e}")
            return {"error": str(e)}

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        删除工作流

        Args:
            workflow_id: 工作流ID

        Returns:
            是否成功删除
        """
        try:
            response = requests.delete(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers
            )

            if response.status_code in [200, 204]:
                logger.info(f"✅ Workflow {workflow_id} deleted successfully")
                return True
            else:
                logger.error(f"❌ Failed to delete workflow: {response.text}")
                return False

        except Exception as e:
            logger.error(f"❌ Error deleting workflow: {e}")
            return False

    def backup_workflow(self, workflow_id: str, backup_dir: str = "./backups") -> str:
        """
        备份工作流

        Args:
            workflow_id: 工作流ID
            backup_dir: 备份目录

        Returns:
            备份文件路径
        """
        try:
            # 获取工作流
            response = requests.get(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers
            )

            if response.status_code != 200:
                logger.error(f"❌ Failed to get workflow for backup")
                return ""

            workflow = response.json()

            # 创建备份目录
            Path(backup_dir).mkdir(parents=True, exist_ok=True)

            # 生成备份文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{backup_dir}/workflow_{workflow_id}_{timestamp}.json"

            # 保存备份
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Workflow backed up to: {backup_file}")
            return backup_file

        except Exception as e:
            logger.error(f"❌ Error backing up workflow: {e}")
            return ""

    def restore_workflow(self, backup_file: str) -> Dict[str, Any]:
        """
        从备份恢复工作流

        Args:
            backup_file: 备份文件路径

        Returns:
            恢复的工作流
        """
        try:
            # 读取备份文件
            with open(backup_file, 'r', encoding='utf-8') as f:
                workflow = json.load(f)

            # 移除ID以创建新工作流
            workflow.pop('id', None)

            # 添加恢复标记
            workflow['name'] = f"{workflow.get('name', 'Workflow')}_restored_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # 创建工作流
            return self.create_workflow(workflow)

        except Exception as e:
            logger.error(f"❌ Error restoring workflow: {e}")
            return {"error": str(e)}

    def list_workflows(self, active_only: bool = False) -> List[Dict[str, Any]]:
        """
        列出所有工作流

        Args:
            active_only: 是否只列出激活的工作流

        Returns:
            工作流列表
        """
        try:
            response = requests.get(
                f"{self.api_url}/workflows",
                headers=self.headers
            )

            if response.status_code == 200:
                workflows = response.json().get('data', [])

                if active_only:
                    workflows = [w for w in workflows if w.get('active')]

                logger.info(f"Found {len(workflows)} workflows")
                return workflows
            else:
                logger.error(f"❌ Failed to list workflows: {response.text}")
                return []

        except Exception as e:
            logger.error(f"❌ Error listing workflows: {e}")
            return []

    def execute_workflow(self, workflow_id: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        手动执行工作流

        Args:
            workflow_id: 工作流ID
            data: 输入数据

        Returns:
            执行结果
        """
        try:
            execution_data = {
                "workflowData": {
                    "id": workflow_id
                }
            }

            if data:
                execution_data["data"] = data

            response = requests.post(
                f"{self.api_url}/workflows/{workflow_id}/execute",
                headers=self.headers,
                json=execution_data
            )

            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Workflow executed successfully: {result.get('id')}")
                return result
            else:
                logger.error(f"❌ Failed to execute workflow: {response.text}")
                return {"error": response.text}

        except Exception as e:
            logger.error(f"❌ Error executing workflow: {e}")
            return {"error": str(e)}

    def get_workflow_executions(self, workflow_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取工作流执行历史

        Args:
            workflow_id: 工作流ID
            limit: 返回数量限制

        Returns:
            执行历史列表
        """
        try:
            response = requests.get(
                f"{self.api_url}/executions",
                headers=self.headers,
                params={
                    "workflowId": workflow_id,
                    "limit": limit
                }
            )

            if response.status_code == 200:
                executions = response.json().get('data', [])
                logger.info(f"Found {len(executions)} executions for workflow {workflow_id}")
                return executions
            else:
                logger.error(f"❌ Failed to get executions: {response.text}")
                return []

        except Exception as e:
            logger.error(f"❌ Error getting executions: {e}")
            return []

    def import_workflow(self, file_path: str, activate: bool = False) -> Dict[str, Any]:
        """
        从文件导入工作流

        Args:
            file_path: 工作流JSON文件路径
            activate: 是否自动激活

        Returns:
            导入的工作流
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_config = json.load(f)

            # 设置激活状态
            workflow_config['active'] = activate

            # 创建工作流
            return self.create_workflow(workflow_config)

        except Exception as e:
            logger.error(f"❌ Error importing workflow: {e}")
            return {"error": str(e)}

    def export_workflow(self, workflow_id: str, output_path: str = None) -> str:
        """
        导出工作流到文件

        Args:
            workflow_id: 工作流ID
            output_path: 输出文件路径

        Returns:
            导出的文件路径
        """
        try:
            # 获取工作流
            response = requests.get(
                f"{self.api_url}/workflows/{workflow_id}",
                headers=self.headers
            )

            if response.status_code != 200:
                logger.error(f"❌ Failed to get workflow for export")
                return ""

            workflow = response.json()

            # 生成输出路径
            if not output_path:
                output_path = f"workflow_{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # 保存到文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(workflow, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Workflow exported to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"❌ Error exporting workflow: {e}")
            return ""


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='n8n Workflow Manager')
    parser.add_argument('--base-url', default=os.getenv('N8N_BASE_URL', 'http://localhost:5678'),
                        help='n8n base URL')
    parser.add_argument('--api-key', default=os.getenv('N8N_API_KEY', ''),
                        help='n8n API key')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # test command
    subparsers.add_parser('test', help='Test n8n connection')

    # list command
    list_parser = subparsers.add_parser('list', help='List workflows')
    list_parser.add_argument('--active', action='store_true', help='Only show active workflows')

    # create command
    create_parser = subparsers.add_parser('create', help='Create workflow')
    create_parser.add_argument('config', help='Workflow configuration file')
    create_parser.add_argument('--activate', action='store_true', help='Activate after creation')

    # deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy (activate) workflow')
    deploy_parser.add_argument('workflow_id', help='Workflow ID')

    # update command
    update_parser = subparsers.add_parser('update', help='Update workflow')
    update_parser.add_argument('workflow_id', help='Workflow ID')
    update_parser.add_argument('changes', help='Changes JSON file')

    # delete command
    delete_parser = subparsers.add_parser('delete', help='Delete workflow')
    delete_parser.add_argument('workflow_id', help='Workflow ID')

    # backup command
    backup_parser = subparsers.add_parser('backup', help='Backup workflow')
    backup_parser.add_argument('workflow_id', help='Workflow ID')
    backup_parser.add_argument('--dir', default='./backups', help='Backup directory')

    # restore command
    restore_parser = subparsers.add_parser('restore', help='Restore workflow')
    restore_parser.add_argument('backup_file', help='Backup file path')

    # execute command
    execute_parser = subparsers.add_parser('execute', help='Execute workflow')
    execute_parser.add_argument('workflow_id', help='Workflow ID')
    execute_parser.add_argument('--data', help='Input data JSON file')

    # import command
    import_parser = subparsers.add_parser('import', help='Import workflow')
    import_parser.add_argument('file', help='Workflow JSON file')
    import_parser.add_argument('--activate', action='store_true', help='Activate after import')

    # export command
    export_parser = subparsers.add_parser('export', help='Export workflow')
    export_parser.add_argument('workflow_id', help='Workflow ID')
    export_parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    # 初始化管理器
    manager = N8nWorkflowManager(args.base_url, args.api_key)

    # 执行命令
    if args.command == 'test':
        manager.test_connection()

    elif args.command == 'list':
        workflows = manager.list_workflows(args.active)
        for w in workflows:
            status = "🟢" if w.get('active') else "⚪"
            print(f"{status} {w.get('id')} - {w.get('name')}")

    elif args.command == 'create':
        with open(args.config, 'r') as f:
            config = json.load(f)
        workflow = manager.create_workflow(config)
        if args.activate and not workflow.get('error'):
            manager.deploy_workflow(workflow)

    elif args.command == 'deploy':
        manager.deploy_workflow(args.workflow_id)

    elif args.command == 'update':
        with open(args.changes, 'r') as f:
            changes = json.load(f)
        manager.update_workflow(args.workflow_id, changes)

    elif args.command == 'delete':
        manager.delete_workflow(args.workflow_id)

    elif args.command == 'backup':
        manager.backup_workflow(args.workflow_id, args.dir)

    elif args.command == 'restore':
        manager.restore_workflow(args.backup_file)

    elif args.command == 'execute':
        data = None
        if args.data:
            with open(args.data, 'r') as f:
                data = json.load(f)
        manager.execute_workflow(args.workflow_id, data)

    elif args.command == 'import':
        manager.import_workflow(args.file, args.activate)

    elif args.command == 'export':
        manager.export_workflow(args.workflow_id, args.output)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()