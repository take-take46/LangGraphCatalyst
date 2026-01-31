"""
LangGraph Catalyst - Common API Schemas

共通で使用するPydanticスキーマ定義。
"""

from typing import Any

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """成功レスポンス"""

    success: bool = Field(True, description="成功フラグ")
    message: str = Field(..., description="メッセージ")
    data: Any = Field(None, description="データ")


class ErrorResponse(BaseModel):
    """エラーレスポンス"""

    error: str = Field(..., description="エラーコード")
    message: str = Field(..., description="エラーメッセージ")
    details: str | None = Field(None, description="詳細情報")


class HealthResponse(BaseModel):
    """ヘルスチェックレスポンス"""

    status: str = Field(..., description="ステータス (healthy, unhealthy)")
    version: str = Field(..., description="APIバージョン")
    environment: str = Field(..., description="環境 (development, production)")
