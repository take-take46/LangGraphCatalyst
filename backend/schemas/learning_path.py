"""
LangGraph Catalyst - Learning Path Schemas

学習パス関連のPydanticスキーマ。
"""

from pydantic import BaseModel, Field


class Resource(BaseModel):
    """学習リソース"""

    type: str = Field(..., description="リソースタイプ（例: 公式ドキュメント、ブログ）")
    url: str = Field(..., description="リソースURL")


class TopicResponse(BaseModel):
    """学習トピックレスポンス"""

    id: str = Field(..., description="トピックID")
    level: str = Field(..., description="難易度レベル（初級、中級、上級）")
    order: int = Field(..., description="レベル内での順序")
    title: str = Field(..., description="トピックタイトル")
    description: str = Field(..., description="トピック説明")
    learning_objectives: list[str] = Field(..., description="学習目標のリスト")
    sample_questions: list[str] = Field(..., description="サンプル質問のリスト")
    prerequisites: list[str] = Field(default_factory=list, description="前提知識")
    estimated_time: str = Field(..., description="推定学習時間")
    resources: list[Resource] = Field(default_factory=list, description="学習リソース")


class LearningPathResponse(BaseModel):
    """学習パス全体のレスポンス"""

    topics: list[TopicResponse] = Field(..., description="全トピックのリスト")
    total_count: int = Field(..., description="総トピック数")
    levels: dict[str, int] = Field(
        ..., description="レベル別のトピック数（例: {'初級': 5, '中級': 5, '上級': 5}）"
    )


class LevelTopicsResponse(BaseModel):
    """特定レベルのトピック一覧レスポンス"""

    level: str = Field(..., description="レベル名")
    topics: list[TopicResponse] = Field(..., description="トピックのリスト")
    count: int = Field(..., description="トピック数")


class ProgressRequest(BaseModel):
    """進捗保存リクエスト"""

    completed_topic_ids: list[str] = Field(
        ..., description="完了したトピックIDのリスト", min_length=0
    )


class LevelProgress(BaseModel):
    """レベル別進捗"""

    progress: float = Field(..., description="進捗率（0.0-1.0）", ge=0.0, le=1.0)
    completed: int = Field(..., description="完了したトピック数", ge=0)
    total: int = Field(..., description="総トピック数", ge=0)


class ProgressResponse(BaseModel):
    """進捗計算レスポンス"""

    total_progress: float = Field(..., description="全体の進捗率（0.0-1.0）", ge=0.0, le=1.0)
    completed_count: int = Field(..., description="完了したトピック数", ge=0)
    total_count: int = Field(..., description="総トピック数", ge=0)
    levels: dict[str, LevelProgress] = Field(
        ..., description="レベル別の進捗（例: {'初級': {...}, '中級': {...}, '上級': {...}}）"
    )
