# スクリプトクイックスタートガイド

このファイルは、LangGraph Catalystの開発・運用スクリプトを素早く使い始めるためのガイドです。

## 🚀 最初の5分

### 1. 初回セットアップ（2分）

```bash
# プロジェクトルートに移動
cd ~/LangGraphCatalyst

# 環境をセットアップ
./scripts/setup.sh all

# .envファイルを編集（OpenAI APIキーを設定）
vim .env  # または nano .env
```

### 2. アプリケーション起動（30秒）

```bash
# アプリケーションを起動
./scripts/run.sh

# ブラウザで開く: http://localhost:8501
```

### 3. 開発開始（2分）

```bash
# 別ターミナルでテスト実行
./scripts/test.sh unit

# コードフォーマット
./scripts/format.sh

# リントチェック
./scripts/lint.sh
```

---

## 📋 よく使うコマンド一覧

### 開発中

```bash
# テスト実行
./scripts/test.sh unit          # ユニットテストのみ（速い）
./scripts/test.sh coverage      # カバレッジ付き

# コード品質
./scripts/format.sh             # フォーマット
./scripts/lint.sh fix           # リント自動修正

# アプリ起動
./scripts/run.sh dev            # 開発モード
./scripts/run.sh debug          # デバッグモード
```

### データベース管理

```bash
# 状態確認
./scripts/db-reset.sh status

# バックアップ
./scripts/db-reset.sh backup

# リセット
./scripts/db-reset.sh reset

# ドキュメントクロール
./scripts/crawl-docs.sh all
```

### クリーンアップ

```bash
# 基本クリーンアップ
./scripts/clean.sh all

# 完全クリーンアップ（DB含む）
./scripts/clean.sh deep
```

### デプロイ前

```bash
# 全チェック実行
./scripts/pre-deploy.sh

# 問題なければ
git push origin main
```

---

## 🎯 開発フロー

### 新機能開発

```bash
# 1. ブランチ作成
git checkout -b feature/new-feature

# 2. コードを書く
vim src/features/...

# 3. テスト実行
./scripts/test.sh unit

# 4. フォーマット＆リント
./scripts/format.sh
./scripts/lint.sh fix

# 5. 再度テスト
./scripts/test.sh coverage

# 6. コミット
git add .
git commit -m "feat: 新機能追加"

# 7. プッシュ
git push origin feature/new-feature
```

### バグ修正

```bash
# 1. テストで問題を再現
./scripts/test.sh file <test_name>

# 2. コードを修正
vim src/...

# 3. テストが通ることを確認
./scripts/test.sh file <test_name>

# 4. 全テスト実行
./scripts/test.sh all

# 5. コミット
git add .
git commit -m "fix: バグ修正"
```

### リリース準備

```bash
# 1. 全チェック実行
./scripts/pre-deploy.sh

# 2. 問題があれば修正
./scripts/format.sh
./scripts/lint.sh fix
./scripts/test.sh all

# 3. 再度チェック
./scripts/pre-deploy.sh

# 4. リリース
git tag v1.0.0
git push origin main --tags
```

---

## 🔍 トラブルシューティング早見表

| 問題 | 解決コマンド |
|------|------------|
| テストが失敗する | `./scripts/clean.sh cache && ./scripts/test.sh all` |
| アプリが起動しない | `./scripts/setup.sh clean` |
| フォーマットエラー | `./scripts/format.sh all` |
| リントエラー | `./scripts/lint.sh fix` |
| DBエラー | `./scripts/db-reset.sh reset` |
| 依存関係エラー | `./scripts/setup.sh deps` |
| 環境がおかしい | `./scripts/clean.sh deep && ./scripts/setup.sh all` |

---

## 📞 ヘルプ

各スクリプトは `--help` または `help` オプションでヘルプを表示できます。

```bash
./scripts/test.sh help
./scripts/run.sh help
./scripts/format.sh help
# など
```

詳細は [scripts/README.md](./README.md) を参照してください。

---

**Happy Coding! 🎉**
