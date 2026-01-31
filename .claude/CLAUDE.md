# LangGraph Catalyst - Project Guidelines

## Project Overview

**LangGraph Catalyst** は、LangGraph の学習支援とビジネス活用を促進する「触媒（Catalyst）」となるポートフォリオシステムです。

### Vision
- **ターゲット**: DX推進・AIコンサル等のBiz寄り人材を目指す転職活動でのアピール材料
- **アピールポイント**:
  - 最新AI技術（LangGraph）の実用経験 + ビジネス視点の統合
  - **フルスタック開発力**: React + FastAPI によるモダンなアーキテクチャ
- **設計思想**: 「なぜその設計にしたのか」を説明できる、クリーンでモジュール化されたコード

### Core Features

#### 1. LangGraph学習支援RAGシステム
- LangGraphの最新公式情報をベクトルDB（Chroma）に保存
- ユーザーの質問に対し、**ソース付き + コード例付き**で回答
- 手動コマンドで情報更新

#### 2. ビジネス課題→LangGraph構成案生成
- 汎用的なビジネス課題を入力として受け付け
- 出力形式:
  - **Mermaid図**: 視覚的なフロー図
  - **コード例**: 実装サンプル
  - **わかりやすい説明**: 非技術者にも伝わるBiz視点の解説

#### 3. 学習パス & テンプレート
- 初級〜上級の体系的な学習カリキュラム
- ユースケース別のLangGraphテンプレート集

### ドキュメント
- **API仕様書**: @docs/API_SPECIFICATION.md
- **テスト仕様書**: @docs/TEST_SPECIFICATION.md
- **実装手順**: @docs/TODO.md

---

## Technology Stack

### 現在の状態（Phase 1-8完了、Phase 9移行中）

| Category | Technology | Status | Rationale |
|----------|------------|--------|-----------|
| **Language** | Python | ✅ 完成 | LangChain/LangGraphエコシステムとの親和性 |
| **Core Framework** | LangGraph, LangChain | ✅ 完成 | エージェントワークフロー構築の業界標準 |
| **Vector DB** | Chroma | ✅ 完成 | 軽量でローカル実行可能、学習コストが低い |
| **LLM** | OpenAI API (GPT-4等) | ✅ 完成 | ドキュメント・事例が豊富、信頼性が高い |
| **UI (Legacy)** | Streamlit | ✅ 完成 | 高速開発、プロトタイピング |
| **Frontend** | React + TypeScript + Vite | 🚧 移行中 | モダンなUI、完全な自由度 |
| **UI Library** | Tailwind CSS + shadcn/ui | 🚧 移行中 | モダンなデザインシステム |
| **State Management** | Zustand | 🚧 移行中 | 軽量で学習コストが低い |
| **Backend API** | FastAPI | 🚧 移行中 | 高速、型安全、自動ドキュメント生成 |
| **Deployment** | Render (Frontend + Backend) | 🚧 移行中 | 無料枠あり、統一管理 |

---

## Architecture

### モノレポ構成（Phase 9移行後）

```
langgraph-catalyst/
├── backend/                    # FastAPI バックエンド
│   ├── main.py                 # FastAPIエントリーポイント
│   ├── api/
│   │   └── v1/                 # APIエンドポイント
│   │       ├── rag.py          # RAG API
│   │       └── architect.py    # 構成案生成 API
│   ├── core/
│   │   ├── config.py           # 設定管理
│   │   └── security.py         # 認証・セキュリティ
│   ├── schemas/                # Pydanticスキーマ
│   │   ├── rag.py
│   │   └── architect.py
│   └── tests/                  # APIテスト
│
├── frontend/                   # React フロントエンド
│   ├── src/
│   │   ├── App.tsx             # ルートコンポーネント
│   │   ├── pages/              # ページコンポーネント
│   │   ├── features/           # 機能別コンポーネント
│   │   │   ├── RAG/
│   │   │   ├── Architect/
│   │   │   ├── LearningPath/
│   │   │   └── Templates/
│   │   ├── components/         # 共通UIコンポーネント
│   │   ├── api/                # API通信層
│   │   ├── store/              # Zustand状態管理
│   │   ├── types/              # TypeScript型定義
│   │   └── utils/
│   ├── package.json
│   └── vite.config.ts
│
├── src/                        # 既存Pythonロジック（95%再利用）
│   ├── config/
│   │   └── settings.py         # 環境変数・設定管理
│   ├── features/               # ビジネスロジック（コア資産）
│   │   ├── rag/                # RAG学習支援機能
│   │   │   ├── crawler.py      # ドキュメント収集
│   │   │   ├── vectorstore.py  # Chroma操作
│   │   │   └── chain.py        # RAGチェーン
│   │   ├── architect/          # 構成案生成機能
│   │   │   ├── graph.py        # LangGraphワークフロー
│   │   │   ├── prompts.py      # プロンプトテンプレート
│   │   │   └── visualizer.py   # Mermaid図生成
│   │   ├── learning_path/      # 学習パス
│   │   └── templates/          # テンプレート
│   └── utils/
│       └── helpers.py
│
├── tests/                      # ユニットテスト（115+ tests）
│   ├── test_crawler.py
│   ├── test_vectorstore.py
│   ├── test_rag_chain.py
│   ├── test_architect_graph.py
│   └── ...
│
├── data/
│   └── chroma/                 # ベクトルDB永続化
│
├── requirements.txt            # Python依存パッケージ
├── render.yaml                 # Renderデプロイ設定（Frontend + Backend）
└── README.md
```

### Design Principles

1. **Feature-based構造**: 機能ごとにディレクトリを分離し、責務を明確化
2. **単一責任の原則**: 各モジュールは1つの責務のみを持つ
3. **設定の外部化**: 環境変数で設定を管理し、コードと分離
4. **テスタビリティ**: 依存性注入でモック可能な設計
5. **既存資産の保護**: `src/features/` の95%を再利用、テスト（115件）を完全維持

---

## RAG Data Sources

| Source | URL | Purpose |
|--------|-----|---------|
| 公式ドキュメント | https://langchain-ai.github.io/langgraph/ | APIリファレンス、チュートリアル |
| LangChain Blog | https://blog.langchain.dev/tag/langgraph/ | ユースケース、ベストプラクティス |
| GitHub | https://github.com/langchain-ai/langgraph | コード例、最新の実装パターン |

### Update Strategy
```bash
# 手動でRAGデータを更新
python -m src.features.rag.crawler --update
```

---

## Development Guidelines

### Code Style
```bash
# Python（バックエンド）
ruff format .
ruff check .

# Frontend（TypeScript/React）
cd frontend
npm run lint
npm run format
```

### Commit Convention
```
feat: 新機能追加
fix: バグ修正
docs: ドキュメント更新
refactor: リファクタリング
test: テスト追加・修正
style: コードスタイル修正
```

### Testing

**テスト仕様書**: @docs/TEST_SPECIFICATION.md

```bash
# バックエンド（Python）
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html

# フロントエンド（React）
cd frontend
npm run test
npm run test:e2e  # Playwright E2Eテスト
```

- **既存テスト**: 115+ ユニットテスト（86%+ カバレッジ）
- **新規テスト**: APIテスト、フロントエンドテスト、E2Eテスト
- LLM呼び出しはモックを使用

---

## Environment Variables

### バックエンド（FastAPI）
```bash
# .env
OPENAI_API_KEY=your_openai_api_key
CHROMA_PERSIST_DIR=./data/chroma
CORS_ORIGINS=https://langgraph-catalyst-frontend.onrender.com,http://localhost:5173
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### フロントエンド（React）
```bash
# frontend/.env.local（ローカル開発）
VITE_API_BASE_URL=http://localhost:8000/api/v1

# frontend/.env.production（本番）
VITE_API_BASE_URL=https://langgraph-catalyst-api.onrender.com/api/v1
```

---

## Deployment（Render統一）

### render.yaml（モノレポ対応）

```yaml
services:
  # バックエンド（FastAPI）
  - type: web
    name: langgraph-catalyst-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false  # Render Dashboardで手動設定
      - key: CORS_ORIGINS
        value: https://langgraph-catalyst-frontend.onrender.com

  # フロントエンド（React Static Site）
  - type: web
    name: langgraph-catalyst-frontend
    runtime: static
    buildCommand: cd frontend && npm ci && npm run build
    staticPublishPath: ./frontend/dist
    envVars:
      - key: VITE_API_BASE_URL
        value: https://langgraph-catalyst-api.onrender.com/api/v1
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

### 公開URL
- **フロントエンド**: https://langgraph-catalyst-frontend.onrender.com
- **バックエンドAPI**: https://langgraph-catalyst-api.onrender.com
- **API Docs**: https://langgraph-catalyst-api.onrender.com/docs

---

## Why This Architecture?

### なぜLangGraphを使うのか
- **状態管理**: 複雑な対話フローを明示的に管理できる
- **可視化**: グラフ構造で処理フローを視覚的に理解できる
- **拡張性**: ノード追加で機能拡張が容易

### なぜRAGを組み合わせるのか
- **最新情報対応**: LLMの学習データ以降の情報も回答可能
- **根拠の明示**: ソース付き回答で信頼性向上
- **学習支援**: 公式ドキュメントへの導線を提供

### なぜReact + FastAPIに移行するのか
- **UI自由度**: Streamlitの限界を超えたモダンなUI/UX
- **パフォーマンス**: CSRによる高速なインタラクション
- **スケーラビリティ**: API分離により、複数フロントエンド対応可能
- **業界標準**: React + FastAPI は業界で広く採用されている
- **ポートフォリオ価値**: フルスタック開発力のアピール

### なぜRender統一デプロイなのか
- **管理のシンプルさ**: 1つのプラットフォームでフロントエンド + バックエンドを管理
- **コスト最適化**: 両方とも無料枠で稼働可能
- **学習コスト低減**: 1つの管理画面、1つのrender.yaml
- **Infrastructure as Code**: render.yamlで再現可能なデプロイ

### なぜこのシステムを作るのか
- **差別化**: LangGraphを「使う」だけでなく「教える」システム
- **Biz視点**: 技術だけでなくビジネス価値も説明できる構成案
- **実用性**: 実際に企業のAI導入検討に使えるツール
- **技術アピール**: 最新技術（LangGraph、React、FastAPI）の実装経験

---

## Milestones

### Phase 1-8: Streamlit版 ✅ 完成
- [x] プロジェクト基盤構築
- [x] RAG学習支援機能
- [x] 構成案生成機能
- [x] 学習パス & テンプレート
- [x] テスト・品質向上（115+ tests, 86%+ coverage）
- [x] UI/UX改善

### Phase 9: React + FastAPI 移行 🚧 進行中
- [ ] バックエンドAPI化（FastAPI）
- [ ] React フロントエンド構築
- [ ] 認証・セキュリティ実装
- [ ] テスト整備（E2E、フロントエンド）
- [ ] Render統一デプロイ
- [ ] 段階的移行・並行稼働
- [ ] ドキュメント整備

詳細な実装計画: @docs/TODO.md

---

**Last Updated**: 2026-01-25
