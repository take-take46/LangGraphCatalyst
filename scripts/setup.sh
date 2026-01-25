#!/bin/bash
# 環境セットアップスクリプト
# Usage: ./scripts/setup.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - 環境セットアップスクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/setup.sh [option]"
    echo ""
    echo "Options:"
    echo "  all          完全セットアップ（依存関係+環境変数+データ） (デフォルト)"
    echo "  deps         依存関係のみインストール"
    echo "  env          環境変数ファイルのみセットアップ"
    echo "  dev          開発用依存関係も含めてインストール"
    echo "  clean        クリーンインストール（既存を削除してから）"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/setup.sh              # 完全セットアップ"
    echo "  ./scripts/setup.sh dev          # 開発環境セットアップ"
    echo "  ./scripts/setup.sh clean        # クリーンインストール"
}

# Pythonバージョンチェック
check_python() {
    echo -e "${BLUE}Pythonバージョンをチェックしています...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}エラー: Python 3 がインストールされていません${NC}"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}Python $PYTHON_VERSION が見つかりました${NC}"
}

# 依存関係インストール
install_deps() {
    echo -e "${BLUE}依存関係をインストールしています...${NC}"
    pip3 install -r requirements.txt
    echo -e "${GREEN}✓ 依存関係のインストール完了${NC}"
}

# 開発用依存関係インストール
install_dev_deps() {
    echo -e "${BLUE}開発用依存関係をインストールしています...${NC}"
    pip3 install -r requirements.txt
    pip3 install pytest pytest-cov pytest-mock ruff
    echo -e "${GREEN}✓ 開発用依存関係のインストール完了${NC}"
}

# 環境変数ファイルセットアップ
setup_env() {
    if [ -f .env ]; then
        echo -e "${YELLOW}.env ファイルは既に存在します${NC}"
        read -p "上書きしますか? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}.env のセットアップをスキップしました${NC}"
            return
        fi
    fi

    echo -e "${BLUE}.env ファイルを作成しています...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env ファイルを作成しました${NC}"
    echo -e "${YELLOW}重要: .env ファイルを編集して、APIキー等を設定してください${NC}"
}

# データディレクトリ作成
setup_data_dirs() {
    echo -e "${BLUE}データディレクトリを作成しています...${NC}"
    mkdir -p data/chroma
    mkdir -p logs
    echo -e "${GREEN}✓ データディレクトリを作成しました${NC}"
}

# クリーンアップ
cleanup() {
    echo -e "${YELLOW}既存の環境をクリーンアップしています...${NC}"
    rm -rf __pycache__
    rm -rf .pytest_cache
    rm -rf htmlcov
    rm -rf .coverage
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    echo -e "${GREEN}✓ クリーンアップ完了${NC}"
}

# メイン処理
case "${1:-all}" in
    all)
        echo -e "${GREEN}完全セットアップを開始します...${NC}"
        echo ""
        check_python
        install_deps
        setup_env
        setup_data_dirs
        echo ""
        echo -e "${GREEN}✓ セットアップ完了${NC}"
        echo -e "${YELLOW}次のステップ:${NC}"
        echo "  1. .env ファイルを編集してAPIキーを設定"
        echo "  2. アプリケーションを起動: ./scripts/run.sh"
        ;;
    deps)
        check_python
        install_deps
        ;;
    env)
        setup_env
        ;;
    dev)
        echo -e "${GREEN}開発環境セットアップを開始します...${NC}"
        echo ""
        check_python
        install_dev_deps
        setup_env
        setup_data_dirs
        echo ""
        echo -e "${GREEN}✓ 開発環境セットアップ完了${NC}"
        ;;
    clean)
        echo -e "${YELLOW}クリーンインストールを実行します${NC}"
        read -p "続行しますか? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
        cleanup
        check_python
        install_deps
        setup_env
        setup_data_dirs
        echo -e "${GREEN}✓ クリーンインストール完了${NC}"
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
