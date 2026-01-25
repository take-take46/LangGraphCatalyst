# LangGraph Catalyst - テスト仕様書

## 目次
- [概要](#概要)
- [テスト戦略](#テスト戦略)
- [テスト環境](#テスト環境)
- [ユニットテスト](#ユニットテスト)
- [統合テスト](#統合テスト)
- [テスト実行](#テスト実行)
- [カバレッジ](#カバレッジ)

---

## 概要

### 目的
LangGraph Catalystの品質を保証し、各機能が仕様通りに動作することを検証します。

### スコープ
- **対象**: RAG学習支援機能、構成案生成機能、UI/UX
- **範囲**: ユニットテスト、統合テスト、E2Eテスト

### テスト実装状況

**バージョン**: 3.0.0 | **最終更新**: 2026-01-25

| 項目 | 値 |
|------|-----|
| **総テスト数** | 115+ (ユニット) + 3 (統合) |
| **コードカバレッジ** | 27.21% (全体) / 86%+ (コア機能) |
| **テストファイル数** | 12 ファイル |
| **モック戦略** | 外部API呼び出しを100%モック化 |

---

## テスト戦略

### テストピラミッド
```
        ┌─────┐
       │ E2E │ 10%
      ├───────┤
     │  統合  │ 30%
    ├─────────┤
   │ ユニット │ 60%
  └───────────┘
```

### 基本方針
- **自動化率**: 主要機能の80%以上を自動テストでカバー
- **モック戦略**: OpenAI API、Webクロール等の外部依存はすべてモック化
- **テストデータ**: 本番データは使用せず、テスト用データを用意
- **CI/CD統合**: GitHub Actionsで自動実行

---

## テスト環境

### 環境構成

| 環境 | 用途 | 特徴 |
|------|------|------|
| **Local** | 開発中のテスト | 開発者のローカルマシン |
| **CI** | 自動テスト | GitHub Actions |
| **Staging** | 統合テスト | 本番相当の環境 |

### 必要な環境変数

```bash
# .env.test
OPENAI_API_KEY=sk-test-mock-key
CHROMA_PERSIST_DIR=./tests/data/chroma_test
LOG_LEVEL=DEBUG
ENVIRONMENT=test
```

---

## ユニットテスト

### 1. RAG機能 (53 tests)

#### 1.1 ドキュメントクローラー (`tests/test_crawler.py`) - 20 tests

**目的**: 外部ドキュメントソースからのクロール処理を検証。すべてのHTTPリクエストはモック化。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **公式ドキュメントクロール** | 5 | 正常クロール、ページ数制限、ネットワークエラー、404エラー、メタデータ抽出 |
| **ブログクロール** | 2 | ブログ記事取得、タグフィルタリング |
| **GitHubクロール** | 2 | リポジトリ取得、examples含む取得 |
| **全ソース更新** | 3 | 成功、部分的失敗、完全失敗 |
| **HTMLパース** | 2 | 不正HTML処理、空コンテンツ処理 |
| **エッジケース** | 6 | ゼロページ、タイムアウト、空データ等 |

**重要テスト**:
- `test_crawl_langgraph_docs_success`: Documentオブジェクト生成、メタデータ(source, title, doc_type, updated_at)検証
- `test_update_all_sources`: 全ソース統合更新、統計情報(total_documents, sources, status, errors)検証
- `test_crawl_network_error`: ネットワークエラー時のCrawlerError発生確認

---

#### 1.2 ベクトルストア (`tests/test_vectorstore.py`) - 18 tests

**目的**: Chromaベクトルストアの操作を検証。OpenAI Embeddingsは自動モック化。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **初期化** | 3 | インスタンス作成、カスタムパラメータ、Chromaクライアント初期化 |
| **ドキュメント追加** | 4 | 正常追加、バッチ処理、空リスト、重複処理 |
| **類似度検索** | 4 | 基本検索、フィルタ付き検索、空クエリ、結果なし |
| **コレクション管理** | 2 | 削除、情報取得 |
| **Retriever機能** | 2 | Retrieverインターフェース、invokeメソッド |
| **エラーハンドリング** | 3 | 追加エラー、埋め込みAPIエラー、永続化 |

**重要テスト**:
- `test_add_documents_success`: statusが"success"、added_count/failed_count検証
- `test_similarity_search`: 結果数≦k、全てDocumentオブジェクト
- `test_similarity_search_with_filter`: メタデータフィルタ(doc_type等)機能検証

---

#### 1.3 RAGチェーン (`tests/test_rag_chain.py`) - 15 tests

**目的**: RAG (Retrieval-Augmented Generation) チェーンの動作検証。LLMとベクトルストアはモック化。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **初期化** | 2 | インスタンス作成、カスタムパラメータ |
| **クエリ実行** | 4 | 正常実行、ソース付き回答、コード例付き回答、ソースなし回答 |
| **バリデーション** | 2 | 空質問、空白のみ質問 |
| **ヘルパーメソッド** | 4 | ソース抽出、コード例抽出、信頼度計算、コンテキスト構築 |
| **エラーハンドリング** | 3 | LLMエラー、検索エラー、タイムアウト |

**重要テスト**:
- `test_query_success`: answer、metadata、response_timeが含まれること
- `test_query_with_sources`: sources配列に url, title, excerpt, relevanceが含まれること
- `test_query_empty_question`: ValidationError発生確認

---

### 2. 構成案生成機能 (44 tests)

#### 2.1 LangGraphワークフロー (`tests/test_architect_graph.py`) - 19 tests

**目的**: ビジネス課題からLangGraph構成案を生成するワークフローを検証。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **初期化** | 2 | インスタンス作成、グラフコンパイル |
| **構成案生成** | 3 | 正常生成、業界指定、制約条件付き |
| **個別ノード** | 5 | 課題分析、構成生成、Mermaid生成、コード生成、説明生成 |
| **ヘルパーメソッド** | 3 | JSON抽出、コードブロック抽出、箇条書きパース |
| **エッジケース** | 3 | 空課題、長い課題文、日本語入力 |
| **エラーハンドリング** | 3 | LLMエラー、無効JSON応答、タイムアウト |

**重要テスト**:
- `test_generate_architecture_success`: challenge_analysis, architecture, code_example, business_explanation, mermaid_diagram が含まれること
- `test_generate_with_constraints`: implementation_notesに制約が反映されること
- `test_japanese_input`: 日本語課題が正しく処理され、日本語で説明生成されること

---

#### 2.2 Mermaid図生成 (`tests/test_visualizer.py`) - 25 tests

**目的**: ノードとエッジからMermaid図を生成する機能を検証。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **基本図生成** | 4 | 基本生成、条件分岐、flowchart、graph |
| **ノードラベルエスケープ** | 2 | 特殊文字(", ', &, <, >, 改行)処理 |
| **空・エッジケース** | 3 | 空ノード、空エッジ、大規模図(20+ノード) |
| **構文検証** | 2 | 有効構文、無効構文検出 |
| **異なる図タイプ** | 2 | flowchart、状態図 |
| **方向・スタイリング** | 2 | 方向指定(TD/LR)、ノード形状 |
| **複雑シナリオ** | 3 | 循環グラフ、複数パス、切断サブグラフ |
| **エラーハンドリング** | 2 | 必須フィールド欠損、無効エッジ参照 |
| **追加テスト** | 5 | Unicode、長いラベル、特殊ケース等 |

**重要テスト**:
- `test_generate_mermaid_diagram_basic`: graph/flowchartキーワード、ノード・エッジ、-->記法確認
- `test_node_label_escaping`: 特殊文字が正しくエスケープされること
- `test_cyclic_graph`: 循環エッジが正しく表現されること

---

### 3. ユーティリティ・設定 (40 tests)

#### 3.1 ユーティリティヘルパー (`tests/test_helpers.py`) - 25 tests

**目的**: ユーティリティヘルパー関数を検証。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **テキスト分割** | 5 | 基本分割、短文、空文、カスタムセパレータ、ゼロchunk_size |
| **コードブロック抽出** | 4 | Python、言語指定なし、なし、Mermaid |
| **トークン数計算** | 4 | 基本、空文、多言語(日英中)、超長文 |
| **メタデータフォーマット** | 3 | 基本フォーマット、フィールド欠損、空 |
| **ファイル名サニタイズ** | 6 | 基本、特殊文字、Unicode、最大長、空、パストラバーサル攻撃 |
| **Mermaid図パース** | 3 | 基本、複雑、無効 |

**重要テスト**:
- `test_split_text_into_chunks_basic`: chunk_size、chunk_overlapが正しく適用されること
- `test_sanitize_filename_path_traversal_attack`: ../や..\\が除去され、セキュリティが確保されること
- `test_extract_code_blocks_python`: ```python```ブロックが正しく抽出されること

---

#### 3.2 設定管理 (`tests/test_config.py`) - 15 tests

**目的**: 環境変数と設定管理を検証。

| カテゴリ | テスト数 | 主な検証内容 |
|---------|---------|------------|
| **初期化・バリデーション** | 5 | インスタンス作成、デフォルト値、OpenAI APIキー、Chromaディレクトリ、ログレベル |
| **追加設定** | 10 | LLMモデル、temperature、max_tokens、embedding_model等 |

**重要テスト**:
- `test_settings_initialization`: 環境変数が正しく読み込まれること
- `test_settings_validation_openai_api_key`: 有効なキーが受け入れられ、無効なキーでエラーが発生すること

---

## 統合テスト

### RAGフロー統合テスト (`tests/test_integration.py`) - 3 tests

**目的**: モジュール間の連携を検証。E2Eフローをテスト。

| テストID | テスト名 | 検証フロー |
|---------|---------|----------|
| TC-INT-001 | `test_end_to_end_rag_query` | クロール→ベクトルストア保存→RAG検索→回答生成 |
| TC-INT-002 | `test_document_update_flow` | ドキュメント更新後の検索可能性確認 |
| TC-INT-003 | `test_rag_with_empty_vectorstore` | 空VectorStoreでのエラーハンドリング |

---

## テスト実行

### ローカル実行

```bash
# 全テスト実行
pytest tests/ -v

# ユニットテストのみ
pytest tests/ -m "not integration and not e2e" -v

# 統合テストのみ
pytest tests/ -m integration -v

# カバレッジ付き実行
pytest tests/ --cov=src --cov-report=html --cov-report=term

# 特定ファイルのみ
pytest tests/test_crawler.py -v
```

### CI/CD実行 (GitHub Actions)

```yaml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: pytest tests/ -m "not integration" --cov=src --cov-report=xml
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY_TEST }}
      - uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## カバレッジ

### コードカバレッジ目標

| レイヤー | 目標 | 現在 | 優先度 |
|---------|------|------|-------|
| **全体** | 80%+ | 27.21% | 高 |
| RAG機能 | 85%+ | 92.13% (vectorstore) | 高 |
| 構成案生成 | 80%+ | 86.76% (graph) | 高 |
| ユーティリティ | 90%+ | 67.19% (helpers) | 中 |
| UI/UX | 60%+ | TBD | 中 |

### テストケース実装状況

| カテゴリ | 実装数 | 達成率 |
|---------|-------|-------|
| ユニットテスト | 115+ | ✅ 完了 |
| 統合テスト | 3 | ✅ 完了 |
| E2Eテスト | 0 | 🚧 計画中 |
| パフォーマンステスト | 0 | 🚧 計画中 |
| セキュリティテスト | 0 | 🚧 計画中 |

### テストファイル一覧

| ファイル | テスト数 | カバレッジ | 状態 |
|---------|---------|----------|------|
| `test_crawler.py` | 20 | TBD | ✅ 実装済み |
| `test_vectorstore.py` | 18 | 92.13% | ✅ 実装済み |
| `test_rag_chain.py` | 15 | 98.99% | ✅ 実装済み |
| `test_architect_graph.py` | 19 | 86.76% | ✅ 実装済み |
| `test_visualizer.py` | 25 | TBD | ✅ 実装済み |
| `test_helpers.py` | 25 | 67.19% | ✅ 実装済み |
| `test_config.py` | 15 | 100% | ✅ 実装済み |
| `test_integration.py` | 3 | N/A | ✅ 実装済み |

---

## テストのベストプラクティス

### AAA パターン
```python
def test_example():
    # Arrange - テストデータの準備
    data = prepare_test_data()
    # Act - テスト対象の実行
    result = function_under_test(data)
    # Assert - 結果の検証
    assert result == expected_value
```

### フィクスチャの活用
```python
@pytest.fixture
def sample_data():
    """再利用可能なテストデータ"""
    return {"key": "value"}
```

### モックの使用
```python
@patch('module.external_api_call')
def test_with_mock(mock_api):
    mock_api.return_value = "mocked_response"
    # テスト実行
```

---

## トラブルシューティング

| 問題 | 原因 | 解決策 |
|------|------|--------|
| テストが遅い | 実際のAPI呼び出し | モックを使用 |
| 不安定なテスト | 外部依存 | フィクスチャで安定化 |
| カバレッジが低い | テスト不足 | 主要パスを優先的にテスト |
| CI/CDでのみ失敗 | 環境差異 | 環境変数、依存関係を確認 |

---

## 付録

### pytest.ini 設定

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: ユニットテスト
    integration: 統合テスト
    e2e: E2Eテスト
    slow: 時間がかかるテスト
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings
```

### conftest.py 設定

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture(scope="session")
def test_config():
    """テスト用設定"""
    return {
        "openai_api_key": "sk-test-mock-key",
        "chroma_persist_dir": "./tests/data/chroma_test"
    }

@pytest.fixture
def mock_llm():
    """モックLLM"""
    mock = Mock()
    mock.invoke.return_value.content = "Mock response"
    return mock
```

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 3.0.0 | 2026-01-25 | ドキュメントを大幅にコンパクト化、新規テスト(crawler, visualizer, helpers)を追加 |
| 2.0.0 | 2026-01-24 | 詳細なテスト説明を追加 |
| 1.0.0 | 2026-01-19 | 初版作成 |

---

**Last Updated**: 2026-01-25
