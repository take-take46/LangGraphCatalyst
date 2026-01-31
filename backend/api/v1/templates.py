"""
LangGraph Catalyst - Templates API Endpoints

テンプレート機能のAPIエンドポイント。
"""

from fastapi import APIRouter, HTTPException, Query

from backend.schemas.templates import (
    TemplateCategoriesResponse,
    TemplateResponse,
    TemplatesListResponse,
)
from src.features.templates.templates import (
    TEMPLATE_CATEGORIES,
    TEMPLATES,
    get_template_by_id,
    get_templates_by_category,
    get_templates_by_difficulty,
)

router = APIRouter()


def convert_template_to_response(template: dict) -> TemplateResponse:
    """
    既存のTemplate型をPydanticレスポンスに変換

    Args:
        template: 既存のTemplate辞書

    Returns:
        TemplateResponse: Pydanticレスポンススキーマ
    """
    return TemplateResponse(
        id=template["id"],
        title=template["title"],
        description=template["description"],
        category=template["category"],
        difficulty=template["difficulty"],
        code=template["code"],
        mermaid=template["mermaid"],
        explanation=template["explanation"],
        use_cases=template["use_cases"],
        tags=template["tags"],
    )


@router.get(
    "/templates",
    response_model=TemplatesListResponse,
    summary="テンプレート一覧取得",
    description="LangGraphテンプレート一覧を取得します。カテゴリや難易度でフィルタリング可能です。",
)
async def get_templates(
    category: str | None = Query(None, description="カテゴリでフィルタリング"),
    difficulty: str | None = Query(None, description="難易度でフィルタリング（初級、中級、上級）"),
) -> TemplatesListResponse:
    """
    テンプレート一覧取得エンドポイント

    Args:
        category: カテゴリ名でフィルタリング（オプション）
        difficulty: 難易度でフィルタリング（オプション）

    Returns:
        テンプレート一覧レスポンス

    Raises:
        HTTPException: 無効なフィルタパラメータ
    """
    # フィルタリング
    if category and difficulty:
        # 両方のフィルタを適用
        templates = [
            t
            for t in TEMPLATES
            if t["category"] == category and t["difficulty"] == difficulty
        ]
    elif category:
        # カテゴリのみでフィルタ
        if category not in TEMPLATE_CATEGORIES:
            raise HTTPException(
                status_code=400,
                detail=f"無効なカテゴリです。有効な値: {', '.join(TEMPLATE_CATEGORIES.keys())}",
            )
        templates = get_templates_by_category(category)
    elif difficulty:
        # 難易度のみでフィルタ
        valid_difficulties = ["初級", "中級", "上級"]
        if difficulty not in valid_difficulties:
            raise HTTPException(
                status_code=400,
                detail=f"無効な難易度です。有効な値: {', '.join(valid_difficulties)}",
            )
        templates = get_templates_by_difficulty(difficulty)
    else:
        # フィルタなし（全テンプレート）
        templates = TEMPLATES

    template_responses = [convert_template_to_response(t) for t in templates]

    # カテゴリ別の集計
    categories_count = {}
    for t in templates:
        cat = t["category"]
        categories_count[cat] = categories_count.get(cat, 0) + 1

    # 難易度別の集計
    difficulties_count = {}
    for t in templates:
        diff = t["difficulty"]
        difficulties_count[diff] = difficulties_count.get(diff, 0) + 1

    return TemplatesListResponse(
        templates=template_responses,
        total_count=len(templates),
        categories=categories_count,
        difficulties=difficulties_count,
    )


@router.get(
    "/templates/categories",
    response_model=TemplateCategoriesResponse,
    summary="カテゴリ一覧取得",
    description="テンプレートのカテゴリ一覧を取得します",
)
async def get_template_categories() -> TemplateCategoriesResponse:
    """
    テンプレートカテゴリ一覧取得エンドポイント

    Returns:
        カテゴリ一覧レスポンス（カテゴリID→カテゴリ名のマッピング）
    """
    return TemplateCategoriesResponse(categories=TEMPLATE_CATEGORIES)


@router.get(
    "/templates/{template_id}",
    response_model=TemplateResponse,
    summary="個別テンプレート取得",
    description="テンプレートIDで個別のテンプレート詳細を取得します",
)
async def get_template(template_id: str) -> TemplateResponse:
    """
    個別テンプレート取得エンドポイント

    Args:
        template_id: テンプレートID（例: customer_support_basic）

    Returns:
        テンプレート詳細

    Raises:
        HTTPException: テンプレートが見つからない
    """
    template = get_template_by_id(template_id)

    if template is None:
        raise HTTPException(
            status_code=404, detail=f"テンプレートID '{template_id}' が見つかりません"
        )

    return convert_template_to_response(template)
