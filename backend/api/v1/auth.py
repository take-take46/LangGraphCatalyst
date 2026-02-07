"""
LangGraph Catalyst - Authentication API Endpoints

ユーザー認証のためのAPIエンドポイント。
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.core.dependencies import CurrentUser
from backend.core.security import create_access_token
from backend.core.users import authenticate_user
from backend.schemas.auth import LoginResponse, UserResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="ログイン",
    description="ユーザー名とパスワードでログインし、JWTアクセストークンを取得します",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> LoginResponse:
    """
    ログインエンドポイント

    Args:
        form_data: ユーザー名とパスワードを含むフォームデータ

    Returns:
        JWTアクセストークンとユーザー情報

    Raises:
        HTTPException: 認証失敗時（401 Unauthorized）
    """
    # ユーザー認証
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWTトークン生成
    access_token = create_access_token(data={"sub": user.username, "role": user.role})

    # レスポンス作成
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            username=user.username,
            role=user.role,
            daily_limit=user.daily_limit,
        ),
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="現在のユーザー情報取得",
    description="JWTトークンから現在ログイン中のユーザー情報を取得します",
)
async def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """
    現在のユーザー情報取得エンドポイント

    Args:
        current_user: 認証されたユーザー（依存性注入）

    Returns:
        ユーザー情報
    """
    return UserResponse(
        username=current_user.username,
        role=current_user.role,
        daily_limit=current_user.daily_limit,
    )


@router.post(
    "/logout",
    summary="ログアウト",
    description="ログアウト（フロントエンドでトークンを削除）",
)
async def logout() -> dict[str, str]:
    """
    ログアウトエンドポイント

    Note:
        JWTは状態を持たないため、サーバー側での無効化は不要。
        フロントエンドでトークンを削除することでログアウトします。

    Returns:
        成功メッセージ
    """
    return {"message": "ログアウトしました"}
