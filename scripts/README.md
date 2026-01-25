# LangGraph Catalyst - 開発・運用スクリプト集

このディレクトリには、LangGraph Catalystの開発・運用に便利なスクリプトがまとめられています。

## 📋 目次

- [クイックスタート](#クイックスタート)
- [スクリプト一覧](#スクリプト一覧)
- [使用例](#使用例)
- [トラブルシューティング](#トラブルシューティング)

---

## 🚀 クイックスタート

### 初回セットアップ

```bash
# 1. 実行権限を付与
chmod +x scripts/*.sh

# 2. 環境をセットアップ
./scripts/setup.sh all

# 3. .envファイルを編集してAPIキーを設定
vim .env

# 4. アプリケーションを起動
./scripts/run.sh
```

### 日常的な開発フロー

```bash
# コードを変更したら...

# 1. フォーマット
./scripts/format.sh

# 2. リントチェック
./scripts/lint.sh

# 3. テスト実行
./scripts/test.sh unit

# 4. アプリケーション起動
./scripts/run.sh dev
```

### デプロイ前

```bash
# 全てのチェックを実行
./scripts/pre-deploy.sh
```

---

## 📚 スクリプト一覧

### 1. `test.sh` - テスト実行

**用途**: ユニットテスト、統合テスト、カバレッジテストの実行

**使い方**:
```bash
# 全テスト実行
./scripts/test.sh all

# ユニットテストのみ
./scripts/test.sh unit

# 統合テストのみ
./scripts/test.sh integration

# カバレッジ付き実行
./scripts/test.sh coverage

# 高速テスト（遅いテストをスキップ）
./scripts/test.sh fast

# 特定のテストファイルのみ
./scripts/test.sh file crawler
```

**主なオプション**:
- `all`: 全テスト実行（デフォルト）
- `unit`: ユニットテストのみ
- `integration`: 統合テストのみ
- `coverage`: カバレッジレポート付き
- `fast`: 高速テスト
- `file <name>`: 特定ファイルのみ

---

### 2. `run.sh` - アプリケーション起動

**用途**: Streamlitアプリケーションの起動

**使い方**:
```bash
# 開発モード（デフォルト）
./scripts/run.sh dev

# 本番モード
./scripts/run.sh prod

# デバッグモード
./scripts/run.sh debug

# ポート指定
./scripts/run.sh port 8080
```

**主なオプション**:
- `dev`: 開発モード（ファイル保存で自動リロード）
- `prod`: 本番モード（headless、CORS無効）
- `debug`: デバッグモード（詳細ログ出力）
- `port <number>`: ポート番号指定

**アクセスURL**:
- デフォルト: http://localhost:8501

---

### 3. `format.sh` - コードフォーマット

**用途**: Ruffを使用したコードフォーマット

**使い方**:
```bash
# 全ファイルをフォーマット
./scripts/format.sh all

# チェックのみ（変更なし）
./scripts/format.sh check

# srcディレクトリのみ
./scripts/format.sh src

# testsディレクトリのみ
./scripts/format.sh tests

# 特定ファイルのみ
./scripts/format.sh file src/app.py
```

**主なオプション**:
- `all`: 全ファイルをフォーマット（デフォルト）
- `check`: チェックのみ
- `src`: srcディレクトリのみ
- `tests`: testsディレクトリのみ
- `file <path>`: 特定ファイルのみ

---

### 4. `lint.sh` - リントチェック

**用途**: Ruffを使用したコード品質チェック

**使い方**:
```bash
# 全ファイルをチェック
./scripts/lint.sh all

# 自動修正
./scripts/lint.sh fix

# srcディレクトリのみ
./scripts/lint.sh src

# testsディレクトリのみ
./scripts/lint.sh tests

# 特定ファイルのみ
./scripts/lint.sh file src/app.py
```

**主なオプション**:
- `all`: 全ファイルをチェック（デフォルト）
- `fix`: 自動修正可能な問題を修正
- `src`: srcディレクトリのみ
- `tests`: testsディレクトリのみ
- `file <path>`: 特定ファイルのみ

---

### 5. `setup.sh` - 環境セットアップ

**用途**: 開発環境の初期セットアップ

**使い方**:
```bash
# 完全セットアップ
./scripts/setup.sh all

# 依存関係のみ
./scripts/setup.sh deps

# 環境変数ファイルのみ
./scripts/setup.sh env

# 開発環境セットアップ
./scripts/setup.sh dev

# クリーンインストール
./scripts/setup.sh clean
```

**主なオプション**:
- `all`: 完全セットアップ（デフォルト）
- `deps`: 依存関係のみインストール
- `env`: .envファイルのみセットアップ
- `dev`: 開発用依存関係も含む
- `clean`: クリーンインストール

**実行内容**:
1. Pythonバージョンチェック
2. 依存パッケージインストール
3. .envファイル作成（.env.exampleからコピー）
4. データディレクトリ作成

---

### 6. `clean.sh` - クリーンアップ

**用途**: 不要なファイル・キャッシュの削除

**使い方**:
```bash
# 基本的なクリーンアップ
./scripts/clean.sh all

# キャッシュのみ
./scripts/clean.sh cache

# テスト関連ファイルのみ
./scripts/clean.sh test

# ログファイルのみ
./scripts/clean.sh logs

# データベースのみ
./scripts/clean.sh db

# 完全クリーンアップ
./scripts/clean.sh deep
```

**主なオプション**:
- `all`: 基本的なクリーンアップ（デフォルト）
- `cache`: Pythonキャッシュファイル
- `test`: テスト関連ファイル
- `logs`: ログファイル
- `db`: データベース/ベクトルストア
- `deep`: 完全クリーンアップ（全て）

**削除されるファイル**:
- `__pycache__/`: Pythonキャッシュ
- `.pytest_cache/`: pytestキャッシュ
- `htmlcov/`: カバレッジレポート
- `.coverage`: カバレッジデータ
- `logs/*`: ログファイル
- `data/chroma/*`: ベクトルストア（dbオプション時）

---

### 7. `db-reset.sh` - データベース管理

**用途**: ベクトルストアのリセット・バックアップ・復元

**使い方**:
```bash
# ベクトルストアをリセット
./scripts/db-reset.sh reset

# 初期化とデータ投入
./scripts/db-reset.sh init

# バックアップ作成
./scripts/db-reset.sh backup

# バックアップから復元
./scripts/db-reset.sh restore

# 状態確認
./scripts/db-reset.sh status
```

**主なオプション**:
- `reset`: ベクトルストアをリセット（デフォルト）
- `init`: 初期化とサンプルデータ投入
- `backup`: 現在のデータをバックアップ
- `restore`: バックアップから復元
- `status`: データベースの状態を表示

**バックアップファイル**:
- 保存先: `data/backups/`
- 形式: `chroma_backup_YYYYMMDD_HHMMSS.tar.gz`

---

### 8. `pre-deploy.sh` - デプロイ前チェック

**用途**: デプロイ前の総合チェック

**使い方**:
```bash
# 全チェックを実行
./scripts/pre-deploy.sh
```

**チェック項目**:
1. 環境変数の存在確認
2. 依存関係の確認
3. コードフォーマットチェック
4. リントチェック
5. テスト実行
6. 必須ファイルの存在確認
7. セキュリティチェック

**終了コード**:
- `0`: 全てのチェックに合格（デプロイ可能）
- `1`: チェックに失敗（修正が必要）

---

### 9. `crawl-docs.sh` - ドキュメントクロール

**用途**: LangGraphドキュメントのクロールとベクトルストアへの投入

**使い方**:
```bash
# 全ソースからクロール
./scripts/crawl-docs.sh all

# 公式ドキュメントのみ
./scripts/crawl-docs.sh docs

# ブログ記事のみ
./scripts/crawl-docs.sh blog

# GitHubリポジトリのみ
./scripts/crawl-docs.sh github

# 既存データを更新
./scripts/crawl-docs.sh update
```

**主なオプション**:
- `all`: 全ソースからクロール（デフォルト）
- `docs`: 公式ドキュメントのみ
- `blog`: LangChain Blogのみ
- `github`: GitHubリポジトリのみ
- `update`: 既存データを更新

**クロール対象**:
- LangGraph公式ドキュメント
- LangChain Blog（LangGraphタグ）
- GitHub: langchain-ai/langgraph

---

## 💡 使用例

### 開発開始時

```bash
# 1. 環境セットアップ（初回のみ）
./scripts/setup.sh all

# 2. APIキーを設定
vim .env

# 3. アプリケーション起動
./scripts/run.sh dev
```

### コード変更後

```bash
# 1. フォーマット
./scripts/format.sh

# 2. リントチェックと自動修正
./scripts/lint.sh fix

# 3. テスト実行
./scripts/test.sh unit

# 4. 問題なければコミット
git add .
git commit -m "feat: 新機能追加"
```

### データベース初期化

```bash
# 1. 既存データをバックアップ
./scripts/db-reset.sh backup

# 2. データベースをリセット
./scripts/db-reset.sh reset

# 3. ドキュメントをクロール
./scripts/crawl-docs.sh all

# 4. 状態確認
./scripts/db-reset.sh status
```

### デプロイ前

```bash
# 1. 全チェック実行
./scripts/pre-deploy.sh

# 2. 問題なければデプロイ
git push origin main
```

### 環境クリーンアップ

```bash
# 1. キャッシュとテストファイルを削除
./scripts/clean.sh all

# 2. 必要に応じてデータベースも削除
./scripts/clean.sh deep

# 3. 再セットアップ
./scripts/setup.sh all
```

---

## 🔧 トラブルシューティング

### スクリプトが実行できない

```bash
# 実行権限を付与
chmod +x scripts/*.sh
```

### テストが失敗する

```bash
# 1. 依存関係を再インストール
./scripts/setup.sh clean

# 2. キャッシュをクリア
./scripts/clean.sh cache

# 3. テストを再実行
./scripts/test.sh all
```

### アプリケーションが起動しない

```bash
# 1. .envファイルを確認
cat .env

# 2. 依存関係を確認
pip3 list | grep streamlit

# 3. ログを確認してデバッグモードで起動
./scripts/run.sh debug
```

### データベースエラー

```bash
# 1. データベースの状態を確認
./scripts/db-reset.sh status

# 2. 必要に応じてリセット
./scripts/db-reset.sh reset

# 3. データを再投入
./scripts/crawl-docs.sh all
```

### フォーマット/リントエラー

```bash
# 1. 自動修正を試す
./scripts/format.sh all
./scripts/lint.sh fix

# 2. それでも解決しない場合は手動修正
ruff check . --show-source
```

---

## 📝 スクリプトのカスタマイズ

各スクリプトは環境に応じてカスタマイズ可能です。

### 環境変数で設定を変更

```bash
# ポート番号を変更
export PORT=8080
./scripts/run.sh

# ログレベルを変更
export LOG_LEVEL=DEBUG
./scripts/run.sh
```

### スクリプトを編集

```bash
# エディタで開く
vim scripts/test.sh

# 変更を保存後、実行権限を確認
chmod +x scripts/test.sh
```

---

## 🔒 セキュリティ注意事項

1. **APIキーの管理**
   - `.env` ファイルは絶対にコミットしない
   - `.gitignore` に `.env` が含まれていることを確認
   - スクリプト内にAPIキーをハードコーディングしない

2. **バックアップの管理**
   - `data/backups/` ディレクトリも `.gitignore` に含める
   - 本番データのバックアップは定期的に取得

3. **デプロイ前チェック**
   - 必ず `./scripts/pre-deploy.sh` を実行してからデプロイ
   - セキュリティチェックで警告が出た場合は必ず対応

---

## 📚 参考資料

- [プロジェクトREADME](../README.md)
- [開発ガイドライン](../CLAUDE.md)
- [テスト仕様書](../docs/TEST_SPECIFICATION.md)
- [API仕様書](../docs/API_SPECIFICATION.md)

---

**Last Updated**: 2026-01-25
