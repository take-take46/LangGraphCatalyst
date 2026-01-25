"""
LangGraph Catalyst - Initial Data Loading Script

ベクトルストアに初期データを投入するスクリプト。
ドキュメントをクロールし、分割して、Chromaベクトルストアに保存します。
"""

import argparse
import logging
import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.features.rag.crawler import (  # noqa: E402
    crawl_github_repo,
    crawl_langchain_blog,
    crawl_langchain_docs,
    crawl_langgraph_docs,
)
from src.features.rag.vectorstore import ChromaVectorStore  # noqa: E402
from src.utils.helpers import split_documents  # noqa: E402

# ロガー設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Initialize vector store with LangGraph documentation"
    )
    parser.add_argument(
        "--max-docs-pages",
        type=int,
        default=10,
        help="Maximum pages to crawl from official docs",
    )
    parser.add_argument(
        "--max-blog-articles",
        type=int,
        default=5,
        help="Maximum articles to crawl from blog",
    )
    parser.add_argument(
        "--skip-github", action="store_true", help="Skip GitHub repository crawling"
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete existing collection and recreate",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print("=" * 70)
    print("LangGraph Catalyst - Vector Store Initialization")
    print("=" * 70)
    print()

    # ベクトルストアの初期化
    print("📦 Initializing vector store...")
    try:
        vectorstore = ChromaVectorStore()
        print(f"✅ Vector store initialized: {vectorstore.collection_name}")
        print(f"   Persist directory: {vectorstore.persist_directory}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize vector store: {e}")
        return 1

    # 既存のコレクションを削除する場合
    if args.recreate:
        print("🗑️  Deleting existing collection...")
        try:
            vectorstore.delete_collection()
            print("✅ Collection deleted")
            # 再初期化
            vectorstore = ChromaVectorStore()
            print("✅ Collection recreated")
            print()
        except Exception as e:
            print(f"⚠️  Warning: Could not delete collection: {e}")
            print()

    # 既存のドキュメント数を確認
    existing_count = vectorstore.get_collection_count()
    print(f"📊 Current documents in store: {existing_count}")
    print()

    all_documents = []

    # 1. LangGraph公式ドキュメントのクロール
    print("🌐 Crawling LangGraph official documentation...")
    try:
        docs_langgraph = crawl_langgraph_docs(
            max_pages=args.max_docs_pages, include_api_reference=True
        )
        print(f"✅ Crawled {len(docs_langgraph)} pages from LangGraph docs")
        all_documents.extend(docs_langgraph)
    except Exception as e:
        print(f"⚠️  Warning: Failed to crawl LangGraph docs: {e}")
    print()

    # 2. LangChain公式ドキュメント（関連ページ）のクロール
    print("🔗 Crawling LangChain official documentation (related pages)...")
    try:
        docs_langchain = crawl_langchain_docs(max_pages=10)
        print(f"✅ Crawled {len(docs_langchain)} pages from LangChain docs")
        all_documents.extend(docs_langchain)
    except Exception as e:
        print(f"⚠️  Warning: Failed to crawl LangChain docs: {e}")
    print()

    # 3. LangChain Blogのクロール
    print("📝 Crawling LangChain Blog...")
    try:
        docs_blog = crawl_langchain_blog(tag="langgraph", max_articles=args.max_blog_articles)
        print(f"✅ Crawled {len(docs_blog)} articles from blog")
        all_documents.extend(docs_blog)
    except Exception as e:
        print(f"⚠️  Warning: Failed to crawl blog: {e}")
    print()

    # 4. GitHubリポジトリのクロール
    if not args.skip_github:
        print("🐙 Crawling GitHub repository...")
        try:
            docs_github = crawl_github_repo(
                repo="langchain-ai/langgraph", include_examples=True, include_tests=False
            )
            print(f"✅ Crawled {len(docs_github)} documents from GitHub")
            all_documents.extend(docs_github)
        except Exception as e:
            print(f"⚠️  Warning: Failed to crawl GitHub: {e}")
        print()

    # ドキュメントが取得できなかった場合
    if not all_documents:
        print("❌ No documents were crawled. Exiting.")
        return 1

    print(f"📚 Total documents crawled: {len(all_documents)}")
    print()

    # 5. ドキュメントを分割
    print("✂️  Splitting documents into chunks...")
    try:
        splits = split_documents(all_documents)
        print(f"✅ Split into {len(splits)} chunks")
    except Exception as e:
        print(f"❌ Failed to split documents: {e}")
        return 1
    print()

    # 6. ベクトルストアに追加
    print("💾 Adding documents to vector store...")
    try:
        result = vectorstore.add_documents(splits, batch_size=50)

        print("✅ Document addition completed:")
        print(f"   Added: {result['added_count']} chunks")
        print(f"   Failed: {result['failed_count']} chunks")
        print(f"   Total in store: {result['total_documents_in_store']} chunks")
        print(f"   Status: {result['status']}")
    except Exception as e:
        print(f"❌ Failed to add documents: {e}")
        return 1
    print()

    # 7. サンプルクエリでテスト
    print("🔍 Testing with sample query...")
    try:
        test_query = "What is LangGraph?"
        results = vectorstore.similarity_search(test_query, k=3)

        print(f"✅ Sample query: '{test_query}'")
        print(f"   Found {len(results)} relevant documents")

        if results:
            print("\n   Top result:")
            print(f"   - Title: {results[0].metadata.get('title', 'N/A')}")
            print(f"   - Source: {results[0].metadata.get('source', 'N/A')}")
            print(f"   - Preview: {results[0].page_content[:100]}...")
    except Exception as e:
        print(f"⚠️  Warning: Sample query failed: {e}")
    print()

    print("=" * 70)
    print("✅ Vector store initialization completed successfully!")
    print("=" * 70)
    print()
    print("You can now run the Streamlit app:")
    print("  streamlit run src/app.py")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
