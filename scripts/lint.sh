#!/bin/bash
# リントチェックスクリプト
# Usage: ./scripts/lint.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - リントチェックスクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/lint.sh [option]"
    echo ""
    echo "Options:"
    echo "  all          全ファイルをチェック (デフォルト)"
    echo "  fix          自動修正可能な問題を修正"
    echo "  src          srcディレクトリのみチェック"
    echo "  tests        testsディレクトリのみチェック"
    echo "  file FILE    特定のファイルのみチェック"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/lint.sh              # 全ファイルをチェック"
    echo "  ./scripts/lint.sh fix          # 自動修正"
    echo "  ./scripts/lint.sh file app.py  # 特定ファイルのみ"
}

# メイン処理
case "${1:-all}" in
    all)
        echo -e "${GREEN}全ファイルをリントチェックしています...${NC}"
        if ruff check .; then
            echo -e "${GREEN}✓ リントエラーはありません${NC}"
        else
            echo -e "${RED}✗ リントエラーが見つかりました${NC}"
            echo -e "${YELLOW}自動修正するには: ./scripts/lint.sh fix${NC}"
            exit 1
        fi
        ;;
    fix)
        echo -e "${GREEN}自動修正可能な問題を修正しています...${NC}"
        ruff check --fix .
        echo -e "${GREEN}✓ 修正完了${NC}"
        echo -e "${YELLOW}手動修正が必要な問題が残っている可能性があります${NC}"
        ;;
    src)
        echo -e "${GREEN}srcディレクトリをリントチェックしています...${NC}"
        if ruff check src/; then
            echo -e "${GREEN}✓ リントエラーはありません${NC}"
        else
            echo -e "${RED}✗ リントエラーが見つかりました${NC}"
            exit 1
        fi
        ;;
    tests)
        echo -e "${GREEN}testsディレクトリをリントチェックしています...${NC}"
        if ruff check tests/; then
            echo -e "${GREEN}✓ リントエラーはありません${NC}"
        else
            echo -e "${RED}✗ リントエラーが見つかりました${NC}"
            exit 1
        fi
        ;;
    file)
        if [ -z "$2" ]; then
            echo -e "${RED}エラー: ファイル名を指定してください${NC}"
            echo "Usage: ./scripts/lint.sh file <filename>"
            exit 1
        fi
        echo -e "${GREEN}ファイル $2 をリントチェックしています...${NC}"
        if ruff check "$2"; then
            echo -e "${GREEN}✓ リントエラーはありません${NC}"
        else
            echo -e "${RED}✗ リントエラーが見つかりました${NC}"
            exit 1
        fi
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
