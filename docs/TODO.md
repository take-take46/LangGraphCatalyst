# LangGraph Catalyst - 開発実行計画

## プロジェクト概要
LangGraphの学習支援とビジネス活用を促進するポートフォリオシステムの構築

---

## Phase 1: プロジェクト基盤構築 🏗️

### 1.1 プロジェクト構造のセットアップ
- [x] ディレクトリ構造の作成
  - [x] `src/` ディレクトリ作成
  - [x] `src/config/` ディレクトリ作成
  - [x] `src/features/` ディレクトリ作成
  - [x] `src/features/rag/` ディレクトリ作成
  - [x] `src/features/architect/` ディレクトリ作成
  - [x] `src/components/` ディレクトリ作成
  - [x] `src/utils/` ディレクトリ作成
  - [x] `data/chroma/` ディレクトリ作成
  - [x] `tests/` ディレクトリ作成
  - [x] `.streamlit/` ディレクトリ作成

### 1.2 基本ファイルの作成
- [x] `.gitignore` ファイル作成（Python、環境変数、DB等）
- [x] `.env.example` ファイル作成（環境変数テンプレート）
- [x] `requirements.txt` 作成（依存パッケージ定義）
- [x] `README.md` 作成（プロジェクト説明、セットアップ手順）
- [x] `render.yaml` 作成（デプロイ設定）

### 1.3 環境変数・設定管理
- [x] `src/config/__init__.py` 作成
- [x] `src/config/settings.py` 作成
  - [x] 環境変数読み込み（OpenAI API Key、Chroma設定等）
  - [x] Pydantic Settingsを使用した型安全な設定管理
  - [x] ログレベル設定

### 1.4 開発環境のセットアップ
- [x] Ruff設定ファイル作成（`pyproject.toml`または`ruff.toml`）
- [ ] Pre-commit hooks設定（オプション）
- [x] `.env` ファイル作成（gitignore済み）

**完了条件**: プロジェクト構造が整い、依存パッケージがインストール可能で、設定管理が機能する

---

## Phase 2: Streamlit基本UI構築 🎨 ~~（削除済み - React移行完了）~~

> **注**: このフェーズで構築されたStreamlit UIは、Phase 9でReact + FastAPIに完全移行したため削除されました。

### 2.1 エントリーポイントの作成
- [x] ~~`src/app.py` 作成~~ （削除済み）
  - [x] ~~Streamlitページ設定（タイトル、アイコン、レイアウト）~~
  - [x] ~~セッション状態の初期化~~
  - [x] ~~基本的なページ構造（ヘッダー、メインエリア、フッター）~~

### 2.2 サイドバーコンポーネント
- [x] ~~`src/components/__init__.py` 作成~~ （削除済み）
- [x] ~~`src/components/sidebar.py` 作成~~ （削除済み）
  - [x] ~~モード切り替え（RAG学習支援 / 構成案生成）~~
  - [x] ~~設定パネル（モデル選択、温度パラメータ等）~~
  - [x] ~~使い方説明セクション~~

### 2.3 スタイリング
- [x] ~~`.streamlit/config.toml` 作成~~ （削除済み）
  - [x] ~~カラーテーマ設定（プライマリ、セカンダリカラー）~~
  - [x] ~~フォント設定~~
- [x] ~~カスタムCSS実装（`st.markdown`でインジェクション）~~ （削除済み）
  - [x] ~~カード風レイアウト~~
  - [x] ~~ボタンスタイル~~
  - [x] ~~チャットインターフェーススタイル~~

### 2.4 基本的なUIフロー確認
- [x] ~~ローカルで起動確認（`streamlit run src/app.py`）~~ （削除済み）
- [x] ~~モード切り替えの動作確認~~
- [x] ~~レスポンシブ表示の確認~~

**完了条件**: ~~Streamlitアプリが起動し、基本的なUIレイアウトが表示される~~ → **React版に完全移行済み**

---

## Phase 3: RAG学習支援機能の実装 📚

### 3.1 ユーティリティモジュール
- [x] `src/utils/__init__.py` 作成
- [x] `src/utils/helpers.py` 作成
  - [x] テキスト分割ユーティリティ
  - [x] ログ設定ヘルパー
  - [x] エラーハンドリング関数

### 3.2 ドキュメントクローラー
- [x] `src/features/rag/__init__.py` 作成
- [x] `src/features/rag/crawler.py` 作成
  - [x] LangGraph公式ドキュメントのクロール処理
  - [x] LangChain Blogのクロール処理
  - [x] GitHubリポジトリのクロール処理（README、examples等）
  - [x] HTMLパース、テキスト抽出処理
  - [x] メタデータ付与（ソースURL、更新日時等）
  - [x] CLIコマンド実装（`python -m src.features.rag.crawler --update`）

### 3.3 ベクトルストア構築
- [x] `src/features/rag/vectorstore.py` 作成
  - [x] Chromaクライアント初期化
  - [x] ドキュメント埋め込み（OpenAI Embeddings）
  - [x] ベクトルDB保存処理
  - [x] 類似度検索関数
  - [x] コレクション管理（作成、更新、削除）

### 3.4 RAGチェーン実装
- [x] `src/features/rag/chain.py` 作成
  - [x] プロンプトテンプレート作成
    - [x] システムプロンプト（役割定義）
    - [x] 回答フォーマット指示（ソース付き、コード例付き）
  - [x] RAG Chain構築（LangChain）
    - [x] Retriever設定
    - [x] LLM設定（OpenAI）
    - [x] チェーン組み立て
  - [x] ストリーミング対応（オプション）

### 3.5 RAG UI統合
- [x] `src/app.py` にRAGモードUI追加
  - [x] チャット入力フォーム
  - [x] 履歴表示（セッション管理）
  - [x] ソース表示カード
  - [x] コードブロックのシンタックスハイライト

### 3.6 初期データ投入
- [x] クローラー実行でドキュメント収集
- [x] ベクトルDB構築確認
- [x] サンプルクエリでのテスト

**完了条件**: RAG機能が動作し、LangGraphに関する質問に対してソース付きで回答できる

---

## Phase 4: 構成案生成機能の実装 🏛️

### 4.1 プロンプト設計
- [x] `src/features/architect/__init__.py` 作成
- [x] `src/features/architect/prompts.py` 作成
  - [x] ビジネス課題分析用プロンプト
  - [x] LangGraph構成案生成プロンプト
  - [x] Mermaid図生成プロンプト
  - [x] コード例生成プロンプト
  - [x] わかりやすい説明生成プロンプト

### 4.2 LangGraphワークフロー設計
- [x] `src/features/architect/graph.py` 作成
  - [x] ノード定義
    - [x] 課題分析ノード
    - [x] 構成案生成ノード
    - [x] 図生成ノード
    - [x] コード生成ノード
    - [x] 説明生成ノード
  - [x] エッジ定義（ノード間の遷移）
  - [x] 状態管理（StateGraph）
  - [x] グラフコンパイル
  - [x] 実行関数

### 4.3 Mermaid図生成
- [x] `src/features/architect/visualizer.py` 作成
  - [x] Mermaid記法生成関数
  - [x] フローチャート生成
  - [x] グラフ構造の可視化
  - [x] バリデーション処理

### 4.4 構成案生成UI統合
- [x] `src/app.py` に構成案生成モードUI追加
  - [x] ビジネス課題入力フォーム
  - [x] 生成ボタン
  - [x] 結果表示エリア
    - [x] Mermaid図表示（`st.mermaid`またはMarkdown）
    - [x] コード例表示（シンタックスハイライト）
    - [x] 説明表示（カード形式）
  - [x] ダウンロードボタン（結果をMarkdownで出力）

### 4.5 サンプル課題でのテスト
- [x] 「カスタマーサポートの自動化」での生成確認（ユニットテスト済み）
- [x] 「データ分析ワークフロー」での生成確認（UIに実装済み）
- [x] 出力品質の調整（プロンプトチューニング済み）

**完了条件**: ビジネス課題を入力すると、Mermaid図+コード+説明が生成される ✅

---

## Phase 5: テスト・品質向上 🧪

### 5.1 ユニットテスト作成
- [x] `tests/__init__.py` 作成
- [x] `tests/test_core.py` 作成
  - [x] RAGチェーンのテスト（モックLLM使用）
  - [x] ベクトルストアのテスト
  - [x] 構成案生成ワークフローのテスト
  - [x] プロンプト生成のテスト

### 5.2 統合テスト
- [x] エンドツーエンドテスト
  - [x] RAGモードでの質問→回答フロー
  - [x] 構成案生成モードでの入力→出力フロー

### 5.3 エラーハンドリング
- [x] API制限エラーのハンドリング
- [x] ベクトルDB接続エラーのハンドリング
- [x] 入力バリデーション
- [x] ユーザーフレンドリーなエラーメッセージ表示

### 5.4 パフォーマンス最適化
- [x] キャッシング実装（`@st.cache_data`、`@st.cache_resource`）
- [x] レスポンス時間の計測
- [x] ストリーミング最適化

**完了条件**: 主要機能のテストが通り、エラーハンドリングが実装されている ✅

---

## Phase 6: UI/UX改善 ✨

### 6.1 視覚的改善
- [x] ローディングアニメーション追加
- [x] プログレスバー表示
- [x] アイコン・絵文字の適切な配置
- [x] カラースキームの統一

### 6.2 ユーザビリティ向上
- [x] サンプル質問ボタン（RAGモード）
- [x] サンプル課題ボタン（構成案生成モード）
- [x] ヘルプセクション・ツールチップ
- [ ] キーボードショートカット（オプション）

### 6.3 レスポンシブ対応
- [x] モバイル表示の確認・調整
- [x] タブレット表示の確認・調整
- [x] 各種画面サイズでのテスト

### 6.4 アクセシビリティ
- [x] スクリーンリーダー対応
- [x] キーボードナビゲーション
- [x] コントラスト比の確認

**完了条件**: UIが洗練され、ユーザーが直感的に操作できる ✅

---

## Phase 7: デプロイ・公開 🚀

### 7.1 Render設定
- [ ] `render.yaml` の最終調整
  - [ ] ビルドコマンド確認
  - [ ] スタートコマンド確認
  - [ ] 環境変数設定
- [ ] Renderアカウント作成・ログイン
- [ ] GitHubリポジトリ連携

### 7.2 環境変数設定
- [ ] Render管理画面でのシークレット登録
  - [ ] `OPENAI_API_KEY`
  - [ ] その他必要な環境変数

### 7.3 デプロイ実行
- [ ] 初回デプロイ
- [ ] ビルドログ確認
- [ ] デプロイ成功確認

### 7.4 本番環境テスト
- [ ] 全機能の動作確認
  - [ ] RAGモードテスト
  - [ ] 構成案生成モードテスト
- [ ] パフォーマンス確認
- [ ] エラーログ確認

### 7.5 ドキュメント整備
- [ ] README.mdの最終更新
  - [ ] デモURL追加
  - [ ] スクリーンショット追加
  - [ ] セットアップ手順の最終確認
- [ ] ポートフォリオサイトへのリンク追加
- [ ] 技術ブログ記事作成（オプション）

**完了条件**: アプリケーションが本番環境で安定稼働し、公開URL経由でアクセス可能

---

## Phase 8: ポストリリース改善 🔄

### 8.1 モニタリング・ロギング
- [ ] アクセスログ分析
- [ ] エラーログ監視
- [ ] パフォーマンスメトリクス収集

### 8.2 フィードバック対応
- [ ] ユーザーフィードバック収集機能（オプション）
- [ ] バグ修正
- [ ] 機能改善

### 8.3 追加機能検討
- [ ] RAGデータの自動更新機能
- [ ] 生成結果の保存・共有機能
- [ ] マルチモーダル対応（画像入力等）
- [ ] 他LLMプロバイダー対応（Claude、Gemini等）

**完了条件**: 継続的な改善サイクルが確立されている

---

## 開発チェックリスト

### 開発中の品質チェック
- [ ] コードレビュー（自己レビュー）
- [ ] コミットメッセージの規約遵守
- [ ] `ruff format .` 実行
- [ ] `ruff check .` 実行
- [ ] `pytest tests/ -v` 実行
- [ ] セキュリティチェック（API Keyのハードコーディング等）

### デプロイ前チェックリスト
- [ ] 全テスト通過
- [ ] `.env` ファイルが`.gitignore`に含まれている
- [ ] `requirements.txt` が最新
- [ ] ドキュメント（README、CLAUDE.md）が最新
- [ ] ローカルで問題なく動作
- [ ] 不要なコメント・デバッグコードの削除

---

## 推奨開発順序

### Streamlit版（Phase 1-8）
1. **Phase 1 → Phase 2**: 基盤とUIを先に固める
2. **Phase 3**: RAG機能を完成させる（単独で価値がある）
3. **Phase 4**: 構成案生成機能を追加（差別化要素）
4. **Phase 5**: テスト・品質を担保
5. **Phase 6**: UI/UXを洗練
6. **Phase 7**: デプロイして公開
7. **Phase 8**: フィードバックを受けて改善

### React + FastAPI 移行（Phase 9）
8. **Phase 9.1**: バックエンドAPI化（既存ロジックを守りながらAPI化）
9. **Phase 9.2**: React フロントエンド構築（UI層を完全リライト）
10. **Phase 9.3**: 認証・セキュリティ実装
11. **Phase 9.4**: テスト整備（E2E、フロントエンドテスト）
12. **Phase 9.5**: デプロイ構成変更（2サービス体制）
13. **Phase 9.6**: ~~段階的移行（Streamlit版と並行稼働）~~ → **スキップ: Streamlit削除を選択**
14. **Phase 9.7**: ドキュメント整備

**実装方針**: Phase 1-8で構築したStreamlit版は、Phase 9.2完了後に削除し、React版のみで運用する方針に変更しました。

---

## 見積もり工数（参考）

| Phase | 概算工数 | 備考 |
|-------|---------|------|
| Phase 1 | 2-3時間 | 構造整備は比較的簡単 |
| ~~Phase 2~~ | ~~3-4時間~~ | ~~Streamlit基本UIは迅速に構築可能~~ → **削除済み** |
| Phase 3 | 8-10時間 | クローラー+RAG実装がコア |
| Phase 4 | 8-10時間 | LangGraphワークフロー設計が重要 |
| Phase 5 | 4-6時間 | テストとエラーハンドリング |
| Phase 6 | 4-6時間 | UI/UX改善 |
| Phase 7 | 2-3時間 | デプロイ・公開 |
| Phase 8 | 継続的 | 運用・改善 |
| **Phase 9** | **80-130時間** | **React + FastAPI 移行（経験者）** |

**~~Streamlit版合計~~**: ~~約30-40時間（Phase 1-8、実装のみ）~~ → **Phase 2削除により約27-36時間**
**React版移行（Render統一）**: 約78-126時間（Phase 9、経験者）
**プロジェクト全体**: 約108-166時間

**Render統一による削減**: デプロイ設定工数が約2-4時間削減（Vercel+Render比較）

---

## 成功指標

### 技術的指標（~~Streamlit版~~ - 削除済み）
- [x] ~~RAG回答の精度: ソース付き回答が正確~~
- [x] ~~構成案の品質: 実用的なMermaid図+コード~~
- [x] ~~レスポンスタイム: 10秒以内（RAG）、30秒以内（構成案生成）~~
- [x] ~~テストカバレッジ: 主要機能86%以上（達成済み）~~

### 技術的指標（React版 - Phase 9）
- [x] FastAPI が起動し、全エンドポイントが正常動作（Phase 9.1 完了）
- [x] React が起動し、全ページが表示される（Phase 9.2 完了）
- [x] 既存のPythonロジック（115テスト）が全てパス
- [x] フロントエンドテスト: 35件全て通過（Phase 9.4）
- [ ] E2Eテストカバレッジ: 主要フロー70%以上
- [ ] レスポンス時間: 10秒以内（RAG）、30秒以内（構成案生成）
- [ ] モバイル、タブレット、デスクトップ対応
- [ ] Lighthouse スコア: Performance 85+, Accessibility 95+ (Render Static Site基準)

### ビジネス指標
- [ ] ポートフォリオとして説明可能
- [ ] デモ可能な状態で公開
- [ ] 設計思想が明確に説明できる
- [ ] 他プロジェクトへの応用可能性
- [ ] **React版でフルスタック開発力をアピール可能**（Phase 9追加指標）
- [ ] **モダンなUIでユーザー体験が向上**（Phase 9追加指標）

---

## リスクと対策

| リスク | 影響 | 対策 |
|-------|------|------|
| API制限超過 | サービス停止 | エラーハンドリング、レート制限実装 |
| クロール失敗 | RAGデータ不足 | 定期的な手動チェック、フォールバック |
| LLM出力品質 | ユーザー体験低下 | プロンプトチューニング、複数回生成 |
| デプロイエラー | 公開遅延 | ローカル環境で十分テスト |
| コスト超過 | 開発中断 | モデル選択の最適化、キャッシング活用 |
| **React移行時の機能喪失** | **既存機能が動かない** | **既存のPythonロジックを95%再利用、段階的移行、並行稼働** |
| **React移行工数超過** | **開発期間の延長** | **段階的リリース、MVPで最小機能から実装** |
| **フロントエンド/バックエンド通信エラー** | **API連携失敗** | **CORS設定確認、Swagger UIでのAPI検証** |
| **2サービス管理の複雑化** | **運用コスト増** | **Render統一で管理画面一元化、render.yaml自動デプロイ** |
| **デプロイコストの増加** | **予算超過** | **Render無料枠の活用（Web Service: Free, Static Site: Free）** |
| **Renderのコールドスタート** | **初回アクセスが遅い** | **無料プランは15分間アクセスなしでスリープ、有料プラン検討またはウォームアップスクリプト** |

---

---

## Phase 9: React + FastAPI 移行 🚀⚛️

### 概要
Streamlit版の機能を維持したまま、React + FastAPI によるフルスタック構成に移行します。
既存のPythonビジネスロジックは95%再利用し、UI層とAPI層を再構築します。

### 移行戦略
- **既存コードの保護**: `src/features/`, `tests/` は**完全に維持**
- **段階的移行**: バックエンドAPI化 → React構築 → 並行稼働 → 完全移行
- **後方互換性**: Streamlit版を `legacy/` に残して並行運用可能

---

### 9.1 バックエンドAPI化（FastAPI） 🔧

#### 9.1.1 プロジェクト構造の拡張
- [x] バックエンドディレクトリの作成
  - [x] `backend/` ディレクトリ作成
  - [x] `backend/api/` ディレクトリ作成（APIエンドポイント）
  - [x] `backend/api/v1/` ディレクトリ作成（バージョニング）
  - [x] `backend/core/` ディレクトリ作成（設定、セキュリティ）
  - [x] `backend/schemas/` ディレクトリ作成（Pydanticスキーマ）
  - [x] `backend/tests/` ディレクトリ作成（APIテスト）

#### 9.1.2 FastAPI基盤構築
- [x] `backend/main.py` 作成（FastAPIエントリーポイント）
  - [x] FastAPIアプリケーション初期化
  - [x] CORS設定
  - [x] ミドルウェア設定（ロギング、エラーハンドリング）
  - [x] ヘルスチェックエンドポイント（`/health`, `/ready`）
- [x] `backend/core/config.py` 作成（FastAPI設定管理）
  - [x] 環境変数読み込み（既存のsettings.pyを流用）
  - [x] CORS許可オリジン設定
  - [x] API認証設定（JWT秘密鍵等）
- [x] `backend/core/security.py` 作成（セキュリティユーティリティ）
  - [x] JWT生成・検証関数
  - [x] パスワードハッシュ（将来のユーザー認証用）
  - [x] APIキー検証（オプション）

#### 9.1.3 Pydanticスキーマ定義
- [x] `backend/schemas/rag.py` 作成
  - [x] `RAGQueryRequest` スキーマ（question, k, include_sources, include_code_examples）
  - [x] `RAGQueryResponse` スキーマ（answer, sources, code_examples, confidence, metadata）
  - [x] `SourceResponse` スキーマ（title, url, excerpt, relevance, doc_type）
  - [x] `CodeExampleResponse` スキーマ（language, code, description, source_url）
- [x] `backend/schemas/architect.py` 作成
  - [x] `ArchitectRequest` スキーマ（business_challenge, industry, constraints）
  - [x] `ArchitectResponse` スキーマ（challenge_analysis, architecture, code_example, business_explanation, implementation_notes, metadata）
  - [x] `ChallengeAnalysis` スキーマ（summary, key_requirements, suggested_approach, langgraph_fit_reason）
  - [x] `Architecture` スキーマ（mermaid_diagram, node_descriptions, edge_descriptions, state_schema）
  - [x] `NodeDescription` スキーマ（node_id, name, purpose, description, inputs, outputs）
  - [x] `EdgeDescription` スキーマ（from_node, to_node, condition, description）
- [x] `backend/schemas/common.py` 作成
  - [x] 共通レスポンス型（`SuccessResponse`, `ErrorResponse`）
  - [x] ページネーション型（将来拡張用）
- [x] `backend/schemas/learning_path.py` 作成
  - [x] `TopicResponse` スキーマ（学習トピック）
  - [x] `LearningPathResponse` スキーマ（学習パス全体）
  - [x] `ProgressRequest`/`ProgressResponse` スキーマ（進捗管理）
- [x] `backend/schemas/templates.py` 作成
  - [x] `TemplateResponse` スキーマ（テンプレート）
  - [x] `TemplatesListResponse` スキーマ（テンプレート一覧）
  - [x] `TemplateCategoriesResponse` スキーマ（カテゴリ一覧）

#### 9.1.4 APIエンドポイント実装
- [x] `backend/api/v1/rag.py` 作成
  - [x] `POST /api/v1/rag/query` エンドポイント
    - [x] リクエストバリデーション
    - [x] 既存の `RAGChain.query()` を呼び出し（**そのまま流用**）
    - [x] レスポンスのシリアライズ
    - [x] エラーハンドリング（VectorStoreError, LLMError等）
  - [x] `GET /api/v1/rag/health` エンドポイント（VectorStore接続確認）
- [x] `backend/api/v1/architect.py` 作成
  - [x] `POST /api/v1/architect/generate` エンドポイント
    - [x] リクエストバリデーション
    - [x] 既存の `ArchitectGraph.generate_architecture()` を呼び出し（**そのまま流用**）
    - [x] レスポンスのシリアライズ
    - [x] エラーハンドリング（ValidationError, LLMError等）
- [x] `backend/api/v1/learning_path.py` 作成
  - [x] `GET /api/v1/learning-path` エンドポイント（学習パスデータ取得）
  - [x] `GET /api/v1/learning-path/level/{level}` エンドポイント（レベル別取得）
  - [x] `GET /api/v1/learning-path/topic/{topic_id}` エンドポイント（個別トピック取得）
  - [x] `POST /api/v1/learning-path/progress` エンドポイント（進捗計算）
- [x] `backend/api/v1/templates.py` 作成
  - [x] `GET /api/v1/templates` エンドポイント（テンプレート一覧取得、フィルタリング対応）
  - [x] `GET /api/v1/templates/categories` エンドポイント（カテゴリ一覧取得）
  - [x] `GET /api/v1/templates/{template_id}` エンドポイント（個別取得）

#### 9.1.5 APIルーター統合
- [x] `backend/api/v1/__init__.py` 作成
  - [x] 全エンドポイントのルーター統合
  - [x] `/api/v1` プレフィックス設定
  - [x] RAG、Architect、Learning Path、Templatesルーター登録
- [x] `backend/main.py` にルーター登録
  - [x] APIドキュメント自動生成（`/docs`, `/redoc`）

#### 9.1.6 APIテスト実装
- [x] `backend/tests/test_api_rag.py` 作成
  - [x] `POST /api/v1/rag/query` のテスト
  - [x] リクエストバリデーションのテスト
  - [x] エラーレスポンスのテスト
  - [x] モック化（既存のPythonロジックはモック）
- [x] `backend/tests/test_api_architect.py` 作成
  - [x] `POST /api/v1/architect/generate` のテスト
  - [x] リクエストバリデーションのテスト
  - [x] エラーレスポンスのテスト
- [x] `backend/tests/conftest.py` 作成
  - [x] FastAPIテストクライアント設定
  - [x] フィクスチャ定義

#### 9.1.7 API実行・動作確認
- [x] ローカルでFastAPI起動（`uvicorn backend.main:app --reload`）
- [x] `/docs` でSwagger UI確認
- [x] Postman/HTTPieでエンドポイントテスト
- [x] 既存のPythonロジックが正常に動作することを確認

**完了条件**: FastAPI が起動し、全エンドポイントが正常に動作し、既存のPythonロジックを呼び出せる

---

### 9.2 React フロントエンド構築 ⚛️ ✅ 完了 (2026-01-28)

#### 9.2.1 プロジェクトセットアップ
- [x] フロントエンドディレクトリの作成
  - [x] `frontend/` ディレクトリ作成
  - [x] Vite + React + TypeScript プロジェクト初期化
  - [x] 依存パッケージインストール
    - [x] `npm install react-router-dom` （ルーティング）
    - [x] `npm install axios` （HTTP通信）
    - [x] `npm install zustand` （状態管理）
    - [x] `npm install @tailwindcss/typography` （Markdown/コード表示）
    - [x] `npm install react-markdown` （Markdown表示）
    - [x] `npm install react-syntax-highlighter` （コードハイライト）
    - [x] `npm install mermaid` （Mermaid図表示）
  - [x] TailwindCSS セットアップ（手動設定）

#### 9.2.2 プロジェクト構造の作成
- [x] `frontend/src/` ディレクトリ構造
  - [x] `src/components/` （再利用可能なUIコンポーネント）
  - [x] `src/pages/` （ページコンポーネント）
  - [x] `src/api/` （API通信ロジック）
  - [x] `src/store/` （状態管理）
  - [x] `src/types/` （TypeScript型定義）

#### 9.2.3 型定義
- [x] `src/types/index.ts` 作成（統合型定義ファイル）
  - [x] `RAGQueryRequest/Response` インターフェース
  - [x] `Source`, `CodeExample` インターフェース
  - [x] `ArchitectRequest/Response` インターフェース
  - [x] `ChallengeAnalysis`, `Architecture` インターフェース
  - [x] `NodeDescription`, `EdgeDescription` インターフェース
  - [x] `Topic`, `Template` インターフェース

#### 9.2.4 API通信層
- [x] `src/api/client.ts` 作成
  - [x] Axios インスタンス作成（ベースURL、タイムアウト設定）
  - [x] リクエストインターセプター（認証トークン追加等）
  - [x] レスポンスインターセプター（エラーハンドリング）
- [x] 環境変数ファイル作成
  - [x] `frontend/.env.local` （ローカル開発用）
- [x] `src/api/rag.ts` 作成
  - [x] `queryRAG`, `checkRAGHealth` 関数
- [x] `src/api/architect.ts` 作成
  - [x] `generateArchitecture` 関数
- [x] `src/api/learningPath.ts` 作成
  - [x] `getLearningPath`, `getLearningPathByLevel`, `getTopic`, `calculateProgress` 関数
- [x] `src/api/templates.ts` 作成
  - [x] `getTemplates`, `getCategories`, `getTemplate` 関数

#### 9.2.5 状態管理（Zustand）
- [x] `src/store/ragStore.ts` 作成
  - [x] チャット履歴管理
  - [x] 質問・回答の状態管理
  - [x] ローディング状態
- [x] `src/store/architectStore.ts` 作成
  - [x] 構成案生成結果の管理
  - [x] 課題入力の状態管理
- [x] `src/store/learningStore.ts` 作成（永続化対応）
  - [x] 学習進捗管理（completedTopics）
  - [x] localStorage永続化

#### 9.2.6 共通UIコンポーネント
- [x] `src/components/Layout/` ディレクトリ作成
  - [x] `Header.tsx` （ヘッダーコンポーネント）
- [x] `src/components/UI/` ディレクトリ作成
  - [x] `Button.tsx` （ボタンコンポーネント）
  - [x] `Card.tsx` （カードコンポーネント）
- [x] `src/components/CodeBlock/` ディレクトリ作成
  - [x] `CodeBlock.tsx` （シンタックスハイライト付きコードブロック）
- [x] `src/components/Markdown/` ディレクトリ作成
  - [x] `MarkdownRenderer.tsx` （Markdown表示）
- [x] `src/components/Mermaid/` ディレクトリ作成
  - [x] `MermaidDiagram.tsx` （Mermaid図表示）

#### 9.2.7-9.2.10 ページコンポーネント（統合実装）
- [x] `src/pages/HomePage.tsx` （ホームページ）
- [x] `src/pages/RAGPage.tsx` （RAG学習支援ページ - 完全統合実装）
- [x] `src/pages/ArchitectPage.tsx` （構成案生成ページ - 完全統合実装）
- [x] `src/pages/LearningPathPage.tsx` （学習パスページ - 完全統合実装）
- [x] `src/pages/TemplatesPage.tsx` （テンプレートページ - 完全統合実装）
- **注**: 各ページは機能を統合実装しており、`src/features/` サブディレクトリは不要

#### 9.2.11 ルーティング
- [x] `src/App.tsx` 修正
  - [x] React Router セットアップ
  - [x] ルート定義（/, /rag, /learning-path, /templates, /architect）
  - [x] レイアウトコンポーネント適用

#### 9.2.12 スタイリング
- [x] Tailwind CSS設定
  - [x] `tailwind.config.js` カスタマイズ（Refined Brutalist デザインシステム）
  - [x] ダークモード対応
- [x] グローバルCSS
  - [x] `src/index.css` 作成（カスタムCSS変数、カード、アニメーション）
  - [x] カスタムフォント読み込み（IBM Plex Mono, Crimson Pro）
  - [x] リセットCSS
- [x] アニメーション
  - [x] ページ遷移アニメーション（カスタムCSS）
  - [x] ローディングアニメーション
  - [x] ホバー・フォーカスエフェクト

#### 9.2.13 ローカル実行・動作確認
- [x] `npm run dev` でReactアプリ起動（http://localhost:5173/）
- [x] TypeScript コンパイルエラーなし
- [x] Vite 開発サーバー正常起動
- [x] 全ページ（Home, RAG, LearningPath, Templates, Architect）が正常表示
- [x] レベル/難易度キーを日本語に統一（'初級', '中級', '上級'）
- [x] フッター削除

**完了条件**: ✅ React フロントエンドが起動し、全ページが正常に動作

---

### 9.3 認証・セキュリティ実装 🔐

**実装方針**:
- ユーザー管理: 環境変数ベース（DB不使用）
- 対象ユーザー: 開発者1名 + テストユーザー3名 = 合計4名
- 使用制限: テストユーザーは1日5回まで（開発者は無制限）
- 永続化: ファイルベース（Render無料プランを想定、再起動でリセット）

#### 9.3.1 バックエンド認証基盤
- [x] ユーザー管理設定
  - [x] `backend/core/users.py` 作成
    - [x] 4ユーザーの定義（username, role, daily_limit）
    - [x] 環境変数からパスワードを読み込み、bcryptハッシュ化
    - [x] ユーザー検証関数（`authenticate_user`, `get_user`）
  - [x] 環境変数設定
    - [x] `ADMIN_PASSWORD`: 開発者パスワード
    - [x] `TESTUSER1_PASSWORD`, `TESTUSER2_PASSWORD`, `TESTUSER3_PASSWORD`
    - [x] `JWT_SECRET_KEY`: JWT署名用秘密鍵
    - [x] `JWT_ALGORITHM`: デフォルト "HS256"
    - [x] `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: 1440分（24時間）

- [x] JWT認証実装
  - [x] `backend/core/security.py` 更新
    - [x] `create_access_token()`: JWT生成関数
    - [x] `verify_token()`: JWT検証関数
  - [x] `backend/schemas/auth.py` 作成
    - [x] `LoginRequest`: FormData形式
    - [x] `LoginResponse`: { access_token, token_type, user: UserResponse }
    - [x] `UserResponse`: { username, role, daily_limit }
    - [x] `TokenData`: { username, role }

- [x] 認証エンドポイント
  - [x] `backend/api/v1/auth.py` 作成
    - [x] `POST /api/v1/auth/login`: ログイン
      - [x] ユーザー名・パスワード検証
      - [x] JWT発行
      - [x] エラーハンドリング（401 Unauthorized）
    - [x] `GET /api/v1/auth/me`: 現在のユーザー情報取得
      - [x] JWT検証
      - [x] ユーザー情報返却
    - [x] `POST /api/v1/auth/logout`: ログアウト（トークン無効化は不要、フロントエンドで削除）

- [x] 使用制限機能
  - [x] `backend/core/usage_limiter.py` 作成
    - [x] `data/usage_limits.json` でカウント管理
    - [x] `check_usage_limit(user)`: 制限チェック
    - [x] `increment_usage(user)`: 使用回数インクリメント
    - [x] `get_remaining_usage(user)`: 残り回数取得
    - [x] 日付変更時の自動リセット
  - [x] 使用制限ミドルウェア
    - [x] `backend/core/dependencies.py` 更新
    - [x] `require_usage_limit()`: 依存性注入用
    - [x] 制限超過時は 429 Too Many Requests エラー

- [x] 保護されたエンドポイント
  - [x] RAG、Architect エンドポイントに認証を追加
    - [x] `UserWithUsageLimit` 型アノテーションを使用
    - [x] 認証 + 使用制限を同時に適用
  - [x] Learning Path、Templates は認証不要（読み取りのみ）

#### 9.3.2 フロントエンド認証
- [x] 状態管理（Zustand）
  - [x] `src/store/authStore.ts` 作成
    - [x] ユーザー情報（username, role）
    - [x] トークン管理（localStorage）
    - [x] `login(username, password)`: ログイン処理
    - [x] `logout()`: ログアウト処理
    - [x] `isAuthenticated()`: 認証状態チェック
    - [x] `isAdmin()`: 管理者判定
    - [x] 永続化（persist middleware）

- [x] API通信層更新
  - [x] `src/api/client.ts` 更新
    - [x] リクエストインターセプター: トークンをAuthorizationヘッダーに追加
    - [x] レスポンスインターセプター: 401エラー時に自動ログアウト
  - [x] `src/api/auth.ts` 作成
    - [x] `login(username, password)`: ログインAPI（FormData形式）
    - [x] `getMe()`: 現在のユーザー情報取得
    - [x] `logout()`: ログアウト

- [x] 認証フロー
  - [x] `src/pages/LoginPage.tsx` 作成
    - [x] ログインフォーム（username, password）
    - [x] エラー表示（認証失敗、ネットワークエラー）
    - [x] ログイン成功後に元のページへリダイレクト
  - [x] `src/components/ProtectedRoute.tsx` 作成
    - [x] 認証チェック
    - [x] 未認証時は `/login` へリダイレクト
    - [x] リダイレクト元のパスを保存（ログイン後に戻る）
  - [x] `src/App.tsx` 更新
    - [x] `/login` ルート追加
    - [x] RAG、Architect ページを ProtectedRoute でラップ

- [x] 使用制限UI
  - [x] `src/components/UsageLimitBadge.tsx` 作成
    - [x] ヘッダーに残り使用回数を表示（テストユーザーのみ）
    - [x] 「残り3回」などの表示
    - [x] 制限超過時の警告
  - [x] `src/api/usage.ts` 作成
    - [x] `getRemainingUsage()`: 残り回数取得API
  - [x] エラーハンドリング
    - [x] 429 Too Many Requests エラー時に専用メッセージ表示
    - [x] 「本日の使用回数上限に達しました」

- [x] ヘッダー更新
  - [x] `src/components/Layout/Header.tsx` 更新
    - [x] ログイン状態の表示
    - [x] ユーザー名表示
    - [x] ログアウトボタン
    - [x] UsageLimitBadge の統合

#### 9.3.3 セキュリティ対策
- [x] バックエンドセキュリティ
  - [x] CORS設定の確認（既存）
  - [x] パスワードのbcryptハッシュ化（bcrypt 4.2.0で動作確認）
  - [x] JWT有効期限設定（24時間 = 1440分）
  - [x] 環境変数の保護確認（.env.example作成、.gitignore更新）
  - [x] 入力バリデーション強化（Pydanticスキーマで自動）
  - [ ] レート制限（slowapi等、オプション）

- [x] フロントエンドセキュリティ
  - [x] XSS対策（React自動）
  - [x] トークンの安全な保存（localStorage + persist middleware）
  - [x] CSRF対策（不要、JWTトークン方式のため）
  - [x] 環境変数の保護（`.env.local`作成済み）

- [ ] Render デプロイ時のセキュリティ（Phase 9.5で実施）
  - [ ] 環境変数をRender Dashboardで設定（パスワード、JWT秘密鍵）
  - [ ] HTTPS強制（Render自動）
  - [ ] シークレット情報のGitコミット防止確認

**完了条件**: ✅ **完了** - 4ユーザーでログイン可能、テストユーザーは1日5回制限、開発者は無制限、全エンドポイントが保護されている（Renderデプロイ時のセキュリティ設定を除く）

---

### 9.4 テスト整備 🧪

#### 9.4.1 バックエンドテスト ✅ **完了**
- [x] 既存のユニットテスト（120件）が全てパスすることを確認
- [x] APIエンドポイントのテスト追加（4ファイル実装済み）
  - [x] レスポンススキーマのバリデーション
  - [x] エラーレスポンスのテスト
  - [x] 認証テスト
- [x] 統合テスト
  - [x] FastAPI + Pythonロジックのエンドツーエンドテスト

#### 9.4.2 フロントエンドテスト 🔄 **部分完了**
- [x] ユニットテスト（Vitest）
  - [x] `vitest` インストール
  - [x] コンポーネントテスト（React Testing Library）- [x] 35件のテスト実装・通過
    - [x] Button.test.tsx
    - [x] Card.test.tsx
    - [x] RAGPage.test.tsx
    - [x] ArchitectPage.test.tsx
- [ ] E2Eテスト（Playwright）
  - [x] `playwright` インストール済み
  - [ ] `playwright.config.ts` 作成
  - [ ] 主要フローのテスト実装
    - [ ] RAG質問→回答フロー
    - [ ] 構成案生成フロー
    - [ ] 学習パス進捗保存フロー
    - [ ] ログイン→保護ページアクセスフロー
- [ ] テストカバレッジ目標: 70%以上（測定未実施）

**完了条件**: ~~全テストがパスし、主要機能のE2Eテストが実装されている~~ → **部分完了: ユニットテスト155件通過（バックエンド120件 + フロントエンド35件）、E2Eテスト未実装**

---

### 9.5 デプロイ構成変更（Render統一） 🌐

#### 9.5.1 Render統一デプロイ設定
- [ ] `render.yaml` ファイル作成（モノレポ対応）
  - [ ] バックエンド（Web Service）設定
  - [ ] フロントエンド（Static Site）設定
  - [ ] 環境変数の定義
  - [ ] CORS設定（フロントエンドURL指定）

**render.yaml 完全版:**
```yaml
services:
  # バックエンド（FastAPI）
  - type: web
    name: langgraph-catalyst-api
    runtime: python
    region: oregon  # または singapore（アジアに近い場合）
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: OPENAI_API_KEY
        sync: false  # 手動設定（シークレット）※Render Dashboard で設定
      - key: CHROMA_PERSIST_DIR
        value: ./data/chroma
      - key: CORS_ORIGINS
        value: https://langgraph-catalyst-frontend.onrender.com,http://localhost:5173
      - key: JWT_SECRET_KEY
        sync: false  # 手動設定（認証使用時）※Render Dashboard で設定
      - key: LOG_LEVEL
        value: INFO
      - key: ENVIRONMENT
        value: production
    # オプション: 永続ディスク（Chromaデータ保存用）
    # disk:
    #   name: chroma-data
    #   mountPath: /data/chroma
    #   sizeGB: 1

  # フロントエンド（React Static Site）
  - type: web
    name: langgraph-catalyst-frontend
    runtime: static
    region: oregon
    plan: free
    buildCommand: cd frontend && npm ci && npm run build
    staticPublishPath: ./frontend/dist
    pullRequestPreviewsEnabled: true  # PRプレビュー（オプション）
    envVars:
      - key: VITE_API_BASE_URL
        value: https://langgraph-catalyst-api.onrender.com/api/v1
    headers:
      - path: /*
        name: Cache-Control
        value: public, max-age=0, must-revalidate  # HTML
      - path: /assets/*
        name: Cache-Control
        value: public, max-age=31536000, immutable  # 静的アセット（JS, CSS等）
    routes:
      - type: rewrite
        source: /*
        destination: /index.html  # SPAルーティング対応
```

**重要な注意事項:**
- `OPENAI_API_KEY` と `JWT_SECRET_KEY` は `sync: false` なので、Render Dashboardで手動設定が必要
- `region: oregon` はUS West、アジアからのアクセスなら `singapore` も検討
- `npm ci` は `npm install` より高速・安定（CI/CD推奨）
- キャッシュヘッダーで静的アセットの配信を最適化

#### 9.5.2 バックエンド設定
- [ ] 環境変数設定（Render Dashboard）
  - [ ] `OPENAI_API_KEY` （手動入力、シークレット）
  - [ ] `CHROMA_PERSIST_DIR` （`./data/chroma`）
  - [ ] `CORS_ORIGINS` （フロントエンドURL: `https://langgraph-catalyst-frontend.onrender.com`）
  - [ ] `JWT_SECRET_KEY` （認証使用時、ランダム生成）
  - [ ] `LOG_LEVEL` （`INFO`）
- [ ] Disk永続化設定（オプション）
  - [ ] Chromaデータの永続化が必要な場合、Render Disks設定
  - [ ] マウントパス: `/data/chroma`
- [ ] ヘルスチェックパス設定
  - [ ] `/health` または `/api/v1/health`
- [ ] デプロイ実行・動作確認
  - [ ] Swagger UI（`https://langgraph-catalyst-api.onrender.com/docs`）確認
  - [ ] ヘルスチェック確認

#### 9.5.3 フロントエンド設定
- [ ] ビルド設定確認
  - [ ] `vite.config.ts` の本番設定
    ```typescript
    export default defineConfig({
      base: '/',
      build: {
        outDir: 'dist',
        sourcemap: false,
        rollupOptions: {
          output: {
            manualChunks: {
              vendor: ['react', 'react-dom', 'react-router-dom'],
            },
          },
        },
      },
    })
    ```
  - [ ] 環境変数設定（`VITE_API_BASE_URL`）
- [ ] SPAルーティング設定
  - [ ] Rewrite Rules: `/*` → `/index.html` （render.yamlで設定済み）
- [ ] デプロイ実行・動作確認
  - [ ] フロントエンドURL（`https://langgraph-catalyst-frontend.onrender.com`）確認
  - [ ] API通信確認（CORS設定が正しいか）
  - [ ] 全ページの表示確認

#### 9.5.4 GitHubリポジトリ連携
- [ ] Renderアカウント作成・ログイン
- [ ] GitHubリポジトリ連携
- [ ] 自動デプロイ設定
  - [ ] mainブランチへのpush時に自動デプロイ
  - [ ] プルリクエストプレビュー（オプション、有料プラン）
- [ ] ビルド通知設定（Slack, Email等）

#### 9.5.5 CORS設定の確認
- [ ] バックエンド（FastAPI）のCORS設定
  ```python
  # backend/main.py
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=[
          "https://langgraph-catalyst-frontend.onrender.com",
          "http://localhost:5173",  # ローカル開発用
      ],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- [ ] 環境変数で動的に設定
  ```python
  origins = settings.cors_origins.split(",")
  ```
- [ ] ブラウザDevToolsでCORSエラーがないか確認

#### 9.5.6 カスタムドメイン設定（オプション）
- [ ] ドメイン取得（Google Domains, Cloudflare, Namecheap等）
- [ ] フロントエンド: カスタムドメイン設定
  - [ ] Render Dashboard → Settings → Custom Domain
  - [ ] 例: `app.yourdomain.com`
  - [ ] DNS設定（CNAMEレコード追加）
- [ ] バックエンド: サブドメイン設定
  - [ ] 例: `api.yourdomain.com`
  - [ ] DNS設定（CNAMEレコード追加）
- [ ] SSL証明書の自動設定確認（Renderが自動発行）
- [ ] CORS設定の更新（カスタムドメインを追加）

#### 9.5.7 パフォーマンス最適化
- [ ] フロントエンドビルド最適化
  - [ ] コード分割（Code Splitting）
  - [ ] Tree Shaking確認
  - [ ] 画像最適化（WebP変換、遅延ロード）
  - [ ] バンドルサイズ分析（`npm run build -- --mode analyze`）
- [ ] キャッシング設定
  - [ ] Static Assetsのキャッシュヘッダー設定
  - [ ] `Cache-Control` ヘッダー確認
- [ ] Lighthouse監査
  - [ ] Performance: 90+目標
  - [ ] Accessibility: 95+目標
  - [ ] Best Practices: 95+目標
  - [ ] SEO: 90+目標

**完了条件**: フロントエンドとバックエンドが両方Renderにデプロイされ、正常に通信でき、Render管理画面で一元管理できる

---

### 9.6 段階的移行・並行稼働 🔄 ~~（スキップ - 直接削除を選択）~~

> **実装方針変更**: Streamlit版を保護せず、React版のみを使用する方針としたため、Phase 9.6はスキップして直接削除を実施しました。

#### 9.6.1 Streamlit版の保護 ~~（スキップ）~~
- [x] ~~Streamlit版を `legacy/` ディレクトリに移動~~ → **スキップ: 直接削除を選択**
- [x] Streamlit専用ファイルの削除（Phase 1完了）
  - [x] `src/app.py` 削除
  - [x] `src/components/sidebar.py` 削除
  - [x] `src/components/` ディレクトリ削除
  - [x] `.streamlit/` ディレクトリ削除
  - [x] `scripts/run.sh` 削除
  - [x] `scripts/pre-deploy.sh` 削除
- [x] `requirements.txt` からstreamlit削除（Phase 2完了）
- [x] ドキュメント更新（Phase 4実施中）
  - [x] README.md 更新
  - [x] CLAUDE.md 更新
  - [x] .claude/CLAUDE.md 更新
  - [ ] docs/TODO.md 更新（本ファイル）

#### 9.6.2 並行稼働期間 ~~（スキップ）~~
- [x] ~~Streamlit版とReact版を同時に稼働~~ → **React版のみを使用**
- [x] React版の安定性確認済み（フロントエンドテスト35件全て通過）

#### 9.6.3 完全移行
- [x] React版の安定性確認済み
- [x] Streamlit版の削除完了（非推奨化ではなく完全削除）
- [x] ドキュメント更新（README.md, CLAUDE.md, .claude/CLAUDE.md完了、docs/TODO.md実施中）
- [ ] ポートフォリオサイトのURL更新

**完了条件**: ~~React版が安定稼働し、Streamlit版からの移行が完了~~ → **React版のみで稼働、Streamlit関連ファイル完全削除済み**

---

### 9.7 ドキュメント整備 📝

#### 9.7.1 README更新
- [ ] プロジェクト構成の説明（モノレポ構成）
- [ ] ローカル開発手順
  - [ ] バックエンド起動方法（`uvicorn backend.main:app --reload`）
  - [ ] フロントエンド起動方法（`cd frontend && npm run dev`）
- [ ] デプロイURL更新
  - [ ] フロントエンド: `https://langgraph-catalyst-frontend.onrender.com`
  - [ ] バックエンド: `https://langgraph-catalyst-api.onrender.com`
  - [ ] API Docs: `https://langgraph-catalyst-api.onrender.com/docs`
- [ ] スクリーンショット更新（React版）
- [ ] 技術スタック更新
  - [ ] **フロントエンド**: React + TypeScript + Vite + Tailwind CSS + Zustand
  - [ ] **バックエンド**: FastAPI + LangChain + LangGraph + Chroma
  - [ ] **インフラ**: Render（フロントエンド + バックエンド統一）
  - [ ] **デプロイ**: render.yaml（Infrastructure as Code）

#### 9.7.2 API仕様書更新
- [ ] `docs/API_SPECIFICATION.md` 更新
  - [ ] OpenAPI/Swagger仕様の追加
  - [ ] エンドポイント一覧の更新
  - [ ] リクエスト/レスポンス例の追加

#### 9.7.3 開発ガイド作成
- [ ] `docs/DEVELOPMENT_GUIDE.md` 作成
  - [ ] ローカル開発環境セットアップ
  - [ ] コーディング規約
  - [ ] テスト実行方法
  - [ ] デプロイ手順

**完了条件**: ドキュメントが最新化され、新規開発者がセットアップできる

---

## 移行工数見積もり（Phase 9）

| サブフェーズ | 概算工数 | 備考 |
|------------|---------|------|
| 9.1 バックエンドAPI化 | ✅ 10-15時間 | 既存ロジック95%再利用、FastAPI基盤構築 |
| 9.2 React フロントエンド構築 | ✅ 40-60時間 | UI完全リライト、コンポーネント設計 |
| 9.3 認証・セキュリティ | ✅ 8-12時間 | 環境変数ベースユーザー管理、JWT実装、使用制限機能 |
| 9.3.1 バックエンド認証基盤 | ✅ 4-6時間 | ユーザー管理、JWT、使用制限ミドルウェア |
| 9.3.2 フロントエンド認証 | ✅ 3-5時間 | authStore、LoginPage、ProtectedRoute |
| 9.3.3 セキュリティ対策 | ✅ 1-1時間 | bcrypt、環境変数保護、レート制限 |
| 9.4 テスト整備 | 🔄 5-7時間 | ユニットテスト完了（155件）、E2Eテスト未実装 |
| 9.5 デプロイ構成変更（Render統一） | 3-6時間 | render.yaml設定、環境変数設定、CORS設定 |
| 9.6 段階的移行 | ✅ スキップ | Streamlit削除を選択（Phase 4完了） |
| 9.7 ドキュメント整備 | 🔄 2-5時間 | README/CLAUDE.md完了、API仕様書等が残り |

**完了済み**: Phase 9.1（10-15時間）、Phase 9.2（40-60時間）、Phase 9.3（8-12時間）、Phase 9.6（スキップ）
**残り工数（経験者）**: 10-18時間（E2Eテスト3-5時間 + デプロイ3-6時間 + ドキュメント2-5時間 + バッファ2時間）
**プロジェクト全体（経験者）**: 81-133時間

**Render統一のメリット**:
- デプロイ設定がシンプル化（1つのrender.yamlで完結）
- 管理画面が統一され、学習コストが低減
- 9.5の工数が約30%削減（5-10時間 → 3-6時間）

---

## Phase 9 成功指標

### 技術的指標
- [x] FastAPI が起動し、全エンドポイントが正常動作（Phase 9.1 完了）
- [x] React が起動し、全ページが表示される（Phase 9.2 完了）
- [x] 既存のPythonロジック（120テスト）が全てパス
- [x] 4ユーザーでログイン可能、認証フローが正常動作（Phase 9.3 完了）
- [x] テストユーザーは1日5回制限、開発者は無制限（Phase 9.3 完了）
- [x] フロントエンドユニットテスト: 35件全て通過（Phase 9.4 完了）
- [x] バックエンドユニットテスト: 120件通過（Phase 9.4 完了）
- [ ] E2Eテストカバレッジ: 主要フロー70%以上（Phase 9.4 未完了）
- [ ] レスポンス時間: 10秒以内（RAG）、30秒以内（構成案生成）
- [ ] モバイル、タブレット、デスクトップ対応
- [ ] **Render統一デプロイ**: 1つのrender.yamlで両サービスが稼働
- [ ] **CORS設定正常**: フロントエンド⇔バックエンド通信エラーなし
- [ ] Lighthouse スコア: Performance 85+, Accessibility 95+ (Render Static Site基準)

### ビジネス指標
- [ ] React版が本番環境で安定稼働（Phase 9.5で実施）
- [x] ~~Streamlit版と同等の機能を提供~~ → **Streamlit削除、React版のみで運用**
- [x] UIがモダンで洗練されている（Refined Brutalistデザイン実装済み）
- [x] ポートフォリオとして「フルスタック力」をアピール可能（React + FastAPI実装済み）
- [ ] **インフラ管理のシンプルさ**: Render管理画面で一元管理できる（Phase 9.5で実施）

---

## 次のステップ

### 完了済み ✅
1. ~~**Phase 9.1**: FastAPIバックエンド構築~~ ✅
2. ~~**Phase 9.2**: React フロントエンド構築~~ ✅
3. ~~**Phase 9.3**: 認証・セキュリティ実装~~ ✅
4. ~~**Phase 9.4（部分）**: ユニットテスト整備（155件通過）~~ ✅
5. ~~**Phase 9.6**: Streamlit削除~~ ✅

### 残りタスク 🎯
1. **Phase 9.4（残り）**: E2Eテスト実装（Playwright）
   - playwright.config.ts 作成
   - 主要フローのE2Eテスト実装
   - カバレッジ測定

2. **Phase 9.5**: Renderデプロイ
   - render.yaml 最終調整
   - 環境変数設定（Render Dashboard）
   - デプロイ実行・動作確認

3. **Phase 9.7（残り）**: ドキュメント整備
   - API仕様書更新
   - テスト仕様書更新

---

このドキュメントは開発の進捗に合わせて随時更新してください。
各チェックボックスを完了時にチェック `[x]` にすることで進捗を可視化できます。
