# BGE Reranker v2-m3 API cURL 使用示例

本文档提供了使用 cURL 命令调用 BGE Reranker API 的各种示例。

## 前提条件

确保 BGE Reranker API 服务正在运行：

```bash
# 方式1: 直接启动
bge-reranker-server

# 方式2: Docker 启动
docker compose up -d

# 方式3: Docker 直接运行
docker run -d -p 8000:8000 yarnovo/bge-reranker-v2-m3-api-server:latest
```

服务默认运行在 `http://localhost:8000`

## 健康检查

检查服务是否正常运行：

```bash
curl -X GET "http://localhost:8000/health" \
  -H "accept: application/json"
```

**预期响应：**
```json
{
  "status": "healthy",
  "service": "BGE Reranker v2-m3 API Server",
  "version": "0.1.0",
  "model_loaded": true,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## 基础重排序

### 中文文档重排序

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "query": "人工智能在医疗领域的应用",
    "documents": [
      "人工智能技术在医疗诊断中发挥着重要作用，可以帮助医生更准确地诊断疾病。",
      "今天的天气非常好，阳光明媚，适合外出游玩。",
      "机器学习算法能够分析大量医疗数据，为个性化治疗提供支持。",
      "区块链技术在金融领域有广泛的应用前景。",
      "深度学习在医学影像分析中取得了突破性进展。"
    ]
  }'
```

### 英文文档重排序

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "query": "machine learning algorithms for natural language processing",
    "documents": [
      "Machine learning algorithms are widely used in natural language processing tasks.",
      "The weather is beautiful today with clear skies and sunshine.",
      "Deep learning models have revolutionized NLP applications like translation and sentiment analysis.",
      "Cooking recipes often include ingredients like flour, eggs, and sugar.",
      "Transformer architectures have become the foundation for modern NLP systems."
    ]
  }'
```

## 高级参数使用

### 限制返回结果数量 (top_k)

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "query": "Python编程语言",
    "documents": [
      "Python是一种高级编程语言，广泛用于数据科学和机器学习。",
      "JavaScript是一种用于网页开发的编程语言。",
      "Java是一种面向对象的编程语言，广泛用于企业级应用开发。",
      "C++是一种系统编程语言，常用于性能要求高的应用。",
      "Go是Google开发的编程语言，注重简洁和高效。"
    ],
    "top_k": 3
  }'
```

### 禁用分数归一化

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "query": "数据分析工具",
    "documents": [
      "Pandas是Python中用于数据分析和处理的强大库。",
      "Excel是Microsoft开发的电子表格应用程序。",
      "Tableau是一款数据可视化工具。"
    ],
    "normalize": false
  }'
```

### 仅返回分数和索引（不返回文档内容）

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "query": "深度学习框架",
    "documents": [
      "TensorFlow是Google开发的开源机器学习框架。",
      "PyTorch是Facebook开发的深度学习框架。",
      "Keras是高级神经网络API，运行在TensorFlow之上。"
    ],
    "return_documents": false
  }'
```

### 完整参数示例

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "query": "自然语言处理技术",
    "documents": [
      "BERT是Google开发的预训练语言模型，在多项NLP任务上取得了突破性成果。",
      "今天下午有一场足球比赛，天气预报说会下雨。",
      "GPT系列模型展示了大规模语言模型在文本生成方面的强大能力。",
      "Transformer架构彻底改变了自然语言处理领域的发展方向。",
      "推荐系统在电商和内容平台中发挥着重要作用。",
      "LSTM和GRU是处理序列数据的重要循环神经网络结构。"
    ],
    "top_k": 4,
    "normalize": true,
    "return_documents": true
  }'
```

## 批量处理示例

### 多个查询顺序处理

```bash
# 查询1: Python相关
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Python数据科学",
    "documents": ["NumPy提供数组计算", "Pandas处理数据", "Matplotlib绘制图表"],
    "top_k": 2
  }'

# 查询2: 机器学习相关  
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "机器学习算法",
    "documents": ["线性回归用于预测", "随机森林是集成方法", "神经网络模拟大脑"],
    "top_k": 2
  }'
```

### 使用脚本批量处理

创建 `batch_rerank.sh` 文件：

```bash
#!/bin/bash

# 定义基础URL
BASE_URL="http://localhost:8000"

# 查询列表
queries=(
  "人工智能"
  "机器学习"  
  "深度学习"
)

# 文档列表
documents='[
  "人工智能是计算机科学的一个分支，旨在创造智能机器。",
  "机器学习是人工智能的子集，专注于算法和统计模型。", 
  "深度学习使用神经网络来模拟人脑的学习过程。",
  "云计算提供按需访问计算资源的服务模式。",
  "区块链是一种分布式账本技术。"
]'

# 处理每个查询
for query in "${queries[@]}"; do
  echo "处理查询: $query"
  
  curl -X POST "$BASE_URL/rerank" \
    -H "Content-Type: application/json" \
    -d "{
      \"query\": \"$query\",
      \"documents\": $documents,
      \"top_k\": 3
    }" | jq '.results[] | {score: .score, document: .document}'
    
  echo "---"
done
```

运行批量处理：

```bash
chmod +x batch_rerank.sh
./batch_rerank.sh
```

## 错误处理示例

### 无效的请求体

```bash
curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "",
    "documents": []
  }'
```

**错误响应：**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "query"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

### 服务不可用

```bash
# 当服务未启动时
curl -X GET "http://localhost:8000/health"
```

**错误响应：**
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

## 性能测试

### 简单性能测试

```bash
# 测试单个请求的响应时间
time curl -X POST "http://localhost:8000/rerank" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "测试查询",
    "documents": ["文档1", "文档2", "文档3", "文档4", "文档5"]
  }' > /dev/null
```

### 并发测试 (需要安装 apache2-utils)

```bash
# 10个并发，总共100个请求
echo '{
  "query": "并发测试",
  "documents": ["文档A", "文档B", "文档C"]
}' > test_payload.json

ab -n 100 -c 10 -T "application/json" -p test_payload.json \
  "http://localhost:8000/rerank"
```

## 集成示例

### 在 Shell 脚本中使用

```bash
#!/bin/bash

# 函数：调用重排序API
rerank_documents() {
  local query="$1"
  local docs="$2"
  
  curl -s -X POST "http://localhost:8000/rerank" \
    -H "Content-Type: application/json" \
    -d "{
      \"query\": \"$query\",
      \"documents\": $docs,
      \"top_k\": 3
    }" | jq -r '.results[] | "\(.score): \(.document)"'
}

# 使用示例
query="机器学习"
documents='["监督学习使用标记数据", "无监督学习发现数据模式", "强化学习通过奖励学习"]'

echo "查询: $query"
echo "重排序结果:"
rerank_documents "$query" "$documents"
```

### 在 Python 中使用 subprocess

```python
import subprocess
import json

def call_rerank_api(query, documents, top_k=None):
    payload = {
        "query": query,
        "documents": documents
    }
    if top_k:
        payload["top_k"] = top_k
    
    cmd = [
        "curl", "-s", "-X", "POST", "http://localhost:8000/rerank",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# 使用示例
response = call_rerank_api(
    "Python编程", 
    ["Python是编程语言", "Java是编程语言", "Python用于AI"]
)
print(f"最佳匹配: {response['results'][0]['document']}")
```

## 监控和日志

### 检查服务状态

```bash
# 持续监控健康状态
watch -n 5 'curl -s http://localhost:8000/health | jq .'
```

### 获取 API 文档

```bash
# 获取 OpenAPI 规范
curl -X GET "http://localhost:8000/openapi.json" | jq .

# 访问交互式文档
# 浏览器打开: http://localhost:8000/docs
# 或 ReDoc: http://localhost:8000/redoc
```

## 故障排除

### 常见问题

1. **连接被拒绝**
   ```bash
   # 检查服务是否运行
   curl -I http://localhost:8000/health
   
   # 检查端口占用
   netstat -an | grep 8000
   ```

2. **请求超时**
   ```bash
   # 增加超时时间
   curl --connect-timeout 30 --max-time 60 \
     -X POST "http://localhost:8000/rerank" \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "documents": ["doc1"]}'
   ```

3. **JSON 格式错误**
   ```bash
   # 使用 jq 验证 JSON
   echo '{"query": "test", "documents": ["doc1"]}' | jq .
   ```

## 更多信息

- **API 文档**: http://localhost:8000/docs
- **项目地址**: https://github.com/yourusername/bge-reranker-v2-m3-api-server
- **模型信息**: [BAAI/bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) 
