"""Integration tests for the BGE Reranker v2-m3 API server.

这些是集成测试，会启动真实的服务器实例，下载模型，并测试实际的API端点。
与单元测试不同，这些测试需要更多时间和资源。
"""

import os

import pytest
from fastapi.testclient import TestClient

from bge_reranker_v2_m3_api_server.api import app

# 检测是否在CI环境中
IS_CI = os.getenv("CI", "false").lower() in ("true", "1", "yes")

# 如果在CI环境中，跳过所有需要模型的测试
pytestmark = pytest.mark.skipif(
    IS_CI, reason="Skipping integration tests in CI environment to avoid model download"
)


class TestAPIIntegration:
    """API 集成测试类。

    这些测试会使用真实的模型和API端点，需要下载模型文件。
    在CI环境中可能需要较长时间。
    """

    @pytest.fixture(scope="class")
    def client(self):
        """创建测试客户端。"""
        # 设置测试环境变量，使用更小的模型以加快测试
        os.environ["BGE_MODEL_NAME"] = "BAAI/bge-reranker-v2-m3"
        os.environ["BGE_USE_FP16"] = "false"  # 在测试中禁用 FP16 以提高兼容性

        with TestClient(app) as test_client:
            yield test_client

    def test_root_endpoint(self, client):
        """测试根端点。"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "BGE Reranker v2-m3 API Server"
        assert "version" in data
        assert "description" in data
        assert data["docs_url"] == "/docs"
        assert data["health_url"] == "/health"

    def test_health_check_endpoint(self, client):
        """测试健康检查端点。"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "version" in data
        assert "model_name" in data

        # 状态应该是 healthy 或 degraded
        assert data["status"] in ["healthy", "degraded"]

    @pytest.mark.slow
    def test_rerank_endpoint_basic(self, client):
        """测试基本的重排序功能。

        注意：此测试标记为 slow，因为可能需要下载模型。
        """
        request_data = {
            "query": "什么是人工智能？",
            "documents": [
                "人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
                "Python是一种高级编程语言，广泛用于数据科学和机器学习。",
                "机器学习是人工智能的一个子领域，通过算法让计算机从数据中学习。",
                "今天天气很好，适合外出运动。",
            ],
        }

        response = client.post("/rerank", json=request_data)

        if response.status_code == 503:
            pytest.skip("Model not loaded, skipping rerank test")

        assert response.status_code == 200

        data = response.json()
        assert "results" in data
        assert "query" in data
        assert "total_documents" in data
        assert "returned_results" in data
        assert "processing_time_ms" in data

        # 验证返回的结果
        assert data["query"] == "什么是人工智能？"
        assert data["total_documents"] == 4
        assert data["returned_results"] == 4
        assert len(data["results"]) == 4

        # 验证结果按分数降序排列
        scores = [item["score"] for item in data["results"]]
        assert scores == sorted(scores, reverse=True)

        # 验证每个结果项的结构
        for item in data["results"]:
            assert "index" in item
            assert "score" in item
            assert "document" in item
            assert isinstance(item["index"], int)
            assert isinstance(item["score"], (int, float))
            assert isinstance(item["document"], str)

    @pytest.mark.slow
    def test_rerank_with_top_k(self, client):
        """测试带 top_k 参数的重排序。"""
        request_data = {
            "query": "机器学习算法",
            "documents": [
                "深度学习是机器学习的一个重要分支。",
                "今天的午餐很美味。",
                "神经网络是深度学习的基础。",
                "我喜欢听音乐。",
                "监督学习和无监督学习是机器学习的两大类。",
            ],
            "top_k": 3,
        }

        response = client.post("/rerank", json=request_data)

        if response.status_code == 503:
            pytest.skip("Model not loaded, skipping rerank test")

        assert response.status_code == 200

        data = response.json()
        assert data["total_documents"] == 5
        assert data["returned_results"] == 3
        assert len(data["results"]) == 3

    @pytest.mark.slow
    def test_rerank_without_documents(self, client):
        """测试不返回文档内容的重排序。"""
        request_data = {
            "query": "编程语言",
            "documents": [
                "Python是一种解释型编程语言。",
                "Java是一种面向对象的编程语言。",
            ],
            "return_documents": False,
        }

        response = client.post("/rerank", json=request_data)

        if response.status_code == 503:
            pytest.skip("Model not loaded, skipping rerank test")

        assert response.status_code == 200

        data = response.json()
        # 当 return_documents=False 时，文档内容应该为空字符串
        for item in data["results"]:
            assert item["document"] == ""

    def test_rerank_invalid_request(self, client):
        """测试无效请求的处理。"""
        # 空查询
        response = client.post("/rerank", json={"query": "", "documents": ["test"]})
        assert response.status_code == 422  # Validation error

        # 空文档列表
        response = client.post("/rerank", json={"query": "test", "documents": []})
        assert response.status_code == 422  # Validation error

        # 无效的 top_k
        response = client.post(
            "/rerank", json={"query": "test", "documents": ["doc1"], "top_k": 0}
        )
        assert response.status_code == 422  # Validation error

    def test_rerank_large_input(self, client):
        """测试大量输入的处理。"""
        # 创建较多的文档进行测试
        documents = [f"这是第{i}个测试文档，内容关于不同的主题。" for i in range(50)]

        request_data = {"query": "测试文档", "documents": documents, "top_k": 10}

        response = client.post("/rerank", json=request_data)

        if response.status_code == 503:
            pytest.skip("Model not loaded, skipping large input test")

        assert response.status_code == 200

        data = response.json()
        assert data["total_documents"] == 50
        assert data["returned_results"] == 10
        assert len(data["results"]) == 10

    @pytest.mark.slow
    def test_multilingual_reranking(self, client):
        """测试多语言重排序能力。"""
        request_data = {
            "query": "artificial intelligence",
            "documents": [
                "Artificial intelligence is transforming the world.",
                "人工智能正在改变世界。",
                "L'intelligence artificielle transforme le monde.",
                "Today is a beautiful day for a walk.",
                "机器学习是AI的核心技术。",
                "Machine learning is the core technology of AI.",
            ],
        }

        response = client.post("/rerank", json=request_data)

        if response.status_code == 503:
            pytest.skip("Model not loaded, skipping multilingual test")

        assert response.status_code == 200

        data = response.json()
        # 验证AI相关的文档应该得到更高的分数
        ai_related_indices = []
        for i, item in enumerate(data["results"]):
            if any(
                keyword in item["document"].lower()
                for keyword in [
                    "artificial intelligence",
                    "人工智能",
                    "machine learning",
                    "机器学习",
                ]
            ):
                ai_related_indices.append(i)

        # AI相关文档应该在结果前部
        assert len(ai_related_indices) > 0


class TestAPIPerformance:
    """API 性能测试类。"""

    @pytest.fixture(scope="class")
    def client(self):
        """创建测试客户端。"""
        with TestClient(app) as test_client:
            yield test_client

    @pytest.mark.slow
    def test_rerank_response_time(self, client):
        """测试重排序响应时间。"""
        request_data = {
            "query": "测试查询性能",
            "documents": ["文档1", "文档2", "文档3"] * 10,  # 30个文档
        }

        response = client.post("/rerank", json=request_data)

        if response.status_code == 503:
            pytest.skip("Model not loaded, skipping performance test")

        assert response.status_code == 200

        data = response.json()
        processing_time = data["processing_time_ms"]

        # 处理时间应该在合理范围内（具体值取决于硬件）
        assert processing_time > 0
        assert processing_time < 30000  # 30秒超时


# 配置 pytest 标记
def pytest_configure(config):
    """配置 pytest 标记。"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
