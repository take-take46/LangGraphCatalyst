#!/bin/bash
# アプリケーション起動スクリプト
# Usage: ./scripts/run.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - アプリケーション起動スクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/run.sh [option]"
    echo ""
    echo "Options:"
    echo "  dev          開発モードで起動 (デフォルト)"
    echo "  prod         本番モードで起動"
    echo "  debug        デバッグモードで起動"
    echo "  port PORT    ポート番号を指定して起動"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/run.sh              # 開発モードで起動"
    echo "  ./scripts/run.sh prod         # 本番モードで起動"
    echo "  ./scripts/run.sh port 8080    # ポート8080で起動"
}

# 環境変数チェック
check_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}警告: .env ファイルが見つかりません${NC}"
        echo -e "${YELLOW}.env.example をコピーして .env を作成してください${NC}"
        echo ""
        read -p "続行しますか? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# メイン処理
case "${1:-dev}" in
    dev)
        echo -e "${GREEN}開発モードでアプリケーションを起動しています...${NC}"
        echo -e "${BLUE}URL: http://localhost:8501${NC}"
        echo -e "${YELLOW}Ctrl+C で終了${NC}"
        echo ""
        check_env
        streamlit run src/app.py --server.runOnSave=true
        ;;
    prod)
        echo -e "${GREEN}本番モードでアプリケーションを起動しています...${NC}"
        echo -e "${BLUE}URL: http://localhost:8501${NC}"
        echo -e "${YELLOW}Ctrl+C で終了${NC}"
        echo ""
        check_env
        streamlit run src/app.py \
            --server.headless=true \
            --server.enableCORS=false \
            --server.enableXsrfProtection=true
        ;;
    debug)
        echo -e "${GREEN}デバッグモードでアプリケーションを起動しています...${NC}"
        echo -e "${BLUE}URL: http://localhost:8501${NC}"
        echo -e "${YELLOW}Ctrl+C で終了${NC}"
        echo ""
        check_env
        export LOG_LEVEL=DEBUG
        streamlit run src/app.py --logger.level=debug
        ;;
    port)
        if [ -z "$2" ]; then
            echo -e "${RED}エラー: ポート番号を指定してください${NC}"
            echo "Usage: ./scripts/run.sh port <port_number>"
            exit 1
        fi
        echo -e "${GREEN}ポート $2 でアプリケーションを起動しています...${NC}"
        echo -e "${BLUE}URL: http://localhost:$2${NC}"
        echo -e "${YELLOW}Ctrl+C で終了${NC}"
        echo ""
        check_env
        streamlit run src/app.py --server.port=$2
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
