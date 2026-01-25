#!/bin/bash
# クリーンアップスクリプト
# Usage: ./scripts/clean.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - クリーンアップスクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/clean.sh [option]"
    echo ""
    echo "Options:"
    echo "  all          全てをクリーンアップ (デフォルト)"
    echo "  cache        キャッシュファイルのみ削除"
    echo "  test         テスト関連ファイルのみ削除"
    echo "  logs         ログファイルのみ削除"
    echo "  db           データベース/ベクトルストアを削除"
    echo "  deep         完全クリーンアップ（DB、ログ、キャッシュ全て）"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/clean.sh              # 基本的なクリーンアップ"
    echo "  ./scripts/clean.sh cache        # キャッシュのみ削除"
    echo "  ./scripts/clean.sh deep         # 完全クリーンアップ"
}

# キャッシュファイル削除
clean_cache() {
    echo -e "${BLUE}キャッシュファイルを削除しています...${NC}"
    rm -rf __pycache__
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type f -name "*.pyo" -delete 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    echo -e "${GREEN}✓ キャッシュファイルを削除しました${NC}"
}

# テスト関連ファイル削除
clean_test() {
    echo -e "${BLUE}テスト関連ファイルを削除しています...${NC}"
    rm -rf .pytest_cache
    rm -rf htmlcov
    rm -rf .coverage
    rm -rf coverage.xml
    rm -rf tests/.pytest_cache
    rm -rf tests/__pycache__
    echo -e "${GREEN}✓ テスト関連ファイルを削除しました${NC}"
}

# ログファイル削除
clean_logs() {
    if [ ! -d logs ]; then
        echo -e "${YELLOW}ログディレクトリが存在しません${NC}"
        return
    fi

    echo -e "${BLUE}ログファイルを削除しています...${NC}"
    rm -rf logs/*
    echo -e "${GREEN}✓ ログファイルを削除しました${NC}"
}

# データベース/ベクトルストア削除
clean_db() {
    echo -e "${YELLOW}警告: データベースとベクトルストアを削除します${NC}"
    echo -e "${RED}この操作は元に戻せません！${NC}"
    read -p "続行しますか? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}データベース削除をキャンセルしました${NC}"
        return
    fi

    echo -e "${BLUE}データベースを削除しています...${NC}"
    rm -rf data/chroma/*
    echo -e "${GREEN}✓ データベースを削除しました${NC}"
}

# 一時ファイル削除
clean_temp() {
    echo -e "${BLUE}一時ファイルを削除しています...${NC}"
    rm -rf .DS_Store
    find . -name ".DS_Store" -delete 2>/dev/null || true
    rm -rf *.tmp
    rm -rf /tmp/langgraph-catalyst-* 2>/dev/null || true
    echo -e "${GREEN}✓ 一時ファイルを削除しました${NC}"
}

# メイン処理
case "${1:-all}" in
    all)
        echo -e "${GREEN}クリーンアップを開始します...${NC}"
        echo ""
        clean_cache
        clean_test
        clean_temp
        echo ""
        echo -e "${GREEN}✓ クリーンアップ完了${NC}"
        ;;
    cache)
        clean_cache
        ;;
    test)
        clean_test
        ;;
    logs)
        clean_logs
        ;;
    db)
        clean_db
        ;;
    deep)
        echo -e "${RED}警告: 完全クリーンアップを実行します${NC}"
        echo -e "${YELLOW}データベース、ログ、キャッシュが全て削除されます${NC}"
        read -p "続行しますか? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}クリーンアップをキャンセルしました${NC}"
            exit 0
        fi

        echo ""
        clean_cache
        clean_test
        clean_logs
        echo -e "${YELLOW}データベース削除の確認...${NC}"
        clean_db
        clean_temp
        echo ""
        echo -e "${GREEN}✓ 完全クリーンアップ完了${NC}"
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
