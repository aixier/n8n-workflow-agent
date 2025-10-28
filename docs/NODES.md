# n8n Node Catalog

## Overview

This catalog provides a comprehensive reference for all n8n nodes supported by the Workflow Intelligence Agent.

## Node Categories

### 🔄 Trigger Nodes

#### Webhook
Triggers workflow via HTTP request.
```json
{
  "type": "webhook",
  "parameters": {
    "path": "/webhook-path",
    "method": "POST",
    "responseMode": "onReceived"
  }
}
```

#### Schedule
Triggers workflow on schedule.
```json
{
  "type": "schedule",
  "parameters": {
    "rule": {
      "interval": [{"field": "minutes", "value": 30}]
    }
  }
}
```

#### Email (IMAP)
Triggers on new emails.
```json
{
  "type": "emailReadImap",
  "parameters": {
    "mailbox": "INBOX",
    "simple": false
  }
}
```

### 📊 Data Nodes

#### HTTP Request
Makes HTTP API calls.
```json
{
  "type": "httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://api.example.com",
    "authentication": "none"
  }
}
```

#### Database (PostgreSQL)
Interacts with PostgreSQL databases.
```json
{
  "type": "postgres",
  "parameters": {
    "operation": "select",
    "query": "SELECT * FROM users"
  }
}
```

#### Spreadsheet (Google Sheets)
Reads/writes Google Sheets.
```json
{
  "type": "googleSheets",
  "parameters": {
    "operation": "read",
    "sheetId": "sheet-id",
    "range": "A1:Z100"
  }
}
```

### 🔧 Transformation Nodes

#### Function
Custom JavaScript code execution.
```json
{
  "type": "function",
  "parameters": {
    "functionCode": "return items.map(item => ({...item, processed: true}));"
  }
}
```

#### Set
Sets or removes values.
```json
{
  "type": "set",
  "parameters": {
    "values": {
      "string": [
        {"name": "status", "value": "processed"}
      ]
    }
  }
}
```

#### Merge
Combines data from multiple sources.
```json
{
  "type": "merge",
  "parameters": {
    "mode": "combine"
  }
}
```

### 🔀 Flow Control Nodes

#### IF
Conditional branching.
```json
{
  "type": "if",
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{$json.status}}",
          "operation": "equals",
          "value2": "success"
        }
      ]
    }
  }
}
```

#### Switch
Multi-path branching.
```json
{
  "type": "switch",
  "parameters": {
    "dataType": "string",
    "value1": "={{$json.type}}",
    "rules": {
      "rules": [
        {"value2": "email", "output": 0},
        {"value2": "sms", "output": 1}
      ]
    }
  }
}
```

#### Split In Batches
Process items in batches.
```json
{
  "type": "splitInBatches",
  "parameters": {
    "batchSize": 10
  }
}
```

### 📧 Communication Nodes

#### Email Send
Sends emails via SMTP.
```json
{
  "type": "emailSend",
  "parameters": {
    "fromEmail": "sender@example.com",
    "toEmail": "recipient@example.com",
    "subject": "Subject",
    "text": "Email body"
  }
}
```

#### Slack
Sends messages to Slack.
```json
{
  "type": "slack",
  "parameters": {
    "operation": "post",
    "channel": "#general",
    "text": "Message text"
  }
}
```

#### Telegram
Sends messages via Telegram.
```json
{
  "type": "telegram",
  "parameters": {
    "operation": "sendMessage",
    "chatId": "chat-id",
    "text": "Message"
  }
}
```

### 📁 File Nodes

#### Read Binary Files
Reads files from filesystem.
```json
{
  "type": "readBinaryFiles",
  "parameters": {
    "filePath": "/path/to/file"
  }
}
```

#### Write Binary File
Writes files to filesystem.
```json
{
  "type": "writeBinaryFile",
  "parameters": {
    "fileName": "/path/to/output",
    "dataPropertyName": "data"
  }
}
```

#### FTP
File transfer via FTP/SFTP.
```json
{
  "type": "ftp",
  "parameters": {
    "operation": "upload",
    "protocol": "sftp"
  }
}
```

### 🔗 Integration Nodes

#### GitHub
GitHub API operations.
```json
{
  "type": "github",
  "parameters": {
    "operation": "create",
    "resource": "issue",
    "owner": "owner",
    "repository": "repo",
    "title": "Issue title"
  }
}
```

#### AWS S3
Amazon S3 operations.
```json
{
  "type": "awsS3",
  "parameters": {
    "operation": "upload",
    "bucketName": "bucket",
    "fileName": "file.txt"
  }
}
```

#### Redis
Redis cache operations.
```json
{
  "type": "redis",
  "parameters": {
    "operation": "set",
    "key": "cache-key",
    "value": "cache-value"
  }
}
```

## Node Properties

### Common Properties

All nodes share these common properties:

- `name`: Display name of the node
- `type`: Node type identifier
- `position`: [x, y] coordinates in workflow
- `disabled`: Boolean to disable node
- `notes`: Optional notes/documentation

### Credentials

Nodes requiring authentication use credentials:

```json
{
  "credentials": {
    "postgresApi": {
      "id": "credential-id",
      "name": "My Database"
    }
  }
}
```

## Data Expression

n8n uses expressions for dynamic values:

- `{{$json.fieldName}}` - Access JSON field
- `{{$node["NodeName"].json.field}}` - Access other node's data
- `{{$env.VARIABLE_NAME}}` - Access environment variable
- `{{$parameter["paramName"]}}` - Access node parameter

## Error Handling

Configure error handling per node:

```json
{
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 1000
}
```

## Best Practices

1. **Use descriptive node names** - Makes workflows readable
2. **Add notes to complex nodes** - Document logic
3. **Handle errors gracefully** - Use continueOnFail wisely
4. **Test edge cases** - Ensure robust workflows
5. **Optimize data flow** - Minimize unnecessary transformations

## Custom Nodes

The agent can also work with custom nodes. Define them in the configuration:

```json
{
  "customNodes": [
    {
      "type": "myCustomNode",
      "displayName": "My Custom Node",
      "properties": [...]
    }
  ]
}
```