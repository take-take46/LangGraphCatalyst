"""
LangGraph Catalyst - RAG Chain Tests

RAGチェーンのユニットテスト
"""


import pytest

from src.features.rag.chain import RAGChain
from src.features.rag.vectorstore import ChromaVectorStore
from src.utils.exceptions import LLMError, ValidationError


@pytest.mark.unit
class TestRAGChain:
    """RAGチェーンのテスト"""

    # ========================================================================
    # Initialization Tests
    # ========================================================================

    def test_rag_chain_initialization(self, mocker, mock_openai_chat, test_chroma_dir):
        """RAGチェーンの初期化テスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)

        # Act
        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Assert
        assert rag_chain is not None
        assert rag_chain.vectorstore == mock_vectorstore
        assert rag_chain.llm_model is not None
        assert rag_chain.temperature is not None

    def test_rag_chain_initialization_with_custom_params(
        self, mocker, mock_openai_chat, test_chroma_dir
    ):
        """カスタムパラメータでの初期化テスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        custom_model = "gpt-4"
        custom_temp = 0.5

        # Act
        rag_chain = RAGChain(
            vectorstore=mock_vectorstore, llm_model=custom_model, temperature=custom_temp
        )

        # Assert
        assert rag_chain.llm_model == custom_model
        assert rag_chain.temperature == custom_temp

    def test_rag_chain_initialization_failure(self, mocker, test_chroma_dir):
        """LLM初期化失敗のテスト"""
        # Arrange
        mocker.patch("src.features.rag.chain.ChatOpenAI", side_effect=Exception("API Error"))
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)

        # Act & Assert
        with pytest.raises(ValidationError, match="Failed to initialize LLM"):
            RAGChain(vectorstore=mock_vectorstore)

    # ========================================================================
    # Query Tests
    # ========================================================================

    def test_query_success(self, mocker, mock_openai_chat, sample_documents):
        """正常なクエリ実行のテスト"""
        # Arrange
        mock_openai_chat(
            response_content="LangGraph is a framework for building stateful agents.", tokens=150
        )

        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = sample_documents

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act
        response = rag_chain.query("What is LangGraph?")

        # Assert
        assert "answer" in response
        assert response["answer"] != ""
        assert "sources" in response
        assert "metadata" in response
        assert response["metadata"]["model"] is not None
        mock_vectorstore.similarity_search.assert_called_once()

    def test_query_with_sources(self, mocker, mock_openai_chat, sample_documents):
        """ソース付き回答のテスト"""
        # Arrange
        mock_openai_chat(response_content="LangGraph is...", tokens=100)

        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = sample_documents

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act
        response = rag_chain.query("What is LangGraph?", include_sources=True)

        # Assert
        assert "sources" in response
        assert len(response["sources"]) > 0
        # ソースにはtitleとurlが含まれる
        for source in response["sources"]:
            assert "title" in source
            assert "url" in source

    def test_query_with_code_examples_auto_detection(
        self, mocker, mock_openai_chat, sample_documents
    ):
        """コード例の自動検出テスト"""
        # Arrange
        code_response = """
LangGraphでは、StateGraphを使用してグラフを作成します。

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
```
        """.strip()

        mock_openai_chat(response_content=code_response, tokens=200)

        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = sample_documents

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act - コードを含む質問
        response = rag_chain.query("LangGraphのコード例を教えて")

        # Assert
        assert "code_examples" in response
        # コード例が自動的に含まれることを確認

    def test_query_without_code_examples(self, mocker, mock_openai_chat, sample_documents):
        """コード例なしのテスト"""
        # Arrange
        mock_openai_chat(response_content="LangGraph is a framework...", tokens=100)

        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = sample_documents

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act - コードを要求しない質問
        response = rag_chain.query("What is LangGraph?", include_code_examples=False)

        # Assert
        assert "code_examples" in response
        assert response["code_examples"] == []

    def test_query_empty_question(self, mocker, mock_openai_chat):
        """空の質問のテスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act & Assert
        with pytest.raises(ValidationError, match="Question cannot be empty"):
            rag_chain.query("")

    def test_query_no_documents_found(self, mocker, mock_openai_chat):
        """ドキュメントが見つからない場合のテスト"""
        # Arrange
        mock_openai_chat()

        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = []

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act
        response = rag_chain.query("What is LangGraph?")

        # Assert
        assert "answer" in response
        assert "関連する情報が見つかりませんでした" in response["answer"]
        assert response["confidence"] == 0.0
        assert len(response["sources"]) == 0

    def test_query_llm_error(self, mocker, sample_documents):
        """LLMエラーのテスト"""
        # Arrange
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = sample_documents

        mock_llm = mocker.patch("src.features.rag.chain.ChatOpenAI")
        mock_llm.return_value.invoke.side_effect = Exception("API Error")

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act & Assert
        with pytest.raises(LLMError, match="Failed to process RAG query"):
            rag_chain.query("What is LangGraph?")

    # ========================================================================
    # Helper Method Tests
    # ========================================================================

    def test_should_include_code_japanese(self, mocker, mock_openai_chat):
        """日本語のコード要求キーワード検出テスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act & Assert
        assert rag_chain._should_include_code("コード例を教えて") is True
        assert rag_chain._should_include_code("実装方法を教えて") is True
        assert rag_chain._should_include_code("書き方を教えて") is True
        assert rag_chain._should_include_code("LangGraphとは何ですか") is False

    def test_should_include_code_english(self, mocker, mock_openai_chat):
        """英語のコード要求キーワード検出テスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act & Assert
        assert rag_chain._should_include_code("show me code example") is True
        assert rag_chain._should_include_code("how to implement") is True
        assert rag_chain._should_include_code("write code") is True
        assert rag_chain._should_include_code("what is LangGraph") is False

    def test_build_context(self, mocker, mock_openai_chat, sample_documents):
        """コンテキスト構築のテスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act
        context = rag_chain._build_context(sample_documents)

        # Assert
        assert context != ""
        assert "Introduction to LangGraph" in context
        assert "StateGraph Documentation" in context
        # URLが含まれることを確認
        assert "https://langchain-ai.github.io/langgraph/" in context

    def test_calculate_confidence(self, mocker, mock_openai_chat, sample_documents):
        """信頼度計算のテスト"""
        # Arrange
        mock_openai_chat()
        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act & Assert
        # 5件以上のドキュメント
        assert rag_chain._calculate_confidence(sample_documents + sample_documents) == 0.9

        # 3-4件のドキュメント
        assert rag_chain._calculate_confidence(sample_documents) == 0.7

        # 1-2件のドキュメント
        assert rag_chain._calculate_confidence(sample_documents[:1]) == 0.5

        # 0件のドキュメント
        assert rag_chain._calculate_confidence([]) == 0.0

    # ========================================================================
    # Integration-like Tests
    # ========================================================================

    @pytest.mark.slow
    def test_query_with_real_like_flow(self, mocker, mock_openai_chat, sample_documents):
        """実際のフローに近いテスト"""
        # Arrange
        realistic_response = """
LangGraphは、LLMを使用した状態を持つマルチアクターアプリケーションを構築するためのライブラリです。

主な特徴：
1. **状態管理**: StateGraphを使用して明示的な状態管理
2. **循環フロー**: 複数のステップを循環的に実行可能
3. **条件分岐**: 状態に基づいて実行フローを制御

以下は基本的な使用例です：

```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

class State(TypedDict):
    messages: list[str]
    count: int

graph = StateGraph(State)
```

このように、LangGraphを使用することで、複雑な対話フローを構築できます。
        """.strip()

        mock_openai_chat(response_content=realistic_response, tokens=300)

        mock_vectorstore = mocker.Mock(spec=ChromaVectorStore)
        mock_vectorstore.similarity_search.return_value = sample_documents

        rag_chain = RAGChain(vectorstore=mock_vectorstore)

        # Act
        response = rag_chain.query("LangGraphのコード例を教えて", k=3, include_sources=True)

        # Assert
        assert response["answer"] != ""
        assert len(response["sources"]) > 0
        assert len(response["code_examples"]) > 0
        assert response["confidence"] > 0.5
        assert response["metadata"]["tokens_used"] > 0
        assert response["metadata"]["response_time"] >= 0
