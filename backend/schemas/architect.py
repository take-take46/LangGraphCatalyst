"""
LangGraph Catalyst - Architect API Schemas

構成案生成API用のPydanticスキーマ定義。
リクエスト・レスポンスの型安全性を確保します。
"""

from pydantic import BaseModel, Field


class ArchitectRequest(BaseModel):
    """構成案生成リクエスト"""

    business_challenge: str = Field(
        ...,
        description="ビジネス課題の説明",
        min_length=10,
        max_length=2000,
        examples=[
            "カスタマーサポートの自動化を実現したい。FAQへの自動回答と、複雑な問い合わせは人間にエスカレーションする仕組みが必要。"
        ],
    )

    industry: str | None = Field(
        None,
        description="業界（例: 製造業、EC）",
        max_length=100,
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="制約条件のリスト",
        max_length=10,
        examples=[["日本語対応必須", "既存のZendeskと連携"]],
    )


class ChallengeAnalysis(BaseModel):
    """課題分析結果"""

    summary: str = Field(..., description="課題の要約")
    key_requirements: list[str] = Field(..., description="主要要件")
    suggested_approach: str = Field(..., description="推奨アプローチ")
    langgraph_fit_reason: str = Field(..., description="LangGraph適用の妥当性")


class NodeDescription(BaseModel):
    """ノード説明"""

    node_id: str = Field(..., description="ノードID")
    name: str = Field(..., description="ノード名")
    purpose: str = Field(..., description="目的")
    description: str = Field(..., description="詳細説明")
    inputs: list[str] = Field(..., description="入力")
    outputs: list[str] = Field(..., description="出力")


class EdgeDescription(BaseModel):
    """エッジ説明"""

    from_node: str = Field(..., description="開始ノード")
    to_node: str = Field(..., description="終了ノード")
    condition: str | None = Field(None, description="条件分岐の条件（ある場合）")
    description: str = Field(..., description="エッジの説明")


class Architecture(BaseModel):
    """アーキテクチャ定義"""

    mermaid_diagram: str = Field(..., description="Mermaid記法のフローチャート")
    node_descriptions: list[NodeDescription] = Field(..., description="ノード説明一覧")
    edge_descriptions: list[EdgeDescription] = Field(..., description="エッジ説明一覧")
    state_schema: dict[str, str] = Field(
        default_factory=dict,
        description="状態スキーマ（フィールド名: 説明）",
    )


class CodeExample(BaseModel):
    """コード例"""

    language: str = Field(..., description="プログラミング言語")
    code: str = Field(..., description="実装コード")
    explanation: str = Field(..., description="コードの説明")


class ArchitectMetadata(BaseModel):
    """構成案生成メタデータ"""

    model: str = Field(..., description="使用したLLMモデル")
    tokens_used: int = Field(..., ge=0, description="使用トークン数")
    response_time: float = Field(..., ge=0.0, description="応答時間（秒）")


class ArchitectResponse(BaseModel):
    """構成案生成レスポンス"""

    challenge_analysis: ChallengeAnalysis = Field(..., description="課題分析結果")
    architecture: Architecture = Field(..., description="アーキテクチャ定義")
    code_example: CodeExample = Field(..., description="実装コード例")
    business_explanation: str = Field(..., description="非技術者向け説明")
    implementation_notes: list[str] = Field(
        default_factory=list,
        description="実装時の注意点",
    )
    metadata: ArchitectMetadata = Field(..., description="メタデータ")
