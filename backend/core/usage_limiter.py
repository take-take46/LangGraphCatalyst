"""
LangGraph Catalyst - Usage Limiter

ユーザーの使用回数制限を管理するモジュール。
ファイルベースでカウンターを管理（Render無料プランでは再起動時にリセット）。
"""

import json
from datetime import date
from pathlib import Path

from fastapi import HTTPException, status

from backend.core.users import User

# 使用制限データファイルのパス
USAGE_LIMITS_FILE = Path("data/usage_limits.json")


def _ensure_data_dir() -> None:
    """dataディレクトリが存在しない場合は作成"""
    USAGE_LIMITS_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_usage_data() -> dict:
    """
    使用制限データをファイルから読み込む

    Returns:
        ユーザー名→使用データのマッピング
        例: {"testuser1": {"date": "2026-01-28", "count": 3}}
    """
    _ensure_data_dir()

    if not USAGE_LIMITS_FILE.exists():
        return {}

    try:
        with open(USAGE_LIMITS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_usage_data(data: dict) -> None:
    """
    使用制限データをファイルに保存

    Args:
        data: ユーザー名→使用データのマッピング
    """
    _ensure_data_dir()

    try:
        with open(USAGE_LIMITS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        # 保存失敗時はログを出力（ただしエラーは投げない）
        print(f"Warning: Failed to save usage data: {e}")


def get_remaining_usage(user: User) -> int | None:
    """
    ユーザーの残り使用回数を取得

    Args:
        user: ユーザーオブジェクト

    Returns:
        残り使用回数（無制限の場合はNone）
    """
    # 管理者は無制限
    if user.daily_limit is None:
        return None

    usage_data = _load_usage_data()
    today = date.today().isoformat()

    user_usage = usage_data.get(user.username, {})

    # 日付が変わったらカウントリセット
    if user_usage.get("date") != today:
        return user.daily_limit

    used_count = user_usage.get("count", 0)
    remaining = user.daily_limit - used_count

    return max(0, remaining)


def check_usage_limit(user: User) -> bool:
    """
    ユーザーが使用制限内かチェック

    Args:
        user: ユーザーオブジェクト

    Returns:
        True: 使用可能、False: 制限超過

    Raises:
        HTTPException: 使用制限超過時（429 Too Many Requests）
    """
    # 管理者は無制限
    if user.daily_limit is None:
        return True

    remaining = get_remaining_usage(user)

    if remaining == 0:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"本日の使用回数上限（{user.daily_limit}回）に達しました。明日以降に再度お試しください。",
        )

    return True


def increment_usage(user: User) -> None:
    """
    ユーザーの使用回数をインクリメント

    Args:
        user: ユーザーオブジェクト
    """
    # 管理者は記録しない
    if user.daily_limit is None:
        return

    usage_data = _load_usage_data()
    today = date.today().isoformat()

    user_usage = usage_data.get(user.username, {})

    # 日付が変わったらリセット
    if user_usage.get("date") != today:
        user_usage = {"date": today, "count": 0}

    user_usage["count"] += 1
    usage_data[user.username] = user_usage

    _save_usage_data(usage_data)
