#!/bin/bash
# テスト実行スクリプト
# Usage: ./scripts/test.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - テスト実行スクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/test.sh [option]"
    echo ""
    echo "Options:"
    echo "  all          全テストを実行 (デフォルト)"
    echo "  unit         ユニットテストのみ実行"
    echo "  integration  統合テストのみ実行"
    echo "  coverage     カバレッジ付きで全テスト実行"
    echo "  fast         高速テスト（遅いテストをスキップ）"
    echo "  watch        ファイル変更を監視してテスト自動実行"
    echo "  file FILE    特定のテストファイルのみ実行"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/test.sh                    # 全テスト実行"
    echo "  ./scripts/test.sh unit               # ユニットテストのみ"
    echo "  ./scripts/test.sh coverage           # カバレッジ付き"
    echo "  ./scripts/test.sh file test_crawler  # 特定ファイルのみ"
}

# メイン処理
case "${1:-all}" in
    all)
        echo -e "${GREEN}全テストを実行しています...${NC}"
        python3 -m pytest tests/ -v
        ;;
    unit)
        echo -e "${GREEN}ユニットテストを実行しています...${NC}"
        python3 -m pytest tests/ -m "not integration and not e2e and not slow" -v
        ;;
    integration)
        echo -e "${GREEN}統合テストを実行しています...${NC}"
        python3 -m pytest tests/ -m integration -v
        ;;
    coverage)
        echo -e "${GREEN}カバレッジ付きでテストを実行しています...${NC}"
        python3 -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -v
        echo -e "${BLUE}カバレッジレポートを htmlcov/index.html に出力しました${NC}"
        echo -e "${YELLOW}ブラウザで確認: open htmlcov/index.html${NC}"
        ;;
    fast)
        echo -e "${GREEN}高速テストを実行しています（遅いテストをスキップ）...${NC}"
        python3 -m pytest tests/ -m "not slow" -v
        ;;
    watch)
        echo -e "${GREEN}ファイル変更を監視してテストを自動実行します...${NC}"
        echo -e "${YELLOW}Ctrl+C で終了${NC}"
        python3 -m pytest-watch tests/ src/
        ;;
    file)
        if [ -z "$2" ]; then
            echo -e "${RED}エラー: テストファイル名を指定してください${NC}"
            echo "Usage: ./scripts/test.sh file <filename>"
            exit 1
        fi
        echo -e "${GREEN}テストファイル $2 を実行しています...${NC}"
        python3 -m pytest tests/test_$2.py -v
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

echo -e "${GREEN}✓ 完了${NC}"
