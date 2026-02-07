"""
LangGraph Catalyst - Learning Path API Endpoints

学習パス機能のAPIエンドポイント。
"""

from fastapi import APIRouter, HTTPException

from backend.schemas.learning_path import (
    LearningPathResponse,
    LevelTopicsResponse,
    ProgressRequest,
    ProgressResponse,
    Resource,
    TopicResponse,
)
from src.features.learning_path.learning_path import (
    calculate_progress,
    get_all_topics,
    get_level_topics,
    get_topic_by_id,
)

router = APIRouter()


def convert_topic_to_response(topic: dict) -> TopicResponse:
    """
    既存のTopic型をPydanticレスポンスに変換

    Args:
        topic: 既存のTopic辞書

    Returns:
        TopicResponse: Pydanticレスポンススキーマ
    """
    return TopicResponse(
        id=topic["id"],
        level=topic["level"],
        order=topic["order"],
        title=topic["title"],
        description=topic["description"],
        learning_objectives=topic["learning_objectives"],
        sample_questions=topic["sample_questions"],
        prerequisites=topic["prerequisites"],
        estimated_time=topic["estimated_time"],
        resources=[Resource(**resource) for resource in topic["resources"]],
    )


@router.get(
    "/learning-path",
    response_model=LearningPathResponse,
    summary="学習パス全体取得",
    description="LangGraphの学習パス全体（初級〜上級）を取得します",
)
async def get_learning_path() -> LearningPathResponse:
    """
    学習パス全体取得エンドポイント

    初級、中級、上級のすべてのトピックを取得します。

    Returns:
        学習パス全体のレスポンス
    """
    topics = get_all_topics()
    topic_responses = [convert_topic_to_response(topic) for topic in topics]

    # レベル別のトピック数を集計
    levels_count = {}
    for topic in topics:
        level = topic["level"]
        levels_count[level] = levels_count.get(level, 0) + 1

    return LearningPathResponse(
        topics=topic_responses, total_count=len(topics), levels=levels_count
    )


@router.get(
    "/learning-path/level/{level}",
    response_model=LevelTopicsResponse,
    summary="特定レベルのトピック取得",
    description="指定されたレベル（初級、中級、上級）のトピックを取得します",
)
async def get_topics_by_level(level: str) -> LevelTopicsResponse:
    """
    特定レベルのトピック取得エンドポイント

    Args:
        level: レベル名（初級、中級、上級）

    Returns:
        指定レベルのトピック一覧

    Raises:
        HTTPException: 無効なレベル名
    """
    # レベル名のバリデーション
    valid_levels = ["初級", "中級", "上級"]
    if level not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"無効なレベル名です。有効な値: {', '.join(valid_levels)}",
        )

    topics = get_level_topics(level)
    topic_responses = [convert_topic_to_response(topic) for topic in topics]

    return LevelTopicsResponse(level=level, topics=topic_responses, count=len(topics))


@router.get(
    "/learning-path/topic/{topic_id}",
    response_model=TopicResponse,
    summary="特定トピック取得",
    description="トピックIDで個別のトピック詳細を取得します",
)
async def get_topic(topic_id: str) -> TopicResponse:
    """
    特定トピック取得エンドポイント

    Args:
        topic_id: トピックID（例: beginner_01）

    Returns:
        トピック詳細

    Raises:
        HTTPException: トピックが見つからない
    """
    topic = get_topic_by_id(topic_id)

    if topic is None:
        raise HTTPException(status_code=404, detail=f"トピックID '{topic_id}' が見つかりません")

    return convert_topic_to_response(topic)


@router.post(
    "/learning-path/progress",
    response_model=ProgressResponse,
    summary="進捗計算",
    description="完了したトピックIDのリストから学習進捗を計算します",
)
async def calculate_learning_progress(request: ProgressRequest) -> ProgressResponse:
    """
    進捗計算エンドポイント

    完了したトピックIDのリストを受け取り、全体およびレベル別の進捗を計算します。

    Args:
        request: 完了トピックIDのリスト

    Returns:
        進捗計算結果

    Raises:
        HTTPException: 計算エラー
    """
    try:
        progress_data = calculate_progress(request.completed_topic_ids)

        # Pydanticスキーマに変換
        from backend.schemas.learning_path import LevelProgress

        levels_response = {}
        for level_name, level_data in progress_data["levels"].items():
            levels_response[level_name] = LevelProgress(
                progress=level_data["progress"],
                completed=level_data["completed"],
                total=level_data["total"],
            )

        return ProgressResponse(
            total_progress=progress_data["total_progress"],
            completed_count=progress_data["completed_count"],
            total_count=progress_data["total_count"],
            levels=levels_response,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"進捗計算エラー: {str(e)}")
