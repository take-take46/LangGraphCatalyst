"""
LangGraph Catalyst - Authentication Schemas

認証関連のPydanticスキーマ。
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """ログインリクエスト"""

    username: str = Field(..., description="ユーザー名", min_length=1)
    password: str = Field(..., description="パスワード", min_length=1)


class UserResponse(BaseModel):
    """ユーザー情報レスポンス"""

    username: str = Field(..., description="ユーザー名")
    role: str = Field(..., description="ロール（admin または user）")
    daily_limit: int | None = Field(
        None, description="1日の使用制限回数（Noneは無制限）"
    )


class LoginResponse(BaseModel):
    """ログインレスポンス"""

    access_token: str = Field(..., description="JWTアクセストークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    user: UserResponse = Field(..., description="ユーザー情報")


class TokenData(BaseModel):
    """トークンペイロードデータ"""

    username: str | None = None
    role: str | None = None
