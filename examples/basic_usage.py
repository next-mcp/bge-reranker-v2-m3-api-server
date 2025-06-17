"""
BGE Reranker v2-m3 API 基本使用示例

此示例演示如何使用 Python 调用 BGE Reranker API 进行文档重排序。
"""

import asyncio
import time

import httpx


class BGERerankerClient:
    """BGE Reranker API 客户端."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """初始化客户端.

        Args:
            base_url: API 服务器地址
        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def health_check(self) -> dict:
        """检查服务健康状态."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 健康检查失败: {e}")
            raise

    async def rerank(
        self,
        query: str,
        documents: list[str],
        top_k: int | None = None,
        normalize: bool = True,
        return_documents: bool = True,
    ) -> dict:
        """对文档进行重排序.

        Args:
            query: 查询文本
            documents: 文档列表
                         top_k: 返回结果数量,None表示返回全部
            normalize: 是否使用sigmoid函数归一化分数
            return_documents: 是否在结果中返回文档内容

        Returns:
            重排序结果
        """
        payload = {
            "query": query,
            "documents": documents,
            "top_k": top_k,
            "normalize": normalize,
            "return_documents": return_documents,
        }

        try:
            response = await self.client.post(f"{self.base_url}/rerank", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 重排序请求失败: {e}")
            raise

    async def close(self):
        """关闭客户端连接."""
        await self.client.aclose()


async def main():
    """主函数演示."""
    print("🚀 BGE Reranker v2-m3 API 使用示例")
    print("=" * 50)

    # 初始化客户端
    client = BGERerankerClient()

    try:
        # 1. 健康检查
        print("\n🔍 检查服务状态...")
        health = await client.health_check()
        print(f"✅ 服务状态: {health['status']}")
        print(f"📝 服务信息: {health['service']}")

        # 2. 中文文档重排序示例
        print("\n📚 中文文档重排序示例:")
        print("-" * 30)

        query = "人工智能在医疗领域的应用"
        documents = [
            "人工智能技术在医疗诊断中发挥着重要作用,可以帮助医生更准确地诊断疾病。",
            "今天的天气非常好,阳光明媚,适合外出游玩。",
            "机器学习算法能够分析大量医疗数据,为个性化治疗提供支持。",
            "区块链技术在金融领域有广泛的应用前景。",
            "深度学习在医学影像分析中取得了突破性进展。",
        ]

        print(f"📝 查询: {query}")
        print(f"📄 文档数量: {len(documents)}")

        start_time = time.time()
        result = await client.rerank(
            query=query, documents=documents, top_k=3, normalize=True
        )
        end_time = time.time()

        print(f"⏱️  处理时间: {(end_time - start_time) * 1000:.2f}ms")
        print(f"🎯 返回结果: {result['returned_results']}/{result['total_documents']}")

        print("\n📊 重排序结果:")
        for i, item in enumerate(result["results"], 1):
            print(f"{i}. 分数: {item['score']:.4f}")
            print(f"   索引: {item['index']}")
            print(f"   文档: {item['document'][:50]}...")
            print()

        # 3. 英文文档重排序示例
        print("\n📚 English Document Reranking Example:")
        print("-" * 40)

        en_query = "machine learning algorithms for natural language processing"
        en_documents = [
            "Machine learning algorithms are widely used in natural language processing tasks.",
            "The weather is beautiful today with clear skies and sunshine.",
            "Deep learning models have revolutionized NLP applications like translation and sentiment analysis.",
            "Cooking recipes often include ingredients like flour, eggs, and sugar.",
            "Transformer architectures have become the foundation for modern NLP systems.",
            "Sports news covers the latest updates from football and basketball games.",
        ]

        print(f"📝 Query: {en_query}")
        print(f"📄 Documents: {len(en_documents)}")

        start_time = time.time()
        en_result = await client.rerank(
            query=en_query, documents=en_documents, top_k=3, normalize=True
        )
        end_time = time.time()

        print(f"⏱️  Processing time: {(end_time - start_time) * 1000:.2f}ms")
        print(
            f"🎯 Results: {en_result['returned_results']}/{en_result['total_documents']}"
        )

        print("\n📊 Reranking Results:")
        for i, item in enumerate(en_result["results"], 1):
            print(f"{i}. Score: {item['score']:.4f}")
            print(f"   Index: {item['index']}")
            print(f"   Document: {item['document'][:60]}...")
            print()

        # 4. 批量处理示例
        print("\n📚 批量处理示例:")
        print("-" * 20)

        queries = ["Python编程语言", "机器学习框架", "数据分析工具"]

        batch_documents = [
            "Python是一种高级编程语言,广泛用于数据科学和机器学习。",
            "TensorFlow是Google开发的开源机器学习框架。",
            "Pandas是Python中用于数据分析和处理的强大库。",
            "JavaScript是一种用于网页开发的编程语言。",
            "PyTorch是Facebook开发的深度学习框架。",
            "NumPy提供了高性能的多维数组对象和数学函数。",
        ]

        print(f"📝 查询数量: {len(queries)}")
        print(f"📄 文档数量: {len(batch_documents)}")

        batch_start = time.time()
        batch_results = []

        for i, query in enumerate(queries, 1):
            print(f"\n处理查询 {i}: {query}")
            result = await client.rerank(
                query=query, documents=batch_documents, top_k=2, normalize=True
            )
            batch_results.append(result)

            # 显示最相关的结果
            top_result = result["results"][0]
            print(
                f"  最佳匹配 (分数: {top_result['score']:.4f}): {top_result['document'][:40]}..."
            )

        batch_end = time.time()
        print(f"\n⏱️  批量处理总时间: {(batch_end - batch_start) * 1000:.2f}ms")
        print(
            f"📊 平均每个查询: {(batch_end - batch_start) * 1000 / len(queries):.2f}ms"
        )

    except Exception as e:
        print(f"❌ 示例运行失败: {e}")
        return False

    finally:
        await client.close()

    print("\n✅ 示例运行完成!")
    return True


def sync_example():
    """同步调用示例 (使用 requests)."""
    print("\n🔄 同步调用示例 (使用 requests):")
    print("-" * 30)

    try:
        import requests

        # 健康检查
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ 服务状态正常")

        # 重排序请求
        payload = {
            "query": "Python编程",
            "documents": ["Python是一种编程语言", "今天天气很好", "Python用于数据科学"],
            "top_k": 2,
        }

        response = requests.post(
            "http://localhost:8000/rerank", json=payload, timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ 同步请求成功")
            print(f"📊 返回 {len(result['results'])} 个结果")
            for item in result["results"]:
                print(f"  分数: {item['score']:.4f} - {item['document'][:30]}...")
        else:
            print(f"❌ 请求失败: {response.status_code}")

    except ImportError:
        print("⚠️  需要安装 requests: pip install requests")
    except Exception as e:
        print(f"❌ 同步示例失败: {e}")


if __name__ == "__main__":
    print("📘 请确保 BGE Reranker API 服务正在运行:")
    print("   命令: bge-reranker-server")
    print("   或者: docker compose up -d")
    print("   服务地址: http://localhost:8000")

    # 运行异步示例
    success = asyncio.run(main())

    if success:
        # 运行同步示例
        sync_example()

    print("\n🔗 更多信息:")
    print("  - API 文档: http://localhost:8000/docs")
    print("  - 健康检查: http://localhost:8000/health")
    print("  - 项目地址: https://github.com/yourusername/bge-reranker-v2-m3-api-server")
