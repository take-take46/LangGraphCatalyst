"""
LangGraph Catalyst - Security Module

JWT認証やパスワードハッシュなどのセキュリティ関連機能を提供します。
将来のユーザー認証機能で使用予定。
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import Settings, get_settings

# パスワードハッシュ用コンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: dict[str, Any],
    settings: Settings | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    JWTアクセストークンを生成

    Args:
        data: トークンに含めるデータ（ユーザーID等）
        settings: 設定インスタンス（Noneの場合は自動取得）
        expires_delta: トークン有効期限（Noneの場合は設定値を使用）

    Returns:
        JWTトークン文字列
    """
    if settings is None:
        settings = get_settings()

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def verify_token(token: str, settings: Settings | None = None) -> dict[str, Any] | None:
    """
    JWTトークンを検証

    Args:
        token: 検証するJWTトークン
        settings: 設定インスタンス（Noneの場合は自動取得）

    Returns:
        トークンのペイロード（検証失敗時はNone）
    """
    if settings is None:
        settings = get_settings()

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return payload
    except JWTError:
        return None


def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化

    Args:
        password: ハッシュ化するパスワード

    Returns:
        ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    パスワードを検証

    Args:
        plain_password: 検証する平文パスワード
        hashed_password: ハッシュ化されたパスワード

    Returns:
        パスワードが一致する場合True
    """
    return pwd_context.verify(plain_password, hashed_password)
