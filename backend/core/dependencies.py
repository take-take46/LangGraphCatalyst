"""
LangGraph Catalyst - Dependency Injection

認証や使用制限のための依存性注入関数。
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.core.config import Settings, get_settings
from backend.core.security import verify_token
from backend.core.usage_limiter import check_usage_limit, increment_usage
from backend.core.users import User, get_user
from backend.schemas.auth import TokenData

# OAuth2スキーム（トークンエンドポイントを指定）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> User:
    """
    JWTトークンから現在のユーザーを取得する依存性注入関数

    Args:
        token: JWTアクセストークン
        settings: アプリケーション設定（依存性注入）

    Returns:
        認証されたユーザーオブジェクト

    Raises:
        HTTPException: 認証失敗時（401 Unauthorized）
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証に失敗しました",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # トークン検証（settingsを明示的に渡す）
    payload = verify_token(token, settings)
    if payload is None:
        raise credentials_exception

    # ユーザー名を取得
    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception

    token_data = TokenData(username=username, role=payload.get("role"))

    # ユーザーを取得
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


# 型アノテーション用のエイリアス
CurrentUser = Annotated[User, Depends(get_current_user)]


async def require_usage_limit(current_user: CurrentUser) -> User:
    """
    使用制限をチェックする依存性注入関数

    LLMを使用するエンドポイント（RAG、Architect）で使用します。
    使用制限チェック後、使用回数をインクリメントします。

    Args:
        current_user: 認証されたユーザー（依存性注入）

    Returns:
        ユーザーオブジェクト

    Raises:
        HTTPException: 使用制限超過時（429 Too Many Requests）
    """
    # 使用制限チェック（超過時は例外を投げる）
    check_usage_limit(current_user)

    # 使用回数インクリメント
    increment_usage(current_user)

    return current_user


# LLM使用エンドポイント用の型アノテーション
UserWithUsageLimit = Annotated[User, Depends(require_usage_limit)]
