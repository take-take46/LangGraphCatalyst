#!/bin/bash
# ドキュメントクロールスクリプト
# Usage: ./scripts/crawl-docs.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - ドキュメントクロールスクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/crawl-docs.sh [option]"
    echo ""
    echo "Options:"
    echo "  all          全ソースからクロール (デフォルト)"
    echo "  docs         公式ドキュメントのみ"
    echo "  blog         ブログ記事のみ"
    echo "  github       GitHubリポジトリのみ"
    echo "  update       既存データを更新"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/crawl-docs.sh              # 全ソースからクロール"
    echo "  ./scripts/crawl-docs.sh docs         # 公式ドキュメントのみ"
    echo "  ./scripts/crawl-docs.sh update       # 既存データを更新"
}

# クロール実行
run_crawler() {
    SOURCE=$1
    echo -e "${BLUE}ドキュメントをクロールしています: $SOURCE${NC}"
    echo -e "${YELLOW}この処理には数分かかる場合があります...${NC}"

    # Pythonクローラーを実行
    python3 -c "
from src.features.rag.crawler import (
    crawl_langgraph_docs,
    crawl_langchain_blog,
    crawl_github_repo,
    update_all_sources
)
from src.features.rag.vectorstore import ChromaVectorStore

vectorstore = ChromaVectorStore()

if '$SOURCE' == 'all':
    result = update_all_sources()
    print(f'合計 {result[\"total_documents\"]} 件のドキュメントを取得しました')
elif '$SOURCE' == 'docs':
    docs = crawl_langgraph_docs(max_pages=100)
    result = vectorstore.add_documents(docs)
    print(f'{result[\"added_count\"]} 件のドキュメントを追加しました')
elif '$SOURCE' == 'blog':
    docs = crawl_langchain_blog(max_articles=50)
    result = vectorstore.add_documents(docs)
    print(f'{result[\"added_count\"]} 件のドキュメントを追加しました')
elif '$SOURCE' == 'github':
    docs = crawl_github_repo(include_examples=True)
    result = vectorstore.add_documents(docs)
    print(f'{result[\"added_count\"]} 件のドキュメントを追加しました')
"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ クロール完了${NC}"
    else
        echo -e "${RED}✗ クロール中にエラーが発生しました${NC}"
        exit 1
    fi
}

# メイン処理
case "${1:-all}" in
    all)
        echo -e "${GREEN}全ソースからドキュメントをクロールします${NC}"
        echo ""
        run_crawler "all"
        ;;
    docs)
        echo -e "${GREEN}公式ドキュメントをクロールします${NC}"
        echo ""
        run_crawler "docs"
        ;;
    blog)
        echo -e "${GREEN}ブログ記事をクロールします${NC}"
        echo ""
        run_crawler "blog"
        ;;
    github)
        echo -e "${GREEN}GitHubリポジトリをクロールします${NC}"
        echo ""
        run_crawler "github"
        ;;
    update)
        echo -e "${GREEN}既存データを更新します${NC}"
        echo ""
        run_crawler "all"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}エラー: 不明なオプション: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}ベクトルストアの統計情報:${NC}"
python3 -c "
from src.features.rag.vectorstore import ChromaVectorStore
vs = ChromaVectorStore()
# ここに統計情報を表示するコードを追加
print('ドキュメント数: 確認してください')
"
