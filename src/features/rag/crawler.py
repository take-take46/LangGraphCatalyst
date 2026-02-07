"""
LangGraph Catalyst - Document Crawler

LangGraph公式ドキュメント、ブログ、GitHubリポジトリから
ドキュメントを収集するクローラー。
"""

import argparse
import logging
from typing import Any

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

from src.utils.exceptions import CrawlerError
from src.utils.helpers import get_current_timestamp

logger = logging.getLogger(__name__)

# LangGraphドキュメントのベースURL（新URL）
LANGGRAPH_DOCS_BASE = "https://docs.langchain.com/oss/python/langgraph/"

# LangChain BlogのベースURL
LANGCHAIN_BLOG_BASE = "https://blog.langchain.dev/tag/langgraph/"

# GitHubリポジトリのベースURL
GITHUB_REPO_BASE = "https://github.com/langchain-ai/langgraph"

# LangChain公式ドキュメントのベースURL
LANGCHAIN_DOCS_BASE = "https://docs.langchain.com/oss/python/langchain/"

# LangGraphと関連性の高いLangChainドキュメントページ（絶対パス）
LANGCHAIN_RELATED_PAGES = [
    # Core Foundation
    "https://docs.langchain.com/oss/python/langchain/agents",
    "https://docs.langchain.com/oss/python/langchain/messages",
    "https://docs.langchain.com/oss/python/langchain/tools",
    "https://docs.langchain.com/oss/python/langchain/models",
    # State Management & Memory
    "https://docs.langchain.com/oss/python/langchain/short-term-memory",
    # Execution & Control Flow
    "https://docs.langchain.com/oss/python/langchain/middleware",
    "https://docs.langchain.com/oss/python/langchain/streaming",
    "https://docs.langchain.com/oss/python/langchain/human_in_the_loop",
    # Advanced Patterns
    "https://docs.langchain.com/oss/python/langchain/multi_agent",
    "https://docs.langchain.com/oss/python/langchain/retrieval",
]

# 主要なLangGraphドキュメントページ（相対パス）
LANGGRAPH_KEY_PAGES = [
    # Core Overview & Getting Started
    "overview",
    "install",
    "quickstart",
    "thinking-in-langgraph",
    "workflows-agents",
    "local-server",
    # Core Capabilities
    "persistence",
    "durable-execution",
    "streaming",
    "interrupts",
    "use-time-travel",
    "add-memory",
    "use-subgraphs",
    # API Reference & Design
    "choosing-apis",
    "graph-api",
    "use-graph-api",
    "functional-api",
    "use-functional-api",
    "pregel",
    # Production & Deployment
    "application-structure",
    "test",
    "studio",
    "ui",
    "deploy",
    "observability",
    # Tutorials
    "agentic-rag",
    "sql-agent",
]


def crawl_langgraph_docs(
    max_pages: int = 100,
    include_api_reference: bool = True,  # noqa: ARG001
) -> list[Document]:
    """
    LangGraph公式ドキュメントをクロール

    Args:
        max_pages: クロールする最大ページ数
        include_api_reference: APIリファレンスを含めるか

    Returns:
        list[Document]: 取得したドキュメントのリスト

    Raises:
        CrawlerError: クロールエラー
    """
    logger.info("Starting to crawl LangGraph official documentation")

    documents = []

    # 主要なドキュメントページを構築
    pages_to_crawl = [LANGGRAPH_DOCS_BASE]  # トップページを追加

    # キーページを追加（max_pages制限内）
    for page in LANGGRAPH_KEY_PAGES[: max_pages - 1]:
        pages_to_crawl.append(f"{LANGGRAPH_DOCS_BASE}{page}")

    for url in pages_to_crawl:
        try:
            # URLからページ名を抽出してタイトルに使用
            page_name = url.split("/")[-1] or "index"
            docs = _load_web_page(url, doc_type="official_docs", title=f"LangGraph - {page_name}")
            documents.extend(docs)
            logger.info(f"Successfully crawled: {url}")
        except Exception as e:
            logger.warning(f"Failed to crawl {url}: {e}")
            continue

    logger.info(f"Crawled {len(documents)} documents from LangGraph official docs")
    return documents


def crawl_langchain_docs(max_pages: int = 10) -> list[Document]:
    """
    LangChain公式ドキュメント（LangGraphと関連性の高いページ）をクロール

    Args:
        max_pages: クロールする最大ページ数

    Returns:
        list[Document]: 取得したドキュメントのリスト

    Raises:
        CrawlerError: クロールエラー
    """
    logger.info("Starting to crawl LangChain official documentation (LangGraph-related)")

    documents = []

    # 関連ページを取得（max_pages制限内）
    pages_to_crawl = LANGCHAIN_RELATED_PAGES[:max_pages]

    for url in pages_to_crawl:
        try:
            # URLからページ名を抽出してタイトルに使用
            page_name = url.split("/")[-1] or "index"
            docs = _load_web_page(url, doc_type="langchain_docs", title=f"LangChain - {page_name}")
            documents.extend(docs)
            logger.info(f"Successfully crawled: {url}")
        except Exception as e:
            logger.warning(f"Failed to crawl {url}: {e}")
            continue

    logger.info(f"Crawled {len(documents)} documents from LangChain official docs")
    return documents


def crawl_langchain_blog(
    tag: str = "langgraph",
    max_articles: int = 50,  # noqa: ARG001
) -> list[Document]:
    """
    LangChain Blogから記事をクロール

    Args:
        tag: フィルタリングするタグ
        max_articles: 取得する最大記事数

    Returns:
        list[Document]: 取得したドキュメントのリスト

    Raises:
        CrawlerError: クロールエラー
    """
    logger.info(f"Starting to crawl LangChain Blog with tag: {tag}")

    documents = []

    # ブログページ
    blog_url = f"{LANGCHAIN_BLOG_BASE}"

    try:
        docs = _load_web_page(blog_url, doc_type="blog", title="LangChain Blog - LangGraph")
        documents.extend(docs)
        logger.info(f"Successfully crawled blog: {blog_url}")
    except Exception as e:
        logger.warning(f"Failed to crawl blog {blog_url}: {e}")

    logger.info(f"Crawled {len(documents)} articles from LangChain Blog")
    return documents


def crawl_github_repo(
    repo: str = "langchain-ai/langgraph",
    include_examples: bool = True,
    include_tests: bool = False,  # noqa: ARG001
) -> list[Document]:
    """
    GitHubリポジトリからREADME、examplesなどを取得

    Args:
        repo: リポジトリ名 (owner/repo)
        include_examples: examples/ディレクトリを含めるか
        include_tests: tests/ディレクトリを含めるか

    Returns:
        list[Document]: 取得したドキュメントのリスト

    Raises:
        CrawlerError: クロールエラー
    """
    logger.info(f"Starting to crawl GitHub repository: {repo}")

    documents = []

    # READMEページ
    readme_url = f"https://github.com/{repo}/blob/main/README.md"

    try:
        docs = _load_web_page(readme_url, doc_type="github", title=f"{repo} - README")
        documents.extend(docs)
        logger.info(f"Successfully crawled README: {readme_url}")
    except Exception as e:
        logger.warning(f"Failed to crawl README {readme_url}: {e}")

    # Examples（重要なJupyter notebooksを取得）
    if include_examples:
        example_notebooks = [
            # RAG examples
            "examples/rag/langgraph_agentic_rag.ipynb",
            "examples/rag/langgraph_adaptive_rag.ipynb",
            "examples/rag/langgraph_self_rag.ipynb",
            "examples/rag/langgraph_crag.ipynb",
            # Multi-agent
            "examples/multi_agent/hierarchical_agent_teams.ipynb",
            "examples/multi_agent/multi-agent-collaboration.ipynb",
            # Plan-and-Execute
            "examples/plan-and-execute/plan-and-execute.ipynb",
            # Customer Support (business use case)
            "examples/customer-support/customer-support.ipynb",
            # Human-in-the-Loop
            "examples/human_in_the_loop/wait-user-input.ipynb",
            # SQL Agent
            "examples/tutorials/sql-agent.ipynb",
        ]

        for notebook_path in example_notebooks:
            # GitHubのblobページURLを構築
            notebook_url = f"https://github.com/{repo}/blob/main/{notebook_path}"
            title = notebook_path.split("/")[-1].replace(".ipynb", "")

            try:
                docs = _load_web_page(
                    notebook_url, doc_type="github_example", title=f"Example: {title}"
                )
                documents.extend(docs)
                logger.info(f"Successfully crawled example: {notebook_path}")
            except Exception as e:
                logger.warning(f"Failed to crawl example {notebook_path}: {e}")

    logger.info(f"Crawled {len(documents)} documents from GitHub repository")
    return documents


def update_all_sources() -> dict[str, Any]:
    """
    すべてのソースからドキュメントを更新

    Returns:
        dict: 更新結果の統計情報
    """
    logger.info("Starting to update all document sources")

    results = {
        "total_documents": 0,
        "sources": {},
        "updated_at": get_current_timestamp(),
        "status": "success",
        "errors": [],
    }

    # LangGraph公式ドキュメント
    try:
        docs_langgraph = crawl_langgraph_docs(max_pages=20)
        results["sources"]["langgraph_docs"] = len(docs_langgraph)
        results["total_documents"] += len(docs_langgraph)
    except Exception as e:
        error_msg = f"Failed to crawl LangGraph docs: {e}"
        logger.error(error_msg)
        results["errors"].append(error_msg)
        results["status"] = "partial"

    # LangChain公式ドキュメント（関連ページ）
    try:
        docs_langchain = crawl_langchain_docs(max_pages=10)
        results["sources"]["langchain_docs"] = len(docs_langchain)
        results["total_documents"] += len(docs_langchain)
    except Exception as e:
        error_msg = f"Failed to crawl LangChain docs: {e}"
        logger.error(error_msg)
        results["errors"].append(error_msg)
        results["status"] = "partial"

    # ブログ記事
    try:
        docs_blog = crawl_langchain_blog(max_articles=10)
        results["sources"]["blog"] = len(docs_blog)
        results["total_documents"] += len(docs_blog)
    except Exception as e:
        error_msg = f"Failed to crawl blog: {e}"
        logger.error(error_msg)
        results["errors"].append(error_msg)
        results["status"] = "partial"

    # GitHub
    try:
        docs_github = crawl_github_repo()
        results["sources"]["github"] = len(docs_github)
        results["total_documents"] += len(docs_github)
    except Exception as e:
        error_msg = f"Failed to crawl GitHub: {e}"
        logger.error(error_msg)
        results["errors"].append(error_msg)
        results["status"] = "partial"

    if results["total_documents"] == 0:
        results["status"] = "failed"

    logger.info(
        f"Update completed. Total documents: {results['total_documents']}, Status: {results['status']}"
    )

    return results


def _load_web_page(url: str, doc_type: str, title: str) -> list[Document]:
    """
    Webページをロードしてドキュメントに変換

    Args:
        url: ページURL
        doc_type: ドキュメントタイプ
        title: ページタイトル

    Returns:
        list[Document]: ロードしたドキュメント

    Raises:
        CrawlerError: ロードエラー
    """
    try:
        # セレクターなしでページ全体を取得
        # （JavaScriptレンダリングされたコンテンツは取得できないが、
        # 静的HTMLコンテンツは全て取得可能）
        loader = WebBaseLoader(web_paths=(url,))

        documents = loader.load()

        # メタデータを追加
        for doc in documents:
            doc.metadata.update(
                {
                    "source": url,
                    "title": title,
                    "doc_type": doc_type,
                    "updated_at": get_current_timestamp(),
                }
            )

        return documents

    except Exception as e:
        raise CrawlerError(f"Failed to load web page {url}: {e}") from e


def main():
    """CLIコマンドのメイン関数"""
    parser = argparse.ArgumentParser(description="LangGraph Catalyst Document Crawler")
    parser.add_argument("--update", action="store_true", help="Update all document sources")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum pages to crawl")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    # ログレベル設定
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.update:
        print("Updating all document sources...")
        results = update_all_sources()

        print("\n=== Update Results ===")
        print(f"Status: {results['status']}")
        print(f"Total documents: {results['total_documents']}")
        print(f"Sources: {results['sources']}")
        print(f"Updated at: {results['updated_at']}")

        if results["errors"]:
            print("\nErrors:")
            for error in results["errors"]:
                print(f"  - {error}")
    else:
        print("Use --update to update all document sources")


if __name__ == "__main__":
    main()
