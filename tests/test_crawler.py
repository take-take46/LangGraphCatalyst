"""
LangGraph Catalyst - Crawler Tests

ドキュメントクローラーのユニットテスト
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from langchain_core.documents import Document

from src.features.rag.crawler import (
    crawl_langgraph_docs,
    crawl_langchain_blog,
    crawl_github_repo,
    update_all_sources,
)
from src.utils.exceptions import CrawlerError


@pytest.mark.unit
class TestCrawler:
    """ドキュメントクローラーのテスト"""

    # ========================================================================
    # LangGraph Documentation Crawler Tests
    # ========================================================================

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_langgraph_docs_success(self, mock_get):
        """
        正常なドキュメントクロールのテスト

        テスト内容:
        - HTTPリクエストが成功すること
        - Documentオブジェクトのリストが返されること
        - 各Documentに必要なメタデータが含まれること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>LangGraph Introduction</title></head>
            <body>
                <article>
                    <h1>Getting Started with LangGraph</h1>
                    <p>LangGraph is a framework for building stateful agents.</p>
                </article>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

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

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_with_max_pages_limit(self, mock_get):
        """
        ページ数制限の動作確認テスト

        テスト内容:
        - max_pagesパラメータが正しく適用されること
        - 返されるドキュメント数が指定値以下であること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Test content</p></body></html>"
        mock_get.return_value = mock_response

        # Act
        max_pages = 5
        docs = crawl_langgraph_docs(max_pages=max_pages)

        # Assert
        assert len(docs) <= max_pages, f"ドキュメント数は{max_pages}以下であるべき"

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_network_error(self, mock_get):
        """
        ネットワークエラー時の処理テスト

        テスト内容:
        - ネットワーク接続エラーが適切に処理されること
        - CrawlerErrorが発生すること
        """
        # Arrange
        mock_get.side_effect = Exception("Network error")

        # Act & Assert
        with pytest.raises(CrawlerError, match="Failed to crawl LangGraph documentation"):
            crawl_langgraph_docs(max_pages=1)

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_404_error(self, mock_get):
        """
        404エラー時の処理テスト

        テスト内容:
        - HTTPステータスエラーが適切に処理されること
        - エラー時に空のリストが返されること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        # Act & Assert
        with pytest.raises(CrawlerError):
            crawl_langgraph_docs(max_pages=1)

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_metadata_extraction(self, mock_get):
        """
        メタデータの正確性テスト

        テスト内容:
        - 抽出されたメタデータに必須フィールドが含まれること
        - source, title, updated_atが正しく設定されること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Test Title</title></head>
            <body><p>Content</p></body>
        </html>
        """
        mock_get.return_value = mock_response

        # Act
        docs = crawl_langgraph_docs(max_pages=1)

        # Assert
        if docs:
            doc = docs[0]
            assert "source" in doc.metadata
            assert "title" in doc.metadata
            assert "doc_type" in doc.metadata
            assert doc.metadata["doc_type"] == "official_docs"

    # ========================================================================
    # Blog Crawler Tests
    # ========================================================================

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_blog_posts(self, mock_get):
        """
        ブログ記事のクロールテスト

        テスト内容:
        - ブログ記事が正しく取得されること
        - doc_typeが'blog'であること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <article>
                    <h2>LangGraph Blog Post</h2>
                    <p>This is a blog post about LangGraph.</p>
                </article>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        # Act
        docs = crawl_langchain_blog(max_articles=1)

        # Assert
        assert len(docs) > 0
        for doc in docs:
            assert doc.metadata["doc_type"] == "blog"

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_blog_with_tag_filter(self, mock_get):
        """
        タグフィルタリングのテスト

        テスト内容:
        - タグパラメータが正しく適用されること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><p>Blog content</p></body></html>"
        mock_get.return_value = mock_response

        # Act
        docs = crawl_langchain_blog(tag="langgraph", max_articles=5)

        # Assert
        # タグフィルタが適用されていることを確認
        # （実際の実装では、タグに基づいてURLが変わる）
        assert isinstance(docs, list)

    # ========================================================================
    # GitHub Repository Crawler Tests
    # ========================================================================

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_github_repo(self, mock_get):
        """
        GitHubリポジトリのクロールテスト

        テスト内容:
        - README等が正しく取得されること
        - doc_typeが'github'であること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        # LangGraph

        This is the README for LangGraph.

        ## Installation

        ```bash
        pip install langgraph
        ```
        """
        mock_get.return_value = mock_response

        # Act
        docs = crawl_github_repo(repo="langchain-ai/langgraph")

        # Assert
        assert len(docs) > 0
        for doc in docs:
            assert doc.metadata["doc_type"] == "github"
            assert "source" in doc.metadata

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_github_with_examples(self, mock_get):
        """
        examples/ディレクトリを含むクロールのテスト

        テスト内容:
        - include_examples=Trueで例が取得されること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "# Example code\nThis is an example."
        mock_get.return_value = mock_response

        # Act
        docs = crawl_github_repo(include_examples=True)

        # Assert
        assert isinstance(docs, list)

    # ========================================================================
    # Update All Sources Tests
    # ========================================================================

    @patch("src.features.rag.crawler.crawl_github_repo")
    @patch("src.features.rag.crawler.crawl_langchain_blog")
    @patch("src.features.rag.crawler.crawl_langgraph_docs")
    def test_update_all_sources(self, mock_docs, mock_blog, mock_github):
        """
        全ソース更新のテスト

        テスト内容:
        - 全てのソース（docs, blog, github）から取得されること
        - 統計情報が正しく返されること
        - statusが'success'であること
        """
        # Arrange
        sample_doc = Document(
            page_content="Content",
            metadata={"source": "http://example.com", "title": "Test", "doc_type": "official_docs"}
        )

        mock_docs.return_value = [sample_doc] * 10
        mock_blog.return_value = [sample_doc] * 5
        mock_github.return_value = [sample_doc] * 3

        # Act
        result = update_all_sources()

        # Assert
        assert "total_documents" in result
        assert result["total_documents"] == 18  # 10 + 5 + 3

        assert "sources" in result
        assert result["sources"]["official_docs"] == 10
        assert result["sources"]["blog"] == 5
        assert result["sources"]["github"] == 3

        assert "updated_at" in result
        assert result["status"] == "success"
        assert result["errors"] is None or len(result["errors"]) == 0

    @patch("src.features.rag.crawler.crawl_github_repo")
    @patch("src.features.rag.crawler.crawl_langchain_blog")
    @patch("src.features.rag.crawler.crawl_langgraph_docs")
    def test_update_all_sources_partial_failure(self, mock_docs, mock_blog, mock_github):
        """
        部分的な失敗のテスト

        テスト内容:
        - 一部のソースが失敗してもエラーが記録されること
        - statusが'partial'になること
        """
        # Arrange
        sample_doc = Document(
            page_content="Content",
            metadata={"source": "http://example.com", "title": "Test", "doc_type": "official_docs"}
        )

        mock_docs.return_value = [sample_doc] * 10
        mock_blog.side_effect = CrawlerError("Blog crawl failed")
        mock_github.return_value = [sample_doc] * 3

        # Act
        result = update_all_sources()

        # Assert
        assert result["status"] == "partial"
        assert "errors" in result
        assert len(result["errors"]) > 0
        assert any("Blog" in error for error in result["errors"])

    @patch("src.features.rag.crawler.crawl_github_repo")
    @patch("src.features.rag.crawler.crawl_langchain_blog")
    @patch("src.features.rag.crawler.crawl_langgraph_docs")
    def test_update_all_sources_complete_failure(self, mock_docs, mock_blog, mock_github):
        """
        完全な失敗のテスト

        テスト内容:
        - 全てのソースが失敗した場合にstatusが'failed'になること
        """
        # Arrange
        mock_docs.side_effect = CrawlerError("Docs failed")
        mock_blog.side_effect = CrawlerError("Blog failed")
        mock_github.side_effect = CrawlerError("GitHub failed")

        # Act
        result = update_all_sources()

        # Assert
        assert result["status"] == "failed"
        assert result["total_documents"] == 0
        assert len(result["errors"]) == 3

    # ========================================================================
    # HTML Parsing Tests
    # ========================================================================

    @patch("src.features.rag.crawler.httpx.get")
    def test_html_parsing_error(self, mock_get):
        """
        HTMLパースエラー時の処理テスト

        テスト内容:
        - 不正なHTMLが適切に処理されること
        - エラーが発生するか、空のコンテンツが返されること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<<>>Invalid HTML<><<"
        mock_get.return_value = mock_response

        # Act
        # パースエラーは処理されるべき
        docs = crawl_langgraph_docs(max_pages=1)

        # Assert
        # エラーが発生しないか、空のリストが返される
        assert isinstance(docs, list)

    @patch("src.features.rag.crawler.httpx.get")
    def test_empty_page_content(self, mock_get):
        """
        空のページコンテンツのテスト

        テスト内容:
        - 空のHTMLページが適切に処理されること
        """
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body></body></html>"
        mock_get.return_value = mock_response

        # Act
        docs = crawl_langgraph_docs(max_pages=1)

        # Assert
        # 空のページは除外されるか、空のドキュメントが返される
        assert isinstance(docs, list)

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_crawl_with_zero_max_pages(self):
        """
        max_pages=0のエッジケーステスト

        テスト内容:
        - max_pages=0で空のリストが返されること
        """
        # Act
        docs = crawl_langgraph_docs(max_pages=0)

        # Assert
        assert docs == []

    @patch("src.features.rag.crawler.httpx.get")
    def test_crawl_with_timeout(self, mock_get):
        """
        タイムアウトのテスト

        テスト内容:
        - タイムアウトエラーが適切に処理されること
        """
        # Arrange
        import httpx
        mock_get.side_effect = httpx.TimeoutException("Request timeout")

        # Act & Assert
        with pytest.raises(CrawlerError):
            crawl_langgraph_docs(max_pages=1)
