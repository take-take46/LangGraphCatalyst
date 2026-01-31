"""
LangGraph Catalyst - RAG API Schemas

RAG学習支援API用のPydanticスキーマ定義。
リクエスト・レスポンスの型安全性を確保します。
"""

from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    """RAGクエリリクエスト"""

    question: str = Field(
        ...,
        description="ユーザーの質問",
        min_length=1,
        max_length=1000,
        examples=["LangGraphで条件分岐エッジを実装する方法は？"],
    )

    k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="取得する関連ドキュメント数",
    )

    include_sources: bool = Field(
        default=True,
        description="ソース情報を含めるか",
    )

    include_code_examples: bool = Field(
        default=True,
        description="コード例を含めるか",
    )


class SourceResponse(BaseModel):
    """ソース情報レスポンス"""

    title: str = Field(..., description="ドキュメントタイトル")
    url: str = Field(..., description="ソースURL")
    excerpt: str = Field(..., description="関連する抜粋")
    relevance: float = Field(..., ge=0.0, le=1.0, description="関連度スコア")
    doc_type: str = Field(..., description="ドキュメントタイプ (official_docs, blog, github)")


class CodeExampleResponse(BaseModel):
    """コード例レスポンス"""

    language: str = Field(..., description="プログラミング言語")
    code: str = Field(..., description="コード内容")
    description: str = Field(..., description="コードの説明")
    source_url: str | None = Field(None, description="ソースURL")


class RAGQueryMetadata(BaseModel):
    """RAGクエリメタデータ"""

    model: str = Field(..., description="使用したLLMモデル")
    tokens_used: int = Field(..., ge=0, description="使用トークン数")
    response_time: float = Field(..., ge=0.0, description="応答時間（秒）")


class RAGQueryResponse(BaseModel):
    """RAGクエリレスポンス"""

    answer: str = Field(..., description="回答テキスト")
    sources: list[SourceResponse] = Field(
        default_factory=list,
        description="参照ソース一覧",
    )
    code_examples: list[CodeExampleResponse] = Field(
        default_factory=list,
        description="コード例一覧",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="回答の信頼度スコア",
    )
    metadata: RAGQueryMetadata = Field(..., description="メタデータ")


class RAGHealthResponse(BaseModel):
    """RAGヘルスチェックレスポンス"""

    status: str = Field(..., description="ステータス (healthy, unhealthy)")
    vectorstore_connected: bool = Field(..., description="VectorStore接続状態")
    document_count: int = Field(..., ge=0, description="保存されているドキュメント数")
