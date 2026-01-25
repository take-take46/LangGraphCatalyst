# ⚡ LangGraph Catalyst

<div align="center">

**LangGraphの学習支援とビジネス活用を促進する、次世代の触媒システム**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[デモを見る](#) | [ドキュメント](./docs/) | [お問い合わせ](#お問い合わせ)

</div>

---

## 📋 目次

- [概要](#-概要)
- [主要機能](#-主要機能)
- [技術スタック](#-技術スタック)
- [セットアップ](#-セットアップ)
- [使い方](#-使い方)
- [開発ガイド](#-開発ガイド)
- [デプロイ](#-デプロイ)
- [設計思想](#-設計思想)
- [ロードマップ](#-ロードマップ)
- [ライセンス](#-ライセンス)

---

## 🎯 概要

**LangGraph Catalyst** は、LangGraphの学習からビジネス活用まで、開発者の生産性を最大化するオールインワンプラットフォームです。

### 🌟 プロジェクトの特徴

- 🎓 **体系的学習**: 初級から上級まで段階的にLangGraphを習得
- 📚 **RAG学習支援**: 最新ドキュメントからソース付き回答を提供
- 🎨 **豊富なテンプレート**: 即座に使える実装パターン集
- 🏗️ **自動構成案生成**: ビジネス課題から最適なアーキテクチャを提案
- 💼 **企業向け設計**: 実務での活用を想定したプロフェッショナルなUI/UX

---

## 🚀 主要機能

### 1️⃣ **RAG学習支援システム**

<img src="https://via.placeholder.com/800x400?text=RAG+Learning+Support+Screenshot" alt="RAG Learning Support" width="100%">

LangGraphの最新公式情報をベクトルDB（Chroma）に保存し、質問に対してソース付き+コード例付きで回答。

- ✅ 公式ドキュメント、ブログ、GitHubリポジトリから自動収集
- ✅ 高精度な意味検索による関連情報の抽出
- ✅ 実行可能なコード例を含む詳細な回答
- ✅ 参照元URLと抜粋を明示した信頼性の高い回答

### 2️⃣ **学習パス機能**

<img src="https://via.placeholder.com/800x400?text=Learning+Path+Screenshot" alt="Learning Path" width="100%">

初級・中級・上級の3段階で体系的にLangGraphを学習。

- ✅ 各トピックに学習目標と推定時間を明示
- ✅ 進捗管理機能で学習状況を可視化
- ✅ サンプル質問ボタンで即座にRAGモードで学習
- ✅ 参考リソースへのリンク完備

### 3️⃣ **テンプレート集**

<img src="https://via.placeholder.com/800x400?text=Templates+Screenshot" alt="Templates" width="100%">

カテゴリ別・難易度別に整理された、実践的なLangGraphテンプレート。

- ✅ カスタマーサポート、データ分析、文書処理など10種類以上
- ✅ 完全に動作するコード + Mermaid図 + 詳細な説明
- ✅ 難易度フィルタでレベルに合わせて選択可能
- ✅ ワンクリックでコードをコピー&実行

### 4️⃣ **ビジネス課題→構成案自動生成**

<img src="https://via.placeholder.com/800x400?text=Architecture+Generation+Screenshot" alt="Architecture Generation" width="100%">

ビジネス課題を入力すると、LangGraphを活用した最適な構成案を自動生成。

- ✅ **Mermaid図**: システムフローを視覚的に表現
- ✅ **コード例**: 実装サンプルを自動生成
- ✅ **わかりやすい説明**: 非技術者向けのBiz視点の解説
- ✅ **実装ノート**: 技術的な注意点を明示

---

## 🛠️ 技術スタック

| カテゴリ | 技術 | バージョン | 用途 |
|---------|------|-----------|------|
| **言語** | Python | 3.11+ | メイン開発言語 |
| **コアフレームワーク** | LangGraph | Latest | エージェントワークフロー構築 |
| **LLMフレームワーク** | LangChain | Latest | LLMアプリケーション基盤 |
| **ベクトルDB** | Chroma | Latest | ドキュメント埋め込みと検索 |
| **LLM** | OpenAI API | GPT-4 Turbo | 言語モデル |
| **WebUI** | Streamlit | Latest | フロントエンド |
| **デプロイ** | Render | - | ホスティング |
| **テスト** | pytest | Latest | ユニット・統合テスト |
| **リント・フォーマット** | Ruff | Latest | コード品質管理 |

### アーキテクチャ図

```
langgraph-catalyst/
├── src/
│   ├── app.py                      # Streamlit エントリーポイント
│   ├── config/
│   │   └── settings.py             # 環境変数・設定管理
│   ├── features/
│   │   ├── rag/                    # RAG学習支援機能
│   │   │   ├── crawler.py          # ドキュメントクローラー
│   │   │   ├── vectorstore.py      # Chromaベクトルストア
│   │   │   └── chain.py            # RAGチェーン
│   │   ├── architect/              # 構成案生成機能
│   │   │   ├── graph.py            # LangGraphワークフロー
│   │   │   ├── prompts.py          # プロンプトテンプレート
│   │   │   └── visualizer.py       # Mermaid図生成
│   │   ├── templates/              # テンプレート定義
│   │   └── learning_path/          # 学習パス定義
│   ├── components/                 # 再利用可能なUIコンポーネント
│   │   └── sidebar.py
│   └── utils/                      # ユーティリティ関数
│       ├── helpers.py
│       ├── styles.py               # カスタムCSS
│       ├── exceptions.py           # カスタム例外
│       └── caching.py              # キャッシング
├── data/chroma/                    # ベクトルDB永続化
├── tests/                          # テストコード
│   ├── test_rag/
│   ├── test_architect/
│   └── test_integration/
├── docs/                           # ドキュメント
│   ├── API_SPECIFICATION.md        # API仕様書
│   ├── TEST_SPECIFICATION.md       # テスト仕様書
│   └── TODO.md                     # 開発計画
├── scripts/                        # ユーティリティスクリプト
│   └── init_vectorstore.py         # ベクトルストア初期化
├── .streamlit/                     # Streamlit設定
│   └── config.toml
├── requirements.txt                # 依存パッケージ
├── pyproject.toml                  # プロジェクト設定（Ruff等）
└── render.yaml                     # Renderデプロイ設定
```

---

## 📦 セットアップ

### 前提条件

- Python 3.11 以上
- OpenAI API キー
- Git

### 1️⃣ リポジトリのクローン

```bash
git clone https://github.com/your-username/LangGraphCatalyst.git
cd LangGraphCatalyst
```

### 2️⃣ 仮想環境の作成

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3️⃣ 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 4️⃣ 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成します。

```bash
cp .env.example .env
```

`.env` ファイルを編集して、OpenAI APIキーを設定してください：

```bash
OPENAI_API_KEY=your_openai_api_key_here
CHROMA_PERSIST_DIR=./data/chroma
LOG_LEVEL=INFO
```

### 5️⃣ RAGデータの初期化（必須）

初回起動前に、ベクトルストアにLangGraphのドキュメントを投入する必要があります：

```bash
python scripts/init_vectorstore.py
```

**オプション:**

```bash
# より多くのドキュメントを取得（時間がかかります）
python scripts/init_vectorstore.py --max-docs-pages 20 --max-blog-articles 10

# 既存のデータを削除して再作成
python scripts/init_vectorstore.py --recreate

# 詳細なログを表示
python scripts/init_vectorstore.py --verbose
```

### 6️⃣ アプリケーションの起動

```bash
streamlit run src/app.py
```

ブラウザで `http://localhost:8501` にアクセスしてください。

---

## 📖 使い方

### 🎓 学習パスモード

1. サイドバーで「**学習パス**」を選択
2. 初級・中級・上級から学習したいレベルを選択
3. 各トピックの説明を読み、サンプル質問で学習
4. 学習が完了したらチェックマークを付けて進捗管理

### 📚 RAG学習支援モード

1. サイドバーで「**RAG学習支援**」を選択
2. LangGraphに関する質問を入力（例: "LangGraphでマルチエージェントシステムを構築する方法は？"）
3. ソース付きの詳細な回答とコード例を確認
4. 参照元ドキュメントへのリンクをクリックして深掘り

### 🎨 テンプレートモード

1. サイドバーで「**テンプレート**」を選択
2. カテゴリや難易度でフィルタリング
3. テンプレートを選択してコード・Mermaid図・説明を確認
4. コードをコピーしてローカル環境で実行

### 🏗️ 構成案生成モード

1. サイドバーで「**構成案生成**」を選択
2. ビジネス課題を入力（例: "カスタマーサポートの自動化を実現したい"）
3. 業界や制約条件を指定（オプション）
4. Mermaid図、コード例、説明を確認
5. 結果をMarkdownファイルとしてダウンロード

---

## 🧑‍💻 開発ガイド

### コードフォーマット

```bash
# コードを自動フォーマット
ruff format .
```

### リント

```bash
# コードの静的解析
ruff check .

# 自動修正可能な問題を修正
ruff check . --fix
```

### テスト実行

```bash
# 全テストを実行
pytest tests/ -v

# 特定のテストマーカーで実行
pytest tests/ -m "not integration" -v

# カバレッジ付きで実行
pytest tests/ --cov=src --cov-report=html
```

### 開発ワークフロー

1. **ブランチ作成**: `git checkout -b feature/new-feature`
2. **開発**: コードを実装
3. **テスト**: `pytest tests/ -v`
4. **フォーマット**: `ruff format .`
5. **リント**: `ruff check .`
6. **コミット**: `git commit -m "feat: add new feature"`
7. **プッシュ**: `git push origin feature/new-feature`
8. **プルリクエスト**: GitHubでPR作成

---

## 🌐 デプロイ

### Renderへのデプロイ

1. GitHubリポジトリをRenderに接続
2. Render管理画面で以下の環境変数を設定:
   - `OPENAI_API_KEY`: OpenAI APIキー
3. `render.yaml` の設定に従って自動デプロイ

**render.yaml 例:**

```yaml
services:
  - type: web
    name: langgraph-catalyst
    env: python
    buildCommand: |
      pip install -r requirements.txt
      python scripts/init_vectorstore.py --max-docs-pages 10
    startCommand: streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: OPENAI_API_KEY
        sync: false
```

---

## 💡 設計思想

### なぜLangGraphを使うのか？

- **🔄 状態管理**: 複雑な対話フローを明示的に管理できる
- **👁️ 可視化**: グラフ構造で処理フローを視覚的に理解できる
- **🔧 拡張性**: ノード追加で機能拡張が容易
- **🧪 テスタビリティ**: 各ノードを独立してテスト可能

### なぜRAGを組み合わせるのか？

- **📰 最新情報対応**: LLMの学習データ以降の情報も回答可能
- **📚 根拠の明示**: ソース付き回答で信頼性向上
- **🎓 学習支援**: 公式ドキュメントへの導線を提供
- **🔍 正確性向上**: ハルシネーションを大幅に削減

### なぜこのシステムを作るのか？

- **🎯 差別化**: LangGraphを「使う」だけでなく「教える」システム
- **💼 Biz視点**: 技術だけでなくビジネス価値も説明できる構成案
- **🏢 実用性**: 実際に企業のAI導入検討に使えるツール
- **🚀 生産性**: 開発者の学習コストを削減し、実装速度を向上

---

## 🗺️ ロードマップ

### Phase 1-4: 基盤構築 ✅
- [x] プロジェクト構造のセットアップ
- [x] Streamlit基本UI
- [x] RAG学習支援機能
- [x] 構成案生成機能

### Phase 5: テスト・品質向上 ✅
- [x] ユニットテスト
- [x] 統合テスト
- [x] エラーハンドリング
- [x] パフォーマンス最適化

### Phase 6: UI/UX改善 ✅
- [x] プロフェッショナルなデザイン
- [x] ローディングアニメーション
- [x] ヘルプセクション
- [x] レスポンシブ対応
- [x] アクセシビリティ向上

### Phase 7: デプロイ・公開 🚧
- [ ] Renderへのデプロイ
- [ ] 本番環境テスト
- [ ] ドキュメント整備
- [ ] デモURL公開

### Phase 8: 継続的改善 📋
- [ ] ユーザーフィードバック収集
- [ ] RAGデータの自動更新機能
- [ ] 他LLMプロバイダー対応（Claude, Gemini等）
- [ ] マルチモーダル対応

---

## 📄 ライセンス

MIT License - 詳細は [LICENSE](LICENSE) をご覧ください。

---

## 🤝 お問い合わせ

- **GitHub Issues**: [Issues](https://github.com/your-username/LangGraphCatalyst/issues)
- **Pull Requests**: [PRs](https://github.com/your-username/LangGraphCatalyst/pulls)
- **Email**: your-email@example.com

---

## 🙏 謝辞

このプロジェクトは以下のオープンソースプロジェクトに支えられています：

- [LangGraph](https://github.com/langchain-ai/langgraph) - LangChain公式のステートフルエージェントフレームワーク
- [LangChain](https://github.com/langchain-ai/langchain) - LLMアプリケーション開発フレームワーク
- [Streamlit](https://streamlit.io/) - データアプリケーションフレームワーク
- [Chroma](https://www.trychroma.com/) - オープンソースベクトルデータベース
- [OpenAI](https://openai.com/) - GPT-4 APIの提供

---

<div align="center">

**Built with ❤️ using LangGraph, LangChain, and Streamlit**

⭐ このプロジェクトが役に立ったら、スターをお願いします！

</div>
