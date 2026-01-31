# LangGraph Catalyst - Project Guidelines

## Project Overview

**LangGraph Catalyst** は、LangGraph の学習支援とビジネス活用を促進する「触媒（Catalyst）」となるポートフォリオシステムです。

### Vision
- **ターゲット**: DX推進・AIコンサル等のBiz寄り人材を目指す転職活動でのアピール材料
- **アピールポイント**: 最新AI技術（LangGraph）の実用経験 + ビジネス視点の統合
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


### API仕様書
@docs/API_SPECIFICATION.md

### ER図
@docs/TODO.md

### 実装手順
@docs/TODO.md


---

## Technology Stack

| Category | Technology | Rationale |
|----------|------------|-----------|
| Language | Python | LangChain/LangGraphエコシステムとの親和性 |
| Core Framework | LangGraph, LangChain | エージェントワークフロー構築の業界標準 |
| Vector DB | Chroma | 軽量でローカル実行可能、学習コストが低い |
| LLM | OpenAI API (GPT-4等) | ドキュメント・事例が豊富、信頼性が高い |
| Backend API | FastAPI | 高速、型安全、自動ドキュメント生成 |
| Frontend | React + TypeScript + Vite | モダンなUI、完全な自由度、高速開発 |
| UI Library | Tailwind CSS + Zustand | モダンなデザインシステム、軽量な状態管理 |
| Deployment | Render | 無料枠あり、Frontend + Backend統一管理 |

---

## Architecture

```
langgraph-catalyst/
├── backend/                   # FastAPI バックエンド
│   ├── main.py                # FastAPIエントリーポイント
│   ├── api/v1/                # APIエンドポイント
│   ├── core/                  # 設定・セキュリティ
│   ├── schemas/               # Pydanticスキーマ
│   └── tests/                 # APIテスト
├── frontend/                  # React フロントエンド
│   ├── src/
│   │   ├── App.tsx            # ルートコンポーネント
│   │   ├── pages/             # ページコンポーネント
│   │   ├── components/        # 共通UIコンポーネント
│   │   ├── api/               # API通信層
│   │   ├── store/             # Zustand状態管理
│   │   └── types/             # TypeScript型定義
│   ├── package.json
│   └── vite.config.ts
├── src/                       # 共有Pythonビジネスロジック
│   ├── config/
│   │   └── settings.py        # 環境変数・設定管理
│   ├── features/              # コア機能（FastAPIから使用）
│   │   ├── rag/               # RAG学習支援機能
│   │   │   ├── crawler.py     # ドキュメント収集
│   │   │   ├── vectorstore.py # Chroma操作
│   │   │   └── chain.py       # RAGチェーン
│   │   ├── architect/         # 構成案生成機能
│   │   │   ├── graph.py       # LangGraphワークフロー
│   │   │   ├── prompts.py     # プロンプトテンプレート
│   │   │   └── visualizer.py  # Mermaid図生成
│   │   ├── templates/         # テンプレート定義
│   │   └── learning_path/     # 学習パス定義
│   └── utils/
│       └── helpers.py
├── data/
│   └── chroma/                # ベクトルDB永続化
├── tests/                     # バックエンドユニットテスト（115+ tests）
│   ├── test_crawler.py
│   ├── test_vectorstore.py
│   └── test_rag_chain.py
├── e2e/                       # E2Eテスト（Playwright）
├── requirements.txt
├── render.yaml                # Renderデプロイ設定（Frontend + Backend）
└── README.md
```

### Design Principles

1. **Feature-based構造**: 機能ごとにディレクトリを分離し、責務を明確化
2. **単一責任の原則**: 各モジュールは1つの責務のみを持つ
3. **設定の外部化**: 環境変数で設定を管理し、コードと分離
4. **テスタビリティ**: 依存性注入でモック可能な設計

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

## UI/UX Design

### Layout
- **サイドバー**: モード切り替え（学習支援 / 構成案生成）
- **メインエリア**: チャットインターフェース + 出力表示

### Target Users
| ユーザー | ニーズ | 対応方針 |
|---------|-------|---------|
| エンジニア（LangGraph初学者） | 技術的な詳細、コード例 | ソースコード付きの回答 |
| ビジネス担当者 | わかりやすい説明、導入イメージ | 図解 + 平易な言葉での解説 |

### Styling
- Tailwind CSS によるユーティリティファーストのスタイリング
- Refined Brutalist デザインシステム（カスタムCSS変数）
- 統一感のある配色・フォント（IBM Plex Mono, Crimson Pro）
- カード風レイアウトで視認性向上

---

## Development Guidelines

### Code Style
```bash
# フォーマッター
ruff format .

# リンター
ruff check .
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

テスト仕様書
@docs/TEST_SPECIFICATION.md

```bash
# テスト実行
pytest tests/ -v
```
- 主要機能（RAGチェーン、構成案生成）のテストを最低限カバー
- LLM呼び出しはモックを使用

---

## Environment Variables

```bash
# .env.example
OPENAI_API_KEY=your_openai_api_key
CHROMA_PERSIST_DIR=./data/chroma
LOG_LEVEL=INFO
```

---

## Deployment

### Render設定
```yaml
# render.yaml
services:
  # バックエンド（FastAPI）
  - type: web
    name: langgraph-catalyst-api
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: CORS_ORIGINS
        value: https://langgraph-catalyst-frontend.onrender.com

  # フロントエンド（React）
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
- **フロントエンド**: `https://langgraph-catalyst-frontend.onrender.com`
- **バックエンドAPI**: `https://langgraph-catalyst-api.onrender.com`
- **API Docs**: `https://langgraph-catalyst-api.onrender.com/docs`

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

### なぜこのシステムを作るのか
- **差別化**: LangGraphを「使う」だけでなく「教える」システム
- **Biz視点**: 技術だけでなくビジネス価値も説明できる構成案
- **実用性**: 実際に企業のAI導入検討に使えるツール

---

## Milestones

### Phase 1: 基盤構築
- [x] プロジェクト構造のセットアップ
- [x] React + FastAPI フルスタック基盤
- [x] 環境変数・設定管理

### Phase 2: RAG機能
- [ ] ドキュメントクローラー実装
- [ ] Chromaベクトルストア構築
- [ ] RAGチェーン実装

### Phase 3: 構成案生成機能
- [ ] LangGraphワークフロー設計
- [ ] プロンプト設計
- [ ] Mermaid図生成

### Phase 4: UI/UX改善
- [ ] カスタムCSS適用
- [ ] レスポンシブ対応
- [ ] エラーハンドリング

### Phase 5: デプロイ
- [ ] Render設定
- [ ] 本番環境テスト
- [ ] ポートフォリオサイト連携
