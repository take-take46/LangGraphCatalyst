#!/bin/bash
# データベース/ベクトルストアリセットスクリプト
# Usage: ./scripts/db-reset.sh [options]

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ヘルプメッセージ
show_help() {
    echo -e "${BLUE}=== LangGraph Catalyst - データベースリセットスクリプト ===${NC}"
    echo ""
    echo "Usage: ./scripts/db-reset.sh [option]"
    echo ""
    echo "Options:"
    echo "  reset        ベクトルストアをリセット (デフォルト)"
    echo "  init         ベクトルストアを初期化（データ投入）"
    echo "  backup       現在のデータをバックアップ"
    echo "  restore      バックアップからデータを復元"
    echo "  status       データベースの状態を表示"
    echo "  help         このヘルプを表示"
    echo ""
    echo "Examples:"
    echo "  ./scripts/db-reset.sh              # ベクトルストアをリセット"
    echo "  ./scripts/db-reset.sh init         # 初期化とデータ投入"
    echo "  ./scripts/db-reset.sh backup       # データをバックアップ"
}

# データベース状態確認
check_status() {
    echo -e "${BLUE}データベースの状態を確認しています...${NC}"

    if [ -d data/chroma ]; then
        DB_SIZE=$(du -sh data/chroma 2>/dev/null | cut -f1)
        FILE_COUNT=$(find data/chroma -type f 2>/dev/null | wc -l | tr -d ' ')
        echo -e "${GREEN}ベクトルストアディレクトリ: 存在${NC}"
        echo -e "  サイズ: $DB_SIZE"
        echo -e "  ファイル数: $FILE_COUNT"
    else
        echo -e "${YELLOW}ベクトルストアディレクトリ: 存在しません${NC}"
    fi

    if [ -d data/backups ]; then
        BACKUP_COUNT=$(ls -1 data/backups/*.tar.gz 2>/dev/null | wc -l | tr -d ' ')
        echo -e "${GREEN}バックアップ: $BACKUP_COUNT 件${NC}"
    else
        echo -e "${YELLOW}バックアップ: なし${NC}"
    fi
}

# ベクトルストアリセット
reset_db() {
    echo -e "${RED}警告: ベクトルストアをリセットします${NC}"
    echo -e "${YELLOW}全てのドキュメントデータが削除されます${NC}"
    read -p "続行しますか? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}リセットをキャンセルしました${NC}"
        exit 0
    fi

    echo -e "${BLUE}ベクトルストアをリセットしています...${NC}"
    rm -rf data/chroma/*
    mkdir -p data/chroma
    echo -e "${GREEN}✓ リセット完了${NC}"
}

# 初期化とデータ投入
init_db() {
    echo -e "${BLUE}ベクトルストアを初期化しています...${NC}"

    # リセット実行
    if [ -d data/chroma ] && [ "$(ls -A data/chroma)" ]; then
        echo -e "${YELLOW}既存のデータが存在します${NC}"
        read -p "リセットしてから初期化しますか? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf data/chroma/*
        else
            echo -e "${BLUE}初期化をキャンセルしました${NC}"
            exit 0
        fi
    fi

    mkdir -p data/chroma

    echo -e "${BLUE}サンプルドキュメントをクロールしています...${NC}"
    echo -e "${YELLOW}この処理には数分かかる場合があります${NC}"

    # クローラースクリプトを実行（存在する場合）
    if [ -f scripts/crawl-docs.sh ]; then
        ./scripts/crawl-docs.sh
    else
        echo -e "${YELLOW}注意: クローラースクリプトが見つかりません${NC}"
        echo -e "${YELLOW}手動でドキュメントをクロールする必要があります:${NC}"
        echo "  python3 -m src.features.rag.crawler --update"
    fi

    echo -e "${GREEN}✓ 初期化完了${NC}"
}

# バックアップ作成
backup_db() {
    if [ ! -d data/chroma ] || [ ! "$(ls -A data/chroma)" ]; then
        echo -e "${RED}エラー: バックアップするデータがありません${NC}"
        exit 1
    fi

    mkdir -p data/backups
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_FILE="data/backups/chroma_backup_${TIMESTAMP}.tar.gz"

    echo -e "${BLUE}データをバックアップしています...${NC}"
    tar -czf "$BACKUP_FILE" -C data chroma

    BACKUP_SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}✓ バックアップ完了${NC}"
    echo -e "  ファイル: $BACKUP_FILE"
    echo -e "  サイズ: $BACKUP_SIZE"
}

# バックアップから復元
restore_db() {
    if [ ! -d data/backups ]; then
        echo -e "${RED}エラー: バックアップディレクトリが存在しません${NC}"
        exit 1
    fi

    # バックアップファイル一覧表示
    echo -e "${BLUE}利用可能なバックアップ:${NC}"
    BACKUPS=(data/backups/*.tar.gz)

    if [ ! -e "${BACKUPS[0]}" ]; then
        echo -e "${RED}エラー: バックアップファイルが見つかりません${NC}"
        exit 1
    fi

    select BACKUP_FILE in "${BACKUPS[@]}" "キャンセル"; do
        if [ "$BACKUP_FILE" = "キャンセル" ]; then
            echo -e "${BLUE}復元をキャンセルしました${NC}"
            exit 0
        elif [ -n "$BACKUP_FILE" ]; then
            break
        fi
    done

    echo -e "${YELLOW}警告: 現在のデータを上書きします${NC}"
    read -p "続行しますか? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}復元をキャンセルしました${NC}"
        exit 0
    fi

    echo -e "${BLUE}データを復元しています...${NC}"
    rm -rf data/chroma/*
    tar -xzf "$BACKUP_FILE" -C data
    echo -e "${GREEN}✓ 復元完了${NC}"
}

# メイン処理
case "${1:-reset}" in
    reset)
        reset_db
        ;;
    init)
        init_db
        ;;
    backup)
        backup_db
        ;;
    restore)
        restore_db
        ;;
    status)
        check_status
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
