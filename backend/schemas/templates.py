"""
LangGraph Catalyst - Templates Schemas

テンプレート関連のPydanticスキーマ。
"""

from pydantic import BaseModel, Field


class TemplateResponse(BaseModel):
    """テンプレートレスポンス"""

    id: str = Field(..., description="テンプレートID")
    title: str = Field(..., description="テンプレートタイトル")
    description: str = Field(..., description="テンプレート説明")
    category: str = Field(..., description="カテゴリ（例: customer_support, data_analysis）")
    difficulty: str = Field(..., description="難易度（初級、中級、上級）")
    code: str = Field(..., description="実装コード（Python）")
    mermaid: str = Field(..., description="Mermaid図")
    explanation: str = Field(..., description="わかりやすい説明")
    use_cases: list[str] = Field(..., description="ユースケースのリスト")
    tags: list[str] = Field(..., description="タグのリスト")


class TemplatesListResponse(BaseModel):
    """テンプレート一覧レスポンス"""

    templates: list[TemplateResponse] = Field(..., description="テンプレートのリスト")
    total_count: int = Field(..., description="総テンプレート数")
    categories: dict[str, int] = Field(
        ...,
        description="カテゴリ別のテンプレート数（例: {'customer_support': 2, 'data_analysis': 1}）",
    )
    difficulties: dict[str, int] = Field(
        ..., description="難易度別のテンプレート数（例: {'初級': 2, '中級': 2, '上級': 1}）"
    )


class TemplateCategoriesResponse(BaseModel):
    """テンプレートカテゴリ一覧レスポンス"""

    categories: dict[str, str] = Field(
        ...,
        description="カテゴリID→カテゴリ名のマッピング（例: {'customer_support': 'カスタマーサポート'}）",
    )
