# n8n Webhook Activation Guide

## 问题诊断

当前所有webhook端点返回404错误，尽管工作流显示为"激活"状态。这是因为通过API创建的工作流的webhook需要在n8n UI中手动保存才能正确注册。

## 激活Webhook的步骤

### 方法1：手动保存工作流（推荐）

1. **打开n8n UI**
   - 访问: http://localhost:5679
   - 登录到你的n8n实例

2. **找到YouTube工作流**
   - 在工作流列表中找到以下工作流：
     - `YouTube2Post Simple - Working Version`
     - `YouTube Processor Test - 20251029_111823`
     - `YouTube2Post - Video to Article Generator`

3. **保存每个工作流**
   - 打开工作流
   - 点击Webhook节点查看配置
   - 按 `Ctrl+S` 或点击保存按钮
   - 确认右上角的激活开关是打开的

4. **验证Webhook URL**
   - 在Webhook节点中会显示production URL
   - 复制这个URL用于测试

### 方法2：使用测试模式

1. **打开工作流**
   - 在n8n UI中打开目标工作流

2. **点击"Execute Workflow"按钮**
   - 这会生成一个临时的test webhook URL
   - Test URL格式: `/webhook-test/{workflow-id}/{path}`

3. **发送测试请求**
   - Test webhook只能使用一次
   - 每次测试前需要重新点击"Execute Workflow"

### 方法3：重启n8n服务

如果上述方法都不起作用：

```bash
# 如果使用Docker
docker restart [n8n-container-name]

# 如果使用PM2
pm2 restart n8n

# 如果直接运行
# 停止服务并重新启动
```

## 测试Webhook

保存工作流后，使用以下命令测试：

```bash
# 测试 YouTube2Post Simple
curl -X POST http://localhost:5679/webhook/youtube2post-simple \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "language": "zh-CN"}'

# 测试 YouTube Processor
curl -X POST http://localhost:5679/webhook/youtube-processor-20251029111823 \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=test123"}'

# 测试 YouTube2Post Video to Article
curl -X POST http://localhost:5679/webhook/youtube2post \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://youtu.be/dQw4w9WgXcQ", "language": "en-US"}'
```

## 验证脚本

运行Python验证脚本：

```bash
python3 test_youtube_webhooks.py
```

## 预期结果

成功激活后，webhook应该返回：
- **Status Code**: 200
- **Response**: JSON格式的处理结果，包含：
  - videoId: 提取的YouTube视频ID
  - status: 处理状态
  - timestamp: 处理时间
  - 其他处理数据

## 故障排除

1. **Webhook仍然返回404**
   - 确认工作流确实被激活（检查右上角开关）
   - 尝试删除并重新创建Webhook节点
   - 检查webhook路径是否正确（不要有空格或特殊字符）

2. **Webhook返回500错误**
   - 检查工作流内部是否有错误
   - 查看n8n日志获取详细错误信息
   - 验证节点之间的连接是否正确

3. **请求超时**
   - 工作流可能正在处理
   - 检查是否有无限循环
   - 增加timeout时间

## 已知限制

- 通过API创建的webhook需要UI干预才能激活
- Test webhooks每次只能使用一次
- 某些n8n版本的API不支持直接激活工作流
- Webhook路径必须唯一，不能重复

## 下一步

1. 按照上述步骤激活webhook
2. 运行测试脚本验证
3. 确认所有webhook正常工作后，可以开始使用YouTube处理功能