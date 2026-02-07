"""
LangGraph Catalyst - User Management

環境変数ベースのユーザー管理システム。
DBを使用せず、4ユーザー（開発者1名 + テストユーザー3名）を管理。
"""

import os

from passlib.context import CryptContext

# パスワードハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    """ユーザークラス"""

    def __init__(
        self,
        username: str,
        password_hash: str,
        role: str,
        daily_limit: int | None = None,
    ):
        self.username = username
        self.password_hash = password_hash
        self.role = role  # "admin" または "user"
        self.daily_limit = daily_limit  # None = 無制限


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証"""
    return pwd_context.verify(plain_password, hashed_password)


def initialize_users() -> dict[str, User]:
    """
    環境変数からユーザー情報を読み込んで初期化

    環境変数:
        ADMIN_PASSWORD: 開発者パスワード
        TESTUSER1_PASSWORD: テストユーザー1のパスワード
        TESTUSER2_PASSWORD: テストユーザー2のパスワード
        TESTUSER3_PASSWORD: テストユーザー3のパスワード

    Returns:
        ユーザー名→Userオブジェクトのマッピング
    """
    users = {}

    # 開発者（管理者）
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # デフォルトは開発用
    users["admin"] = User(
        username="admin",
        password_hash=get_password_hash(admin_password),
        role="admin",
        daily_limit=None,  # 無制限
    )

    # テストユーザー1
    testuser1_password = os.getenv("TESTUSER1_PASSWORD", "test123")
    users["testuser1"] = User(
        username="testuser1",
        password_hash=get_password_hash(testuser1_password),
        role="user",
        daily_limit=5,
    )

    # テストユーザー2
    testuser2_password = os.getenv("TESTUSER2_PASSWORD", "test123")
    users["testuser2"] = User(
        username="testuser2",
        password_hash=get_password_hash(testuser2_password),
        role="user",
        daily_limit=5,
    )

    # テストユーザー3
    testuser3_password = os.getenv("TESTUSER3_PASSWORD", "test123")
    users["testuser3"] = User(
        username="testuser3",
        password_hash=get_password_hash(testuser3_password),
        role="user",
        daily_limit=5,
    )

    return users


# グローバルユーザーデータベース（アプリ起動時に初期化）
USERS_DB = initialize_users()


def get_user(username: str) -> User | None:
    """ユーザー名でユーザーを取得"""
    return USERS_DB.get(username)


def authenticate_user(username: str, password: str) -> User | None:
    """
    ユーザー認証

    Args:
        username: ユーザー名
        password: 平文パスワード

    Returns:
        認証成功時はUserオブジェクト、失敗時はNone
    """
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
