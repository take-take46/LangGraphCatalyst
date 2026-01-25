#!/bin/bash
# デプロイ前チェックスクリプト
# Usage: ./scripts/pre-deploy.sh

set -e

# カラー定義
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ERRORS=0

echo -e "${BLUE}=== LangGraph Catalyst - デプロイ前チェック ===${NC}"
echo ""

# 1. 環境変数チェック
echo -e "${BLUE}[1/7] 環境変数をチェックしています...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env ファイルが見つかりません${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓ .env ファイルが存在します${NC}"

    # APIキーの存在確認（値は表示しない）
    if grep -q "OPENAI_API_KEY=your_openai_api_key" .env; then
        echo -e "${YELLOW}⚠ OpenAI APIキーがデフォルト値のままです${NC}"
        ERRORS=$((ERRORS + 1))
    elif grep -q "OPENAI_API_KEY=sk-" .env; then
        echo -e "${GREEN}✓ OpenAI APIキーが設定されています${NC}"
    else
        echo -e "${RED}✗ OpenAI APIキーが設定されていません${NC}"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 2. 依存関係チェック
echo ""
echo -e "${BLUE}[2/7] 依存関係をチェックしています...${NC}"
if pip3 show streamlit &> /dev/null && \
   pip3 show langchain &> /dev/null && \
   pip3 show chromadb &> /dev/null; then
    echo -e "${GREEN}✓ 必要なパッケージがインストールされています${NC}"
else
    echo -e "${RED}✗ 必要なパッケージが不足しています${NC}"
    echo -e "${YELLOW}実行してください: ./scripts/setup.sh deps${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. コードフォーマットチェック
echo ""
echo -e "${BLUE}[3/7] コードフォーマットをチェックしています...${NC}"
if ruff format --check . &> /dev/null; then
    echo -e "${GREEN}✓ コードフォーマットは正しいです${NC}"
else
    echo -e "${YELLOW}⚠ フォーマットが必要なファイルがあります${NC}"
    echo -e "${YELLOW}実行してください: ./scripts/format.sh${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 4. リントチェック
echo ""
echo -e "${BLUE}[4/7] リントをチェックしています...${NC}"
if ruff check . &> /dev/null; then
    echo -e "${GREEN}✓ リントエラーはありません${NC}"
else
    echo -e "${YELLOW}⚠ リントエラーが見つかりました${NC}"
    echo -e "${YELLOW}実行してください: ./scripts/lint.sh fix${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 5. テスト実行
echo ""
echo -e "${BLUE}[5/7] テストを実行しています...${NC}"
if python3 -m pytest tests/ -m "not integration and not slow" -q &> /dev/null; then
    echo -e "${GREEN}✓ 全てのテストが合格しました${NC}"
else
    echo -e "${RED}✗ テストが失敗しました${NC}"
    echo -e "${YELLOW}実行してください: ./scripts/test.sh${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 6. 必須ファイルチェック
echo ""
echo -e "${BLUE}[6/7] 必須ファイルをチェックしています...${NC}"
REQUIRED_FILES=(
    "src/app.py"
    "requirements.txt"
    "render.yaml"
    "README.md"
)

ALL_FILES_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ $file が見つかりません${NC}"
        ALL_FILES_EXIST=false
        ERRORS=$((ERRORS + 1))
    fi
done

if $ALL_FILES_EXIST; then
    echo -e "${GREEN}✓ 全ての必須ファイルが存在します${NC}"
fi

# 7. セキュリティチェック
echo ""
echo -e "${BLUE}[7/7] セキュリティをチェックしています...${NC}"
SECURITY_ISSUES=false

# .envファイルが.gitignoreに含まれているか
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo -e "${RED}✗ .env が .gitignore に含まれていません${NC}"
    SECURITY_ISSUES=true
    ERRORS=$((ERRORS + 1))
fi

# APIキーがコードにハードコーディングされていないか
if grep -r "sk-[a-zA-Z0-9]\{32,\}" src/ tests/ 2>/dev/null | grep -v ".pyc" | grep -q "sk-"; then
    echo -e "${RED}✗ APIキーがソースコードにハードコーディングされている可能性があります${NC}"
    SECURITY_ISSUES=true
    ERRORS=$((ERRORS + 1))
fi

if ! $SECURITY_ISSUES; then
    echo -e "${GREEN}✓ セキュリティチェックに合格しました${NC}"
fi

# 結果サマリー
echo ""
echo -e "${BLUE}================================${NC}"

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ 全てのチェックに合格しました！${NC}"
    echo -e "${GREEN}デプロイの準備ができています${NC}"
    echo ""
    echo -e "${BLUE}次のステップ:${NC}"
    echo "  1. git add ."
    echo "  2. git commit -m \"Release: vX.X.X\""
    echo "  3. git push origin main"
    echo "  4. Renderで自動デプロイされます"
    exit 0
else
    echo -e "${RED}✗ $ERRORS 件の問題が見つかりました${NC}"
    echo -e "${YELLOW}上記の問題を修正してから再度実行してください${NC}"
    exit 1
fi
