"""
LangGraph Catalyst - Crawler Tests

ドキュメントクローラーのユニットテスト
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from langchain_core.documents import Document

from src.features.rag.crawler import (
    crawl_langgraph_docs,
    crawl_langchain_blog,
    crawl_github_repo,
    update_all_sources,
)


@pytest.mark.unit
class TestCrawler:
    """ドキュメントクローラーのテスト"""

    @patch("src.features.rag.crawler.WebBaseLoader")
    def test_crawl_langgraph_docs_success(self, mock_loader_class):
        """
        正常なドキュメントクロールのテスト

        テスト内容:
        - WebBaseLoaderが正しく使用されること
        - Documentオブジェクトのリストが返されること
        - 各Documentに必要なメタデータが含まれること
        """
        # Arrange
        mock_doc = Document(
            page_content="LangGraph is a framework for building stateful agents.",
            metadata={}
        )
        mock_loader = MagicMock()
        mock_loader.load.return_value = [mock_doc]
        mock_loader_class.return_value = mock_loader

        # Act
        docs = crawl_langgraph_docs(max_pages=1)

        # Assert
        assert len(docs) > 0, "少なくとも1つのドキュメントが返されるべき"
        assert all(isinstance(doc, Document) for doc in docs), "全てDocumentオブジェクトであるべき"

        # メタデータの検証
        for doc in docs:
            assert "source" in doc.metadata, "sourceメタデータが必要"
            assert "title" in doc.metadata, "titleメタデータが必要"
            assert "doc_type" in doc.metadata, "doc_typeメタデータが必要"
            assert doc.metadata["doc_type"] == "official_docs"
            assert doc.page_content != "", "ページコンテンツは空でないべき"

    @patch("src.features.rag.crawler.WebBaseLoader")
    def test_crawl_langchain_blog_success(self, mock_loader_class):
        """
        ブログクロール正常実行テスト
        """
        # Arrange
        mock_doc = Document(
            page_content="Blog post about LangGraph",
            metadata={}
        )
        mock_loader = MagicMock()
        mock_loader.load.return_value = [mock_doc]
        mock_loader_class.return_value = mock_loader

        # Act
        docs = crawl_langchain_blog(max_articles=1)

        # Assert
        assert len(docs) > 0
        for doc in docs:
            assert "doc_type" in doc.metadata
            assert doc.metadata["doc_type"] == "blog"

    @patch("src.features.rag.crawler.WebBaseLoader")
    def test_crawl_github_repo_success(self, mock_loader_class):
        """
        GitHubリポジトリクロール正常実行テスト
        """
        # Arrange
        mock_doc = Document(
            page_content="GitHub README content",
            metadata={}
        )
        mock_loader = MagicMock()
        mock_loader.load.return_value = [mock_doc]
        mock_loader_class.return_value = mock_loader

        # Act
        docs = crawl_github_repo(include_examples=False)

        # Assert
        assert len(docs) > 0
        for doc in docs:
            assert "doc_type" in doc.metadata
            assert "github" in doc.metadata["doc_type"]

    @patch("src.features.rag.crawler.crawl_github_repo")
    @patch("src.features.rag.crawler.crawl_langchain_blog")
    @patch("src.features.rag.crawler.crawl_langgraph_docs")
    @patch("src.features.rag.crawler.crawl_langchain_docs")
    def test_update_all_sources_success(
        self,
        mock_crawl_langchain_docs,
        mock_crawl_langgraph,
        mock_crawl_blog,
        mock_crawl_github,
    ):
        """
        全ソース更新成功テスト
        """
        # Arrange
        mock_doc = Document(page_content="Test", metadata={})
        mock_crawl_langgraph.return_value = [mock_doc] * 10
        mock_crawl_langchain_docs.return_value = [mock_doc] * 5
        mock_crawl_blog.return_value = [mock_doc] * 5
        mock_crawl_github.return_value = [mock_doc] * 5

        # Act
        result = update_all_sources()

        # Assert
        assert result["status"] == "success"
        assert result["total_documents"] == 25
        assert "langgraph_docs" in result["sources"]
        assert "blog" in result["sources"]
        assert "updated_at" in result
        assert isinstance(result["errors"], list)

    @patch("src.features.rag.crawler.crawl_github_repo")
    @patch("src.features.rag.crawler.crawl_langchain_blog")
    @patch("src.features.rag.crawler.crawl_langgraph_docs")
    @patch("src.features.rag.crawler.crawl_langchain_docs")
    def test_update_all_sources_partial_failure(
        self,
        mock_crawl_langchain_docs,
        mock_crawl_langgraph,
        mock_crawl_blog,
        mock_crawl_github,
    ):
        """
        部分的な失敗を含む更新テスト
        """
        # Arrange
        mock_doc = Document(page_content="Test", metadata={})
        mock_crawl_langgraph.return_value = [mock_doc] * 10
        mock_crawl_langchain_docs.side_effect = Exception("Network error")
        mock_crawl_blog.return_value = [mock_doc] * 5
        mock_crawl_github.return_value = [mock_doc] * 5

        # Act
        result = update_all_sources()

        # Assert
        assert result["status"] == "partial"
        assert result["total_documents"] == 20
        assert len(result["errors"]) > 0
        assert any("langchain" in error.lower() for error in result["errors"])
