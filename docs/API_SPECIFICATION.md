# LangGraph Catalyst - API仕様書

## 目次
- [概要](#概要)
- [内部モジュールAPI](#内部モジュールapi)
- [REST API仕様（将来実装）](#rest-api仕様将来実装)
- [データモデル](#データモデル)
- [エラーハンドリング](#エラーハンドリング)
- [認証・セキュリティ](#認証セキュリティ)

---

## 概要

### 目的
LangGraph Catalystは、LangGraphの学習支援とビジネス活用を促進するポートフォリオシステムです。本API仕様書では、システム内部のモジュール間インターフェースと、将来的な外部API公開を見据えた仕様を定義します。

### アーキテクチャ
- **フロントエンド**: Streamlit (Web UI)
- **バックエンド**: Python (LangChain/LangGraph)
- **ベクトルDB**: Chroma
- **LLM**: OpenAI API (GPT-4等)

### バージョン
- API Version: 1.0.0
- 最終更新日: 2026-01-19

---

## 内部モジュールAPI

### 1. RAG機能 (`src/features/rag/`)

#### 1.1 ドキュメントクローラー (`crawler.py`)

##### `crawl_langgraph_docs()`
LangGraph公式ドキュメントをクロールし、テキストとメタデータを取得します。

**シグネチャ**:
```python
def crawl_langgraph_docs(
    max_pages: int = 100,
    include_api_reference: bool = True
) -> list[Document]
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `max_pages` | `int` | No | 100 | クロールする最大ページ数 |
| `include_api_reference` | `bool` | No | True | APIリファレンスを含めるか |

**戻り値**:
```python
list[Document]  # LangChain Document オブジェクトのリスト
```

**Document構造**:
```python
{
    "page_content": str,  # ドキュメントのテキスト内容
    "metadata": {
        "source": str,      # ソースURL
        "title": str,       # ページタイトル
        "updated_at": str,  # 更新日時 (ISO 8601形式)
        "doc_type": str     # "official_docs" | "blog" | "github"
    }
}
```

**例外**:
- `ConnectionError`: ネットワーク接続エラー
- `HTTPError`: HTTPステータスエラー (404, 500等)
- `ParsingError`: HTMLパース失敗

**使用例**:
```python
from src.features.rag.crawler import crawl_langgraph_docs

docs = crawl_langgraph_docs(max_pages=50)
print(f"Crawled {len(docs)} documents")
```

---

##### `crawl_langchain_blog()`
LangChain Blogから記事をクロールします。

**シグネチャ**:
```python
def crawl_langchain_blog(
    tag: str = "langgraph",
    max_articles: int = 50
) -> list[Document]
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `tag` | `str` | No | "langgraph" | フィルタリングするタグ |
| `max_articles` | `int` | No | 50 | 取得する最大記事数 |

**戻り値**: `list[Document]`

---

##### `crawl_github_repo()`
GitHubリポジトリからREADME、examplesなどを取得します。

**シグネチャ**:
```python
def crawl_github_repo(
    repo: str = "langchain-ai/langgraph",
    include_examples: bool = True,
    include_tests: bool = False
) -> list[Document]
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `repo` | `str` | No | "langchain-ai/langgraph" | リポジトリ名 (owner/repo) |
| `include_examples` | `bool` | No | True | examples/ディレクトリを含める |
| `include_tests` | `bool` | No | False | tests/ディレクトリを含める |

**戻り値**: `list[Document]`

---

##### `update_all_sources()`
すべてのソースからドキュメントを更新します。

**シグネチャ**:
```python
def update_all_sources() -> dict[str, Any]
```

**戻り値**:
```python
{
    "total_documents": int,
    "sources": {
        "official_docs": int,
        "blog": int,
        "github": int
    },
    "updated_at": str,  # ISO 8601形式
    "status": "success" | "partial" | "failed",
    "errors": list[str] | None
}
```

**使用例**:
```python
from src.features.rag.crawler import update_all_sources

result = update_all_sources()
if result["status"] == "success":
    print(f"Successfully updated {result['total_documents']} documents")
```

---

#### 1.2 ベクトルストア (`vectorstore.py`)

##### `ChromaVectorStore`
Chromaベクトルストアの操作を管理するクラス。

**初期化**:
```python
class ChromaVectorStore:
    def __init__(
        self,
        collection_name: str = "langgraph_docs",
        persist_directory: str | None = None,
        embedding_model: str = "text-embedding-3-small"
    )
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `collection_name` | `str` | No | "langgraph_docs" | コレクション名 |
| `persist_directory` | `str \| None` | No | None | 永続化ディレクトリ (Noneの場合は設定から取得) |
| `embedding_model` | `str` | No | "text-embedding-3-small" | OpenAI埋め込みモデル |

---

##### `add_documents()`
ドキュメントをベクトルストアに追加します。

**シグネチャ**:
```python
def add_documents(
    self,
    documents: list[Document],
    batch_size: int = 100
) -> dict[str, Any]
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `documents` | `list[Document]` | Yes | - | 追加するドキュメントのリスト |
| `batch_size` | `int` | No | 100 | バッチ処理サイズ |

**戻り値**:
```python
{
    "added_count": int,
    "failed_count": int,
    "total_documents_in_store": int,
    "status": "success" | "partial" | "failed"
}
```

**使用例**:
```python
from src.features.rag.vectorstore import ChromaVectorStore
from src.features.rag.crawler import crawl_langgraph_docs

vectorstore = ChromaVectorStore()
docs = crawl_langgraph_docs()
result = vectorstore.add_documents(docs)
```

---

##### `similarity_search()`
類似度検索を実行します。

**シグネチャ**:
```python
def similarity_search(
    self,
    query: str,
    k: int = 5,
    filter_metadata: dict[str, Any] | None = None
) -> list[Document]
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `query` | `str` | Yes | - | 検索クエリ |
| `k` | `int` | No | 5 | 取得する上位k件 |
| `filter_metadata` | `dict \| None` | No | None | メタデータフィルタ |

**戻り値**: `list[Document]` (類似度スコア付き)

**使用例**:
```python
results = vectorstore.similarity_search(
    query="How to create a graph in LangGraph?",
    k=3,
    filter_metadata={"doc_type": "official_docs"}
)
```

---

##### `delete_collection()`
コレクションを削除します。

**シグネチャ**:
```python
def delete_collection(self) -> bool
```

**戻り値**: `bool` (成功時True)

---

#### 1.3 RAGチェーン (`chain.py`)

##### `RAGChain`
RAG (Retrieval-Augmented Generation) チェーンのクラス。

**初期化**:
```python
class RAGChain:
    def __init__(
        self,
        vectorstore: ChromaVectorStore,
        llm_model: str = "gpt-4-turbo-preview",
        temperature: float = 0.3,
        streaming: bool = False
    )
```

---

##### `query()`
RAGクエリを実行します。

**シグネチャ**:
```python
def query(
    self,
    question: str,
    k: int = 5,
    include_sources: bool = True,
    include_code_examples: bool = True
) -> RAGResponse
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `question` | `str` | Yes | - | ユーザーの質問 |
| `k` | `int` | No | 5 | 検索する関連ドキュメント数 |
| `include_sources` | `bool` | No | True | ソース情報を含める |
| `include_code_examples` | `bool` | No | True | コード例を含める |

**戻り値** (`RAGResponse`):
```python
{
    "answer": str,              # 回答テキスト
    "sources": list[Source],    # ソース情報のリスト
    "code_examples": list[CodeExample] | None,  # コード例
    "confidence": float,        # 信頼度スコア (0-1)
    "metadata": {
        "model": str,
        "tokens_used": int,
        "response_time": float  # 秒
    }
}
```

**Source構造**:
```python
{
    "title": str,
    "url": str,
    "excerpt": str,     # 関連する抜粋
    "relevance": float  # 関連度スコア (0-1)
}
```

**CodeExample構造**:
```python
{
    "language": str,    # "python" | "typescript" 等
    "code": str,
    "description": str,
    "source_url": str | None
}
```

**使用例**:
```python
from src.features.rag.chain import RAGChain
from src.features.rag.vectorstore import ChromaVectorStore

vectorstore = ChromaVectorStore()
rag_chain = RAGChain(vectorstore)

response = rag_chain.query(
    question="How do I create a conditional edge in LangGraph?",
    k=5
)

print(response["answer"])
for source in response["sources"]:
    print(f"- {source['title']}: {source['url']}")
```

---

### 2. 構成案生成機能 (`src/features/architect/`)

#### 2.1 LangGraphワークフロー (`graph.py`)

##### `ArchitectGraph`
ビジネス課題からLangGraph構成案を生成するワークフロー。

**初期化**:
```python
class ArchitectGraph:
    def __init__(
        self,
        llm_model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        streaming: bool = False
    )
```

---

##### `generate_architecture()`
ビジネス課題から構成案を生成します。

**シグネチャ**:
```python
def generate_architecture(
    self,
    business_challenge: str,
    industry: str | None = None,
    constraints: list[str] | None = None
) -> ArchitectureResponse
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `business_challenge` | `str` | Yes | - | ビジネス課題の説明 |
| `industry` | `str \| None` | No | None | 業界（例: "製造業", "EC"） |
| `constraints` | `list[str] \| None` | No | None | 制約条件のリスト |

**戻り値** (`ArchitectureResponse`):
```python
{
    "challenge_analysis": {
        "summary": str,          # 課題の要約
        "key_requirements": list[str],
        "suggested_approach": str
    },
    "architecture": {
        "mermaid_diagram": str,  # Mermaid記法の図
        "node_descriptions": list[NodeDescription],
        "edge_descriptions": list[EdgeDescription]
    },
    "code_example": {
        "language": "python",
        "code": str,
        "explanation": str
    },
    "business_explanation": str,  # 非技術者向け説明
    "implementation_notes": list[str],
    "metadata": {
        "model": str,
        "tokens_used": int,
        "response_time": float
    }
}
```

**NodeDescription構造**:
```python
{
    "node_id": str,
    "name": str,
    "purpose": str,
    "inputs": list[str],
    "outputs": list[str]
}
```

**EdgeDescription構造**:
```python
{
    "from_node": str,
    "to_node": str,
    "condition": str | None,  # 条件分岐の場合
    "description": str
}
```

**使用例**:
```python
from src.features.architect.graph import ArchitectGraph

architect = ArchitectGraph()

response = architect.generate_architecture(
    business_challenge="カスタマーサポートの自動化を実現したい。FAQへの自動回答と、複雑な問い合わせは人間にエスカレーションする仕組みが必要。",
    industry="EC",
    constraints=["日本語対応必須", "既存のZendeskと連携"]
)

print(response["business_explanation"])
print("\n## アーキテクチャ図")
print(response["architecture"]["mermaid_diagram"])
```

---

#### 2.2 Mermaid図生成 (`visualizer.py`)

##### `generate_mermaid_diagram()`
ノードとエッジからMermaid図を生成します。

**シグネチャ**:
```python
def generate_mermaid_diagram(
    nodes: list[NodeDescription],
    edges: list[EdgeDescription],
    diagram_type: str = "flowchart"
) -> str
```

**パラメータ**:
| 名前 | 型 | 必須 | デフォルト | 説明 |
|------|-----|------|-----------|------|
| `nodes` | `list[NodeDescription]` | Yes | - | ノードのリスト |
| `edges` | `list[EdgeDescription]` | Yes | - | エッジのリスト |
| `diagram_type` | `str` | No | "flowchart" | 図のタイプ ("flowchart" | "graph") |

**戻り値**: `str` (Mermaid記法のテキスト)

**使用例**:
```python
from src.features.architect.visualizer import generate_mermaid_diagram

nodes = [
    {"node_id": "start", "name": "開始", "purpose": "入力受付", ...},
    {"node_id": "analyze", "name": "分析", "purpose": "意図分析", ...}
]

edges = [
    {"from_node": "start", "to_node": "analyze", "description": "入力を渡す", ...}
]

mermaid_code = generate_mermaid_diagram(nodes, edges)
print(mermaid_code)
```

---

### 3. 設定管理 (`src/config/settings.py`)

##### `Settings`
環境変数と設定を管理するPydantic Settingsクラス。

**フィールド**:
```python
class Settings(BaseSettings):
    openai_api_key: str
    chroma_persist_dir: str = "./data/chroma"
    log_level: str = "INFO"
    default_llm_model: str = "gpt-4-turbo-preview"
    default_embedding_model: str = "text-embedding-3-small"
    max_tokens: int = 4096
    temperature: float = 0.3

    class Config:
        env_file = ".env"
        case_sensitive = False
```

**使用例**:
```python
from src.config.settings import Settings

settings = Settings()
print(settings.openai_api_key)  # 環境変数から取得
```

---

## REST API仕様（将来実装）

将来的にStreamlitアプリとは別に、REST APIとして公開する場合の仕様です。

### ベースURL
```
https://api.langgraph-catalyst.com/v1
```

### 認証
```http
Authorization: Bearer <API_KEY>
```

---

### エンドポイント一覧

#### 1. RAGクエリ

##### `POST /rag/query`
LangGraphに関する質問に回答します。

**リクエスト**:
```http
POST /rag/query
Content-Type: application/json
Authorization: Bearer <API_KEY>

{
    "question": "How do I create a conditional edge in LangGraph?",
    "k": 5,
    "include_sources": true,
    "include_code_examples": true
}
```

**レスポンス** (200 OK):
```json
{
    "answer": "To create a conditional edge in LangGraph, you use the `add_conditional_edges()` method...",
    "sources": [
        {
            "title": "Conditional Edges - LangGraph Documentation",
            "url": "https://langchain-ai.github.io/langgraph/concepts/conditional_edges/",
            "excerpt": "Conditional edges allow you to route execution based on...",
            "relevance": 0.92
        }
    ],
    "code_examples": [
        {
            "language": "python",
            "code": "from langgraph.graph import StateGraph\n\ndef route_message(state):\n    if state['needs_human']:\n        return 'human'\n    return 'agent'\n\ngraph.add_conditional_edges(\n    'analyze',\n    route_message,\n    {'human': 'escalate', 'agent': 'respond'}\n)",
            "description": "Example of routing based on state",
            "source_url": "https://github.com/langchain-ai/langgraph/blob/main/examples/..."
        }
    ],
    "confidence": 0.89,
    "metadata": {
        "model": "gpt-4-turbo-preview",
        "tokens_used": 1543,
        "response_time": 2.34
    }
}
```

**エラーレスポンス**:
- `400 Bad Request`: 不正なリクエスト
- `401 Unauthorized`: 認証失敗
- `429 Too Many Requests`: レート制限超過
- `500 Internal Server Error`: サーバーエラー

---

#### 2. 構成案生成

##### `POST /architect/generate`
ビジネス課題からLangGraph構成案を生成します。

**リクエスト**:
```http
POST /architect/generate
Content-Type: application/json
Authorization: Bearer <API_KEY>

{
    "business_challenge": "カスタマーサポートの自動化を実現したい",
    "industry": "EC",
    "constraints": ["日本語対応必須", "既存のZendeskと連携"]
}
```

**レスポンス** (200 OK):
```json
{
    "challenge_analysis": {
        "summary": "EC業界におけるカスタマーサポートの効率化...",
        "key_requirements": [
            "FAQ自動回答",
            "複雑な問い合わせのエスカレーション",
            "Zendesk連携"
        ],
        "suggested_approach": "LangGraphの条件分岐を活用した段階的対応フロー"
    },
    "architecture": {
        "mermaid_diagram": "graph TD\n    A[問い合わせ受付] --> B{FAQ検索}\n    B -->|一致| C[自動回答]\n    B -->|不一致| D[意図分析]\n    D --> E{複雑度判定}\n    E -->|簡単| F[AI回答生成]\n    E -->|複雑| G[人間にエスカレーション]\n    F --> H[Zendesk記録]\n    G --> H",
        "node_descriptions": [
            {
                "node_id": "A",
                "name": "問い合わせ受付",
                "purpose": "ユーザーからの問い合わせを受け付ける",
                "inputs": ["user_query"],
                "outputs": ["query_text", "user_id"]
            }
        ],
        "edge_descriptions": [
            {
                "from_node": "A",
                "to_node": "B",
                "condition": null,
                "description": "受付した問い合わせをFAQ検索に渡す"
            }
        ]
    },
    "code_example": {
        "language": "python",
        "code": "from langgraph.graph import StateGraph\nfrom typing import TypedDict\n\nclass SupportState(TypedDict):\n    query: str\n    faq_match: bool\n    complexity: str\n    response: str\n\ndef faq_search(state):\n    # FAQ検索ロジック\n    return {'faq_match': check_faq(state['query'])}\n\n...",
        "explanation": "このコードは、カスタマーサポート自動化のための基本的なLangGraphワークフローを示しています..."
    },
    "business_explanation": "このシステムでは、まずFAQデータベースで即座に回答できる質問かを判定します。該当しない場合は、AIが質問の複雑度を分析し、簡単な質問にはAIが回答、複雑な質問は人間のオペレーターにエスカレーションします。全てのやり取りはZendeskに記録され、後からの分析や改善に活用できます。",
    "implementation_notes": [
        "FAQ検索にはベクトルDBを使用することを推奨",
        "Zendesk APIの認証情報が必要",
        "日本語の精度向上のため、プロンプトに日本語での回答を明示"
    ],
    "metadata": {
        "model": "gpt-4-turbo-preview",
        "tokens_used": 3421,
        "response_time": 8.76
    }
}
```

---

#### 3. ドキュメント更新

##### `POST /admin/update-documents`
RAGデータソースを更新します（管理者用）。

**リクエスト**:
```http
POST /admin/update-documents
Content-Type: application/json
Authorization: Bearer <ADMIN_API_KEY>

{
    "sources": ["official_docs", "blog", "github"],
    "max_documents": 200
}
```

**レスポンス** (202 Accepted):
```json
{
    "job_id": "update-20260119-abc123",
    "status": "processing",
    "message": "Document update started",
    "estimated_time": 300
}
```

**ジョブ状態確認**:
```http
GET /admin/jobs/{job_id}
```

**レスポンス** (200 OK):
```json
{
    "job_id": "update-20260119-abc123",
    "status": "completed",
    "result": {
        "total_documents": 187,
        "sources": {
            "official_docs": 92,
            "blog": 45,
            "github": 50
        },
        "updated_at": "2026-01-19T10:30:45Z"
    }
}
```

---

### レート制限
| プラン | リクエスト数 | 期間 |
|--------|------------|------|
| Free | 10 | 1時間 |
| Basic | 100 | 1時間 |
| Pro | 1000 | 1時間 |

**レート制限時のレスポンス** (429):
```json
{
    "error": "rate_limit_exceeded",
    "message": "API rate limit exceeded",
    "retry_after": 3600,
    "limit": 10,
    "remaining": 0
}
```

---

## データモデル

### Document
LangChain標準のDocumentオブジェクト。

```python
from langchain.schema import Document

document = Document(
    page_content="LangGraph is a framework...",
    metadata={
        "source": "https://...",
        "title": "Introduction to LangGraph",
        "updated_at": "2026-01-15T12:00:00Z",
        "doc_type": "official_docs"
    }
)
```

---

### State (LangGraph)
LangGraphのワークフロー状態管理。

#### RAGState
```python
from typing import TypedDict

class RAGState(TypedDict):
    question: str
    retrieved_docs: list[Document]
    answer: str
    sources: list[dict]
    code_examples: list[dict]
```

#### ArchitectState
```python
class ArchitectState(TypedDict):
    business_challenge: str
    industry: str | None
    constraints: list[str]
    challenge_analysis: dict
    nodes: list[dict]
    edges: list[dict]
    mermaid_diagram: str
    code_example: dict
    business_explanation: str
```

---

## エラーハンドリング

### エラーコード一覧

| コード | 名前 | 説明 | HTTPステータス |
|--------|------|------|----------------|
| `INVALID_REQUEST` | 不正なリクエスト | リクエストパラメータが不正 | 400 |
| `UNAUTHORIZED` | 認証エラー | API Keyが無効または未提供 | 401 |
| `RATE_LIMIT_EXCEEDED` | レート制限超過 | APIリクエスト制限を超過 | 429 |
| `LLM_ERROR` | LLMエラー | OpenAI API呼び出しエラー | 500 |
| `VECTORSTORE_ERROR` | ベクトルストアエラー | Chroma接続エラー | 500 |
| `CRAWL_ERROR` | クロールエラー | ドキュメント取得失敗 | 500 |
| `PARSING_ERROR` | パースエラー | レスポンスのパース失敗 | 500 |
| `INTERNAL_ERROR` | 内部エラー | その他のサーバーエラー | 500 |

### エラーレスポンス形式

```json
{
    "error": {
        "code": "LLM_ERROR",
        "message": "OpenAI API returned an error",
        "details": "Rate limit exceeded for model gpt-4-turbo-preview",
        "request_id": "req-abc123",
        "timestamp": "2026-01-19T10:30:45Z"
    }
}
```

### Python例外クラス

```python
# src/utils/exceptions.py

class CatalystException(Exception):
    """基底例外クラス"""
    pass

class VectorStoreError(CatalystException):
    """ベクトルストア関連エラー"""
    pass

class LLMError(CatalystException):
    """LLM呼び出しエラー"""
    pass

class CrawlerError(CatalystException):
    """クローラーエラー"""
    pass

class ValidationError(CatalystException):
    """バリデーションエラー"""
    pass
```

**使用例**:
```python
from src.utils.exceptions import VectorStoreError

try:
    vectorstore.add_documents(docs)
except VectorStoreError as e:
    logger.error(f"Failed to add documents: {e}")
    # エラーハンドリング処理
```

---

## 認証・セキュリティ

### API Key管理

**環境変数**:
```bash
# OpenAI API Key
OPENAI_API_KEY=sk-...

# 管理者用API Key（将来実装）
ADMIN_API_KEY=cat_admin_...

# ユーザー用API Key（将来実装）
USER_API_KEY=cat_user_...
```

### セキュリティベストプラクティス

1. **API Keyの保護**
   - `.env` ファイルは `.gitignore` に含める
   - 環境変数として管理
   - コードにハードコーディングしない

2. **入力検証**
   - すべてのユーザー入力をバリデーション
   - SQLインジェクション対策
   - プロンプトインジェクション対策

3. **レート制限**
   - APIリクエスト数の制限
   - IP単位での制限
   - ユーザー単位での制限

4. **ロギング**
   - すべてのAPI呼び出しをログ記録
   - エラー情報の詳細記録
   - 機密情報のマスキング

**ロギング例**:
```python
import logging
from src.config.settings import settings

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# 使用例
logger.info(f"RAG query received: {query[:50]}...")  # 最初の50文字のみログ
logger.error(f"LLM error: {error_code}", exc_info=True)
```

5. **データ保護**
   - ユーザーデータの暗号化
   - HTTPS通信の必須化
   - CORS設定の適切な管理

---

## パフォーマンス最適化

### キャッシング戦略

#### Streamlitキャッシング
```python
import streamlit as st

@st.cache_resource
def get_vectorstore():
    """ベクトルストアのキャッシング（アプリ全体で共有）"""
    return ChromaVectorStore()

@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_faq_data():
    """FAQデータのキャッシング"""
    return load_faq_from_db()
```

#### LLMキャッシング
```python
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# LLMレスポンスのキャッシング
set_llm_cache(InMemoryCache())
```

### ベクトル検索の最適化

```python
# バッチ処理
vectorstore.add_documents(docs, batch_size=100)

# フィルタリングで検索範囲を絞る
results = vectorstore.similarity_search(
    query=query,
    k=5,
    filter_metadata={"doc_type": "official_docs"}
)
```

---

## 付録

### A. 使用技術スタック

| カテゴリ | 技術 | バージョン | 用途 |
|---------|------|-----------|------|
| Language | Python | 3.11+ | メイン言語 |
| Framework | LangChain | 0.1.0+ | LLMアプリケーション基盤 |
| Framework | LangGraph | 0.0.20+ | ワークフロー管理 |
| Vector DB | Chroma | 0.4.0+ | ベクトルストア |
| LLM | OpenAI API | gpt-4-turbo-preview | 言語モデル |
| Embedding | OpenAI | text-embedding-3-small | ベクトル埋め込み |
| Web UI | Streamlit | 1.30.0+ | フロントエンド |
| HTTP Client | httpx | 0.25.0+ | 非同期HTTPクライアント |
| HTML Parser | BeautifulSoup4 | 4.12.0+ | HTMLパース |
| Validation | Pydantic | 2.5.0+ | データバリデーション |

### B. 開発ツール

| ツール | 用途 |
|--------|------|
| Ruff | リンター・フォーマッター |
| pytest | テストフレームワーク |
| mypy | 型チェッカー（オプション） |

### C. 参考リンク

- [LangGraph公式ドキュメント](https://langchain-ai.github.io/langgraph/)
- [LangChain公式ドキュメント](https://python.langchain.com/)
- [Chroma公式ドキュメント](https://docs.trychroma.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Streamlit公式ドキュメント](https://docs.streamlit.io/)

---

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.0.0 | 2026-01-19 | 初版作成 |

---

## お問い合わせ

- GitHub Issues: [リポジトリURL]/issues
- Email: [連絡先メールアドレス]

---

**Last Updated**: 2026-01-19
