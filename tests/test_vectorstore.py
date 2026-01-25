"""
LangGraph Catalyst - Vector Store Tests

ベクトルストアのユニットテスト
"""

import pytest
from unittest.mock import Mock

from langchain_core.documents import Document

from src.features.rag.vectorstore import ChromaVectorStore
from src.utils.exceptions import VectorStoreError


@pytest.mark.unit
class TestChromaVectorStore:
    """ChromaVectorStoreのテスト"""

    # ========================================================================
    # Initialization Tests
    # ========================================================================

    def test_vectorstore_initialization(self, mocker, mock_openai_embeddings, test_chroma_dir):
        """ベクトルストアの初期化テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma = mocker.patch("src.features.rag.vectorstore.Chroma")

        # Act
        vectorstore = ChromaVectorStore(
            collection_name="test_collection", persist_directory=str(test_chroma_dir)
        )

        # Assert
        assert vectorstore is not None
        assert vectorstore.collection_name == "test_collection"
        assert vectorstore.persist_directory == str(test_chroma_dir)

    def test_vectorstore_initialization_with_defaults(self, mocker, mock_openai_embeddings):
        """デフォルト値での初期化テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma = mocker.patch("src.features.rag.vectorstore.Chroma")

        # Act
        vectorstore = ChromaVectorStore()

        # Assert
        assert vectorstore.collection_name == "langgraph_docs"
        assert vectorstore.persist_directory is not None

    def test_vectorstore_initialization_failure(self, mocker):
        """初期化失敗のテスト"""
        # Arrange
        mocker.patch(
            "src.features.rag.vectorstore.OpenAIEmbeddings", side_effect=Exception("API Error")
        )

        # Act & Assert
        with pytest.raises(VectorStoreError, match="Failed to initialize vector store"):
            ChromaVectorStore()

    # ========================================================================
    # Add Documents Tests
    # ========================================================================

    def test_add_documents_success(
        self, mocker, mock_openai_embeddings, mock_chroma, sample_documents
    ):
        """ドキュメント追加の成功テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma(sample_documents)

        vectorstore = ChromaVectorStore()

        # Act
        result = vectorstore.add_documents(sample_documents)

        # Assert
        assert result["status"] == "success"
        assert result["added_count"] == len(sample_documents)
        assert result["failed_count"] == 0
        assert result["total_documents_in_store"] >= 0

    def test_add_documents_empty_list(self, mocker, mock_openai_embeddings, mock_chroma):
        """空のドキュメントリストのテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma([])

        vectorstore = ChromaVectorStore()

        # Act
        result = vectorstore.add_documents([])

        # Assert
        assert result["status"] == "success"
        assert result["added_count"] == 0
        assert result["failed_count"] == 0

    def test_add_documents_batch_processing(
        self, mocker, mock_openai_embeddings, mock_chroma, sample_documents
    ):
        """バッチ処理のテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma(sample_documents)

        vectorstore = ChromaVectorStore()

        # 大量のドキュメントを生成
        large_doc_list = sample_documents * 50  # 150件

        # Act
        result = vectorstore.add_documents(large_doc_list, batch_size=50)

        # Assert
        assert result["status"] == "success"
        assert result["added_count"] == len(large_doc_list)
        # バッチ処理が複数回呼ばれることを確認
        assert vectorstore.vector_store.add_documents.call_count == 3

    def test_add_documents_partial_failure(
        self, mocker, mock_openai_embeddings, sample_documents
    ):
        """部分的な失敗のテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma = mocker.patch("src.features.rag.vectorstore.Chroma")
        mock_instance = mock_chroma.return_value

        # 1回目は成功、2回目は失敗
        mock_instance.add_documents.side_effect = [
            None,
            Exception("Batch error"),
        ]

        # モックコレクション
        mock_collection = Mock()
        mock_collection.count.return_value = len(sample_documents)
        mock_instance._collection = mock_collection

        vectorstore = ChromaVectorStore()

        # 6件のドキュメント（3件ずつ2バッチ）
        docs = sample_documents * 2

        # Act
        result = vectorstore.add_documents(docs, batch_size=3)

        # Assert
        assert result["status"] == "partial"
        assert result["added_count"] == 3
        assert result["failed_count"] == 3

    # ========================================================================
    # Similarity Search Tests
    # ========================================================================

    def test_similarity_search_success(
        self, mocker, mock_openai_embeddings, mock_chroma, sample_documents
    ):
        """類似度検索の成功テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma(sample_documents)

        vectorstore = ChromaVectorStore()

        # Act
        results = vectorstore.similarity_search("What is LangGraph?", k=5)

        # Assert
        assert len(results) > 0
        assert all(isinstance(doc, Document) for doc in results)
        vectorstore.vector_store.similarity_search.assert_called_once_with(
            query="What is LangGraph?", k=5
        )

    def test_similarity_search_with_filter(
        self, mocker, mock_openai_embeddings, mock_chroma, sample_documents
    ):
        """フィルタ付き検索のテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma(sample_documents)

        vectorstore = ChromaVectorStore()

        # Act
        results = vectorstore.similarity_search(
            "LangGraph", k=3, filter_metadata={"doc_type": "official_docs"}
        )

        # Assert
        vectorstore.vector_store.similarity_search.assert_called_once_with(
            query="LangGraph", k=3, filter={"doc_type": "official_docs"}
        )

    def test_similarity_search_empty_query(self, mocker, mock_openai_embeddings, mock_chroma):
        """空クエリのテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma([])

        vectorstore = ChromaVectorStore()

        # Act
        results = vectorstore.similarity_search("", k=5)

        # Assert
        assert results == []

    def test_similarity_search_with_score(
        self, mocker, mock_openai_embeddings, mock_chroma, sample_documents
    ):
        """スコア付き検索のテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma(sample_documents)

        vectorstore = ChromaVectorStore()

        # Act
        results = vectorstore.similarity_search_with_score("LangGraph", k=3)

        # Assert
        assert len(results) > 0
        # 各結果は(Document, float)のタプル
        for doc, score in results:
            assert isinstance(doc, Document)
            assert isinstance(score, float)

    def test_similarity_search_error(self, mocker, mock_openai_embeddings):
        """検索エラーのテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma = mocker.patch("src.features.rag.vectorstore.Chroma")
        mock_chroma.return_value.similarity_search.side_effect = Exception("Search error")

        vectorstore = ChromaVectorStore()

        # Act & Assert
        with pytest.raises(VectorStoreError, match="Failed to perform similarity search"):
            vectorstore.similarity_search("test query")

    # ========================================================================
    # Collection Management Tests
    # ========================================================================

    def test_delete_collection_success(self, mocker, mock_openai_embeddings, mock_chroma):
        """コレクション削除の成功テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma([])

        vectorstore = ChromaVectorStore()

        # Act
        result = vectorstore.delete_collection()

        # Assert
        assert result is True
        vectorstore.vector_store.delete_collection.assert_called_once()

    def test_delete_collection_error(self, mocker, mock_openai_embeddings):
        """コレクション削除のエラーテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma = mocker.patch("src.features.rag.vectorstore.Chroma")
        mock_chroma.return_value.delete_collection.side_effect = Exception("Delete error")

        vectorstore = ChromaVectorStore()

        # Act & Assert
        with pytest.raises(VectorStoreError, match="Failed to delete collection"):
            vectorstore.delete_collection()

    def test_get_collection_count(
        self, mocker, mock_openai_embeddings, mock_chroma, sample_documents
    ):
        """コレクション内のドキュメント数取得テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma(sample_documents)

        vectorstore = ChromaVectorStore()

        # Act
        count = vectorstore.get_collection_count()

        # Assert
        assert count == len(sample_documents)

    def test_get_collection_count_error(self, mocker, mock_openai_embeddings):
        """ドキュメント数取得のエラーテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma = mocker.patch("src.features.rag.vectorstore.Chroma")
        mock_collection = Mock()
        mock_collection.count.side_effect = Exception("Count error")
        mock_chroma.return_value._collection = mock_collection

        vectorstore = ChromaVectorStore()

        # Act
        count = vectorstore.get_collection_count()

        # Assert
        assert count == 0  # エラー時は0を返す

    # ========================================================================
    # Retriever Tests
    # ========================================================================

    def test_as_retriever(self, mocker, mock_openai_embeddings, mock_chroma):
        """Retrieverとして取得するテスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma([])

        vectorstore = ChromaVectorStore()

        # Act
        retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

        # Assert
        vectorstore.vector_store.as_retriever.assert_called_once_with(search_kwargs={"k": 10})

    def test_as_retriever_default_kwargs(self, mocker, mock_openai_embeddings, mock_chroma):
        """デフォルトパラメータでのRetriever取得テスト"""
        # Arrange
        mock_openai_embeddings()
        mock_chroma_instance = mock_chroma([])

        vectorstore = ChromaVectorStore()

        # Act
        retriever = vectorstore.as_retriever()

        # Assert
        # デフォルト値で呼ばれることを確認
        vectorstore.vector_store.as_retriever.assert_called_once()
