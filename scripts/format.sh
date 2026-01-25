#!/bin/bash
# コードフォーマットスクリプト
# Usage: ./scripts/format.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - コードフォーマットスクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/format.sh [option]"
    echo ""
    echo "Options:"
    echo "  all          全ファイルをフォーマット (デフォルト)"
    echo "  check        フォーマットチェックのみ（変更なし）"
    echo "  src          srcディレクトリのみフォーマット"
    echo "  tests        testsディレクトリのみフォーマット"
    echo "  file FILE    特定のファイルのみフォーマット"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/format.sh              # 全ファイルをフォーマット"
    echo "  ./scripts/format.sh check        # チェックのみ"
    echo "  ./scripts/format.sh file app.py  # 特定ファイルのみ"
}

# メイン処理
case "${1:-all}" in
    all)
        echo -e "${GREEN}全ファイルをフォーマットしています...${NC}"
        ruff format .
        echo -e "${GREEN}✓ フォーマット完了${NC}"
        ;;
    check)
        echo -e "${GREEN}フォーマットをチェックしています...${NC}"
        if ruff format --check .; then
            echo -e "${GREEN}✓ すべてのファイルが正しくフォーマットされています${NC}"
        else
            echo -e "${RED}✗ フォーマットが必要なファイルがあります${NC}"
            echo -e "${YELLOW}修正するには: ./scripts/format.sh all${NC}"
            exit 1
        fi
        ;;
    src)
        echo -e "${GREEN}srcディレクトリをフォーマットしています...${NC}"
        ruff format src/
        echo -e "${GREEN}✓ フォーマット完了${NC}"
        ;;
    tests)
        echo -e "${GREEN}testsディレクトリをフォーマットしています...${NC}"
        ruff format tests/
        echo -e "${GREEN}✓ フォーマット完了${NC}"
        ;;
    file)
        if [ -z "$2" ]; then
            echo -e "${RED}エラー: ファイル名を指定してください${NC}"
            echo "Usage: ./scripts/format.sh file <filename>"
            exit 1
        fi
        echo -e "${GREEN}ファイル $2 をフォーマットしています...${NC}"
        ruff format "$2"
        echo -e "${GREEN}✓ フォーマット完了${NC}"
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
