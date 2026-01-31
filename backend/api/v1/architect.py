"""
LangGraph Catalyst - Architect API Endpoints

構成案生成機能のAPIエンドポイント。
既存のArchitectGraphロジックを呼び出します。
"""

import time

from fastapi import APIRouter, Depends, HTTPException

from backend.core.config import Settings, get_settings
from backend.core.dependencies import UserWithUsageLimit
from backend.schemas.architect import (
    ArchitectMetadata,
    ArchitectResponse,
    ArchitectRequest,
    Architecture,
    ChallengeAnalysis,
    CodeExample,
    EdgeDescription,
    NodeDescription,
)
from src.features.architect.graph import ArchitectGraph
from src.utils.exceptions import LLMError, ValidationError

router = APIRouter()


def get_architect_graph(
    settings: Settings = Depends(get_settings),
) -> ArchitectGraph:
    """
    ArchitectGraphインスタンスを取得する依存性注入

    Args:
        settings: アプリケーション設定

    Returns:
        ArchitectGraphインスタンス

    Raises:
        HTTPException: ArchitectGraph初期化エラー
    """
    try:
        return ArchitectGraph(
            llm_model=settings.default_llm_model,
            temperature=settings.temperature,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ArchitectGraphの初期化に失敗しました: {str(e)}",
        )


@router.post(
    "/architect/generate",
    response_model=ArchitectResponse,
    summary="構成案生成",
    description="ビジネス課題からLangGraph構成案を生成します",
    responses={
        200: {"description": "成功"},
        400: {"description": "不正なリクエスト"},
        500: {"description": "サーバーエラー"},
    },
)
async def generate_architecture(
    request: ArchitectRequest,
    current_user: UserWithUsageLimit,
    architect_graph: ArchitectGraph = Depends(get_architect_graph),
    settings: Settings = Depends(get_settings),
) -> ArchitectResponse:
    """
    構成案生成エンドポイント

    ビジネス課題を入力として受け取り、LangGraph構成案を生成します。
    課題分析、アーキテクチャ設計、Mermaid図、コード例、説明を含む包括的な出力を提供します。

    **認証必須**: JWTトークンが必要です。
    **使用制限**: テストユーザーは1日5回まで、管理者は無制限です。

    Args:
        request: 構成案生成リクエスト
        current_user: 認証されたユーザー（依存性注入）
        architect_graph: ArchitectGraphインスタンス（依存性注入）
        settings: アプリケーション設定（依存性注入）

    Returns:
        構成案生成レスポンス

    Raises:
        HTTPException: 構成案生成エラー、認証エラー、使用制限超過
    """
    start_time = time.time()

    try:
        # 構成案生成実行（既存のロジックをそのまま使用）
        result = architect_graph.generate_architecture(
            business_challenge=request.business_challenge,
            industry=request.industry,
            constraints=request.constraints,
        )

        # レスポンススキーマに変換
        challenge_analysis = ChallengeAnalysis(
            summary=result["challenge_analysis"]["summary"],
            key_requirements=result["challenge_analysis"]["key_requirements"],
            suggested_approach=result["challenge_analysis"]["suggested_approach"],
            langgraph_fit_reason=result["challenge_analysis"].get(
                "langgraph_fit_reason",
                "LangGraphの状態管理機能が適している",
            ),
        )

        # ノード説明の変換
        node_descriptions = [
            NodeDescription(
                node_id=node["node_id"],
                name=node["name"],
                purpose=node["purpose"],
                description=node.get("description", node["purpose"]),
                inputs=node.get("inputs", []),
                outputs=node.get("outputs", []),
            )
            for node in result["architecture"]["node_descriptions"]
        ]

        # エッジ説明の変換
        edge_descriptions = [
            EdgeDescription(
                from_node=edge["from_node"],
                to_node=edge["to_node"],
                condition=edge.get("condition"),
                description=edge["description"],
            )
            for edge in result["architecture"]["edge_descriptions"]
        ]

        architecture = Architecture(
            mermaid_diagram=result["architecture"]["mermaid_diagram"],
            node_descriptions=node_descriptions,
            edge_descriptions=edge_descriptions,
            state_schema=result["architecture"].get("state_schema", {}),
        )

        code_example = CodeExample(
            language=result["code_example"]["language"],
            code=result["code_example"]["code"],
            explanation=result["code_example"].get("explanation", ""),
        )

        response_time = time.time() - start_time

        metadata = ArchitectMetadata(
            model=result["metadata"]["model"],
            tokens_used=result["metadata"].get("tokens_used", 0),
            response_time=response_time,
        )

        return ArchitectResponse(
            challenge_analysis=challenge_analysis,
            architecture=architecture,
            code_example=code_example,
            business_explanation=result["business_explanation"],
            implementation_notes=result["implementation_notes"],
            metadata=metadata,
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"入力バリデーションエラー: {str(e)}",
        )
    except LLMError as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLMエラー: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"予期しないエラーが発生しました: {str(e)}",
        )
