"""
LangGraph Catalyst - Test Configuration

pytestの共通設定とフィクスチャを定義します。
"""

import os
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
from langchain_core.documents import Document

# テスト実行時に必要な環境変数を設定（import時のエラーを防ぐ）
os.environ.setdefault("OPENAI_API_KEY", "sk-test-mock-key-for-testing")
os.environ.setdefault("CHROMA_PERSIST_DIR", "./tests/data/chroma_test")
os.environ.setdefault("LOG_LEVEL", "DEBUG")
os.environ.setdefault("ENVIRONMENT", "test")


# ============================================================================
# Test Configuration
# ============================================================================


@pytest.fixture(scope="session")
def test_config() -> dict[str, Any]:
    """テスト用設定"""
    return {
        "openai_api_key": "sk-test-mock-key-for-testing",
        "chroma_persist_dir": "./tests/data/chroma_test",
        "default_llm_model": "gpt-4-turbo-preview",
        "default_embedding_model": "text-embedding-3-small",
        "temperature": 0.3,
        "log_level": "DEBUG",
    }


@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory) -> Path:
    """テストデータディレクトリ"""
    data_dir = tmp_path_factory.mktemp("test_data")
    return data_dir


@pytest.fixture(scope="session")
def test_chroma_dir(tmp_path_factory) -> Path:
    """テスト用Chromaディレクトリ"""
    chroma_dir = tmp_path_factory.mktemp("chroma_test")
    return chroma_dir


# ============================================================================
# Environment Variable Mocking
# ============================================================================


@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    環境変数のモック

    注意: このフィクスチャは自動適用されません。
    環境変数を使用するテストで明示的に使用してください。
    設定クラスのバリデーションをテストする場合は使用しないでください。
    """
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-mock-key-for-testing")
    monkeypatch.setenv("CHROMA_PERSIST_DIR", "./tests/data/chroma_test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("ENVIRONMENT", "test")


@pytest.fixture(autouse=True)
def block_openai_api_calls(mocker):
    """
    すべてのテストで実際のOpenAI API呼び出しをブロック

    このフィクスチャは自動的に適用され、実際のAPI呼び出しを防ぎます。
    個別のテストでモックが必要な場合は、明示的にモックフィクスチャを使用してください。
    """
    # OpenAI APIへの実際の呼び出しをブロック
    mock_openai = mocker.patch("openai.OpenAI")
    mock_openai.return_value.chat.completions.create.side_effect = RuntimeError(
        "Attempted to call real OpenAI API in tests! Use mock fixtures instead."
    )

    # Note: httpxはモックしない（OpenAIのisinstanceチェックが壊れるため）
    # 代わりに、auto_mock_langchain_openaiで上位レベルでモックする


@pytest.fixture(autouse=True)
def auto_mock_langchain_openai(mocker):
    """
    すべてのテストでLangChainのOpenAI統合を自動的にモック

    これにより、テストで明示的にモックを呼ばなくても、
    実際のAPI呼び出しは発生しません。
    """
    # ChatOpenAIのモック（すべてのインポートパスで）
    for path in [
        "langchain_openai.ChatOpenAI",
        "langchain_openai.chat_models.ChatOpenAI",
        "langchain_openai.chat_models.base.ChatOpenAI",
    ]:
        try:
            mock_chat = mocker.patch(path)
            mock_instance = Mock()
            mock_instance.invoke.return_value = Mock(
                content="Mocked response", response_metadata={"token_usage": {"total_tokens": 100}}
            )
            mock_chat.return_value = mock_instance
        except Exception:
            # パスが存在しない場合はスキップ
            pass

    # OpenAIEmbeddingsのモック
    for path in [
        "langchain_openai.OpenAIEmbeddings",
        "langchain_openai.embeddings.OpenAIEmbeddings",
        "langchain_openai.embeddings.base.OpenAIEmbeddings",
    ]:
        try:
            mock_embeddings = mocker.patch(path)
            mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 1536] * 3
            mock_embeddings.return_value.embed_query.return_value = [0.1] * 1536
        except Exception:
            pass

    # Chromaのモック
    for path in ["langchain_chroma.Chroma", "chromadb.Client"]:
        try:
            mock_chroma = mocker.patch(path)
            mock_instance = Mock()
            mock_instance.similarity_search.return_value = []
            mock_instance.similarity_search_with_score.return_value = []
            mock_instance.add_documents.return_value = None
            mock_instance.delete_collection.return_value = None
            mock_collection = Mock()
            mock_collection.count.return_value = 0
            mock_instance._collection = mock_collection
            mock_instance.as_retriever.return_value = Mock()
            mock_chroma.return_value = mock_instance
        except Exception:
            pass


# ============================================================================
# Sample Test Data
# ============================================================================


@pytest.fixture
def sample_documents() -> list[Document]:
    """サンプルドキュメント"""
    return [
        Document(
            page_content="""
LangGraph is a library for building stateful, multi-actor applications with LLMs.
It extends the LangChain Expression Language with the ability to coordinate
multiple chains (or actors) across multiple steps of computation in a cyclic manner.
            """.strip(),
            metadata={
                "source": "https://langchain-ai.github.io/langgraph/",
                "title": "Introduction to LangGraph",
                "doc_type": "official_docs",
                "updated_at": "2026-01-15T00:00:00Z",
            },
        ),
        Document(
            page_content="""
StateGraph is the main graph class in LangGraph. It is parameterized by a state object.
The state can be any Python type, but typically you'll use a TypedDict or Pydantic model.

Example:
```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class State(TypedDict):
    messages: list[str]

graph = StateGraph(State)
```
            """.strip(),
            metadata={
                "source": "https://langchain-ai.github.io/langgraph/concepts/state_graph/",
                "title": "StateGraph Documentation",
                "doc_type": "official_docs",
                "updated_at": "2026-01-15T00:00:00Z",
            },
        ),
        Document(
            page_content="""
Conditional edges allow you to route execution based on the state of your graph.
They are created using the `add_conditional_edges()` method.

Example:
```python
def route_message(state):
    if state['needs_human']:
        return 'human'
    return 'agent'

graph.add_conditional_edges(
    'analyze',
    route_message,
    {'human': 'escalate', 'agent': 'respond'}
)
```
            """.strip(),
            metadata={
                "source": "https://langchain-ai.github.io/langgraph/concepts/conditional_edges/",
                "title": "Conditional Edges",
                "doc_type": "official_docs",
                "updated_at": "2026-01-16T00:00:00Z",
            },
        ),
    ]


@pytest.fixture
def sample_business_challenge() -> str:
    """サンプルビジネス課題"""
    return "カスタマーサポートの自動化を実現したい。FAQへの自動回答と、複雑な問い合わせは人間にエスカレーションする仕組みが必要。"


@pytest.fixture
def sample_industry() -> str:
    """サンプル業界"""
    return "EC"


@pytest.fixture
def sample_constraints() -> list[str]:
    """サンプル制約条件"""
    return ["日本語対応必須", "既存のZendeskと連携"]


# ============================================================================
# LLM Mocking
# ============================================================================


@pytest.fixture
def mock_llm_response():
    """モックLLMレスポンス"""

    def _create_response(content: str, tokens: int = 100):
        """LLMレスポンスを作成"""
        mock = Mock()
        mock.content = content
        mock.response_metadata = {"token_usage": {"total_tokens": tokens}}
        return mock

    return _create_response


@pytest.fixture
def mock_openai_chat(mocker, mock_llm_response):
    """OpenAI Chatモデルのモック"""

    def _mock_chat(response_content: str = "This is a mocked response", tokens: int = 100):
        """ChatOpenAIをモック化"""
        mock_response = mock_llm_response(response_content, tokens)

        # 複数のインポートパスでパッチを適用
        mocks = []
        for path in [
            "langchain_openai.ChatOpenAI",
            "src.features.rag.chain.ChatOpenAI",
            "src.features.architect.graph.ChatOpenAI",
        ]:
            mock_llm = mocker.patch(path)
            mock_llm.return_value.invoke.return_value = mock_response
            mocks.append(mock_llm)

        # 最初のモックを返す（全てが同じ ChatOpenAI クラスをパッチしているため）
        return mocks[0]

    return _mock_chat


@pytest.fixture
def mock_openai_embeddings(mocker):
    """OpenAI Embeddingsのモック"""
    # 複数のインポートパスでパッチを適用
    for path in [
        "langchain_openai.OpenAIEmbeddings",
        "src.features.rag.vectorstore.OpenAIEmbeddings",
    ]:
        mock_embeddings = mocker.patch(path)
        # 1536次元のダミー埋め込みベクトル
        mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 1536] * 3
        mock_embeddings.return_value.embed_query.return_value = [0.1] * 1536

    return mock_embeddings


# ============================================================================
# Vector Store Mocking
# ============================================================================


@pytest.fixture
def mock_chroma(mocker):
    """Chromaベクトルストアのモック"""

    def _create_mock(documents: list[Document] | None = None):
        """Chromaモックを作成"""
        # 複数のインポートパスでパッチを適用
        for path in [
            "langchain_chroma.Chroma",
            "src.features.rag.vectorstore.Chroma",
        ]:
            mock = mocker.patch(path)
            mock_instance = mock.return_value

            # similarity_searchのモック
            if documents:
                mock_instance.similarity_search.return_value = documents
                mock_instance.similarity_search_with_score.return_value = [
                    (doc, 0.9 - i * 0.1) for i, doc in enumerate(documents)
                ]
            else:
                mock_instance.similarity_search.return_value = []
                mock_instance.similarity_search_with_score.return_value = []

            # add_documentsのモック
            mock_instance.add_documents.return_value = None

            # delete_collectionのモック
            mock_instance.delete_collection.return_value = None

            # _collectionのモック
            mock_collection = Mock()
            mock_collection.count.return_value = len(documents) if documents else 0
            mock_instance._collection = mock_collection

            # as_retrieverのモック
            mock_instance.as_retriever.return_value = Mock()

        return mock

    return _create_mock


# ============================================================================
# Cleanup
# ============================================================================


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """テスト後のクリーンアップ"""
    yield
    # テスト後のクリーンアップ処理
    # 必要に応じてテストデータを削除
    test_dirs = [
        "./tests/data/chroma_test",
        "./tests/logs",
    ]

    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            # 実際の削除は慎重に行う
            pass
