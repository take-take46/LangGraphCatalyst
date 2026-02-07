"""
FastAPI Test Configuration

FastAPIテストクライアントとフィクスチャを提供します。
"""

from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from backend.core.config import Settings
from backend.main import app


@pytest.fixture
def test_settings():
    """テスト用設定"""
    return Settings(
        openai_api_key="sk-test-mock-key",
        chroma_persist_dir="./tests/data/chroma_test",
        log_level="DEBUG",
        environment="test",
        cors_origins="http://localhost:5173,http://localhost:3000",
        jwt_secret_key="test-secret-key",
    )


@pytest.fixture
def client():
    """FastAPIテストクライアント"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_vectorstore():
    """モックVectorStore"""
    with patch("backend.api.v1.rag.ChromaVectorStore") as mock:
        instance = Mock()
        instance.get_collection_info.return_value = {"document_count": 100}
        mock.return_value = instance
        yield instance


@pytest.fixture
def mock_rag_chain():
    """モックRAGChain"""
    with patch("backend.api.v1.rag.RAGChain") as mock:
        instance = Mock()
        instance.query.return_value = {
            "answer": "This is a test answer about LangGraph.",
            "sources": [
                {
                    "title": "LangGraph Documentation",
                    "url": "https://langchain-ai.github.io/langgraph/",
                    "excerpt": "LangGraph is a framework for building stateful agents.",
                    "relevance": 0.95,
                    "doc_type": "official_docs",
                }
            ],
            "code_examples": [
                {
                    "language": "python",
                    "code": "from langgraph.graph import StateGraph\n\ngraph = StateGraph()",
                    "description": "Basic StateGraph initialization",
                    "source_url": "https://github.com/langchain-ai/langgraph",
                }
            ],
            "confidence": 0.92,
            "metadata": {
                "model": "gpt-4-turbo-preview",
                "tokens_used": 1500,
            },
        }
        mock.return_value = instance
        yield instance


@pytest.fixture
def mock_architect_graph():
    """モックArchitectGraph"""
    with patch("backend.api.v1.architect.ArchitectGraph") as mock:
        instance = Mock()
        instance.generate_architecture.return_value = {
            "challenge_analysis": {
                "summary": "カスタマーサポートの自動化プロジェクト",
                "key_requirements": [
                    "FAQ自動回答",
                    "人間へのエスカレーション",
                    "Zendesk連携",
                ],
                "suggested_approach": "LangGraphの条件分岐フローを活用",
                "langgraph_fit_reason": "状態管理と条件分岐が適している",
            },
            "architecture": {
                "mermaid_diagram": "graph TD\n    A[問い合わせ受付] --> B{FAQ検索}\n    B -->|一致| C[自動回答]",
                "node_descriptions": [
                    {
                        "node_id": "A",
                        "name": "問い合わせ受付",
                        "purpose": "ユーザーからの問い合わせを受け付ける",
                        "description": "問い合わせテキストを受け取り、前処理を行う",
                        "inputs": ["user_query"],
                        "outputs": ["query_text", "user_id"],
                    }
                ],
                "edge_descriptions": [
                    {
                        "from_node": "A",
                        "to_node": "B",
                        "condition": None,
                        "description": "受付した問い合わせをFAQ検索に渡す",
                    }
                ],
                "state_schema": {
                    "query": "str",
                    "faq_match": "bool",
                    "response": "str",
                },
            },
            "code_example": {
                "language": "python",
                "code": "from langgraph.graph import StateGraph\nfrom typing import TypedDict\n\nclass SupportState(TypedDict):\n    query: str\n    response: str\n\ngraph = StateGraph(SupportState)",
                "explanation": "基本的なカスタマーサポートワークフローの実装例",
            },
            "business_explanation": "このシステムは、FAQで即座に回答できる質問を自動処理し、複雑な質問は人間にエスカレーションします。",
            "implementation_notes": [
                "FAQ検索にはベクトルDBを使用することを推奨",
                "Zendesk APIの認証情報が必要",
            ],
            "metadata": {
                "model": "gpt-4-turbo-preview",
                "tokens_used": 3500,
            },
        }
        mock.return_value = instance
        yield instance


@pytest.fixture
def auth_token(test_settings):
    """テスト用認証トークン"""
    from backend.core.security import create_access_token

    token_data = {"sub": "admin", "role": "admin"}
    return create_access_token(token_data, settings=test_settings)


@pytest.fixture
def authenticated_client(client, test_settings):
    """認証済みテストクライアント - 認証をバイパス"""
    from backend.core.users import User

    # テスト用のモックユーザー
    test_user = User(
        username="testuser",
        password_hash="",  # テストではパスワードハッシュは不要
        role="admin",
        daily_limit=None,  # 無制限
    )

    # 認証依存性をバイパス
    def override_get_current_user():
        return test_user

    # 使用制限依存性もバイパス（Userオブジェクトを返す）
    def override_require_usage_limit():
        return test_user

    from backend.core.dependencies import get_current_user, require_usage_limit
    from backend.main import app

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[require_usage_limit] = override_require_usage_limit

    yield client

    # クリーンアップ
    app.dependency_overrides.clear()


@pytest.fixture
def mock_usage_limiter():
    """モック使用制限"""
    with (
        patch("backend.core.dependencies.check_usage_limit") as mock_check,
        patch("backend.core.dependencies.increment_usage") as mock_increment,
    ):
        mock_check.return_value = True  # 制限チェックは常に成功
        yield {"check": mock_check, "increment": mock_increment}
