"""
RAG API Endpoint Tests

RAG学習支援APIのテスト。
"""

from unittest.mock import patch


def test_rag_query_success(authenticated_client, mock_vectorstore, mock_rag_chain):
    """RAGクエリ正常実行テスト"""
    with patch("backend.api.v1.rag.get_vectorstore", return_value=mock_vectorstore):
        with patch("backend.api.v1.rag.get_rag_chain", return_value=mock_rag_chain):
            response = authenticated_client.post(
                "/api/v1/rag/query",
                json={
                    "question": "How do I create a conditional edge in LangGraph?",
                    "k": 5,
                    "include_sources": True,
                    "include_code_examples": True,
                },
            )

    assert response.status_code == 200
    data = response.json()

    # 回答が含まれること
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

    # ソースが含まれること
    assert "sources" in data
    assert isinstance(data["sources"], list)
    assert len(data["sources"]) > 0

    # ソースの構造確認
    source = data["sources"][0]
    assert "title" in source
    assert "url" in source
    assert "excerpt" in source
    assert "relevance" in source
    assert "doc_type" in source

    # コード例が含まれること
    assert "code_examples" in data
    assert isinstance(data["code_examples"], list)
    assert len(data["code_examples"]) > 0

    # コード例の構造確認
    code_example = data["code_examples"][0]
    assert "language" in code_example
    assert "code" in code_example
    assert "description" in code_example

    # 信頼度スコアが含まれること
    assert "confidence" in data
    assert 0.0 <= data["confidence"] <= 1.0

    # メタデータが含まれること
    assert "metadata" in data
    assert "model" in data["metadata"]
    assert "tokens_used" in data["metadata"]
    assert "response_time" in data["metadata"]


def test_rag_query_without_sources(authenticated_client, mock_vectorstore, mock_rag_chain):
    """ソースなしRAGクエリテスト"""
    mock_rag_chain.query.return_value = {
        "answer": "Test answer",
        "sources": [],
        "code_examples": [],
        "confidence": 0.8,
        "metadata": {"model": "gpt-4", "tokens_used": 500},
    }

    with patch("backend.api.v1.rag.get_vectorstore", return_value=mock_vectorstore):
        with patch("backend.api.v1.rag.get_rag_chain", return_value=mock_rag_chain):
            response = authenticated_client.post(
                "/api/v1/rag/query",
                json={
                    "question": "Test question",
                    "k": 3,
                    "include_sources": False,
                    "include_code_examples": False,
                },
            )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["sources"] == []
    assert data["code_examples"] == []


def test_rag_query_empty_question(authenticated_client):
    """空質問でのバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/rag/query",
        json={
            "question": "",
            "k": 5,
        },
    )

    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation error)


def test_rag_query_invalid_k(authenticated_client):
    """不正なk値でのバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/rag/query",
        json={
            "question": "Test question",
            "k": 0,  # k must be >= 1
        },
    )

    assert response.status_code == 422


def test_rag_query_k_too_large(authenticated_client):
    """k値が大きすぎる場合のバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/rag/query",
        json={
            "question": "Test question",
            "k": 100,  # k must be <= 20
        },
    )

    assert response.status_code == 422


def test_rag_health_success(authenticated_client, mock_vectorstore):
    """RAGヘルスチェック成功テスト"""
    with patch("backend.api.v1.rag.get_vectorstore", return_value=mock_vectorstore):
        response = authenticated_client.get("/api/v1/rag/health")

    assert response.status_code == 200
    data = response.json()

    assert "status" in data
    assert data["status"] == "healthy"
    assert "vectorstore_connected" in data
    assert data["vectorstore_connected"] is True
    assert "document_count" in data
    assert data["document_count"] == 100


def test_rag_health_vectorstore_error(authenticated_client):
    """VectorStoreエラー時のヘルスチェックテスト"""
    with patch("backend.api.v1.rag.get_vectorstore") as mock:
        mock_instance = mock.return_value
        mock_instance.get_collection_info.side_effect = Exception("Connection error")

        response = authenticated_client.get("/api/v1/rag/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "unhealthy"
    assert data["vectorstore_connected"] is False
    assert data["document_count"] == 0


def test_rag_query_llm_error(authenticated_client, mock_vectorstore, mock_rag_chain):
    """LLMエラー時のテスト"""
    from src.utils.exceptions import LLMError

    mock_rag_chain.query.side_effect = LLMError("OpenAI API error")

    with patch("backend.api.v1.rag.get_vectorstore", return_value=mock_vectorstore):
        with patch("backend.api.v1.rag.get_rag_chain", return_value=mock_rag_chain):
            response = authenticated_client.post(
                "/api/v1/rag/query",
                json={
                    "question": "Test question",
                },
            )

    assert response.status_code == 500
    assert "LLMエラー" in response.json()["detail"]


def test_rag_query_validation_error(authenticated_client, mock_vectorstore, mock_rag_chain):
    """バリデーションエラー時のテスト"""
    from src.utils.exceptions import ValidationError

    mock_rag_chain.query.side_effect = ValidationError("Invalid input")

    with patch("backend.api.v1.rag.get_vectorstore", return_value=mock_vectorstore):
        with patch("backend.api.v1.rag.get_rag_chain", return_value=mock_rag_chain):
            response = authenticated_client.post(
                "/api/v1/rag/query",
                json={
                    "question": "Test question",
                },
            )

    assert response.status_code == 400
    assert "バリデーションエラー" in response.json()["detail"]
