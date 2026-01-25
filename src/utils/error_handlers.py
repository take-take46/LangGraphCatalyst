"""
LangGraph Catalyst - Error Handlers

エラーハンドリングを一元管理するモジュール
"""

import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from openai import APIError, RateLimitError, APIConnectionError
from src.utils.exceptions import (
    CatalystException,
    LLMError,
    VectorStoreError,
    CrawlerError,
    ValidationError,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_on_error(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (APIError, APIConnectionError),
):
    """
    エラー発生時にリトライするデコレータ

    Args:
        max_retries: 最大リトライ回数
        initial_delay: 初回待機時間（秒）
        backoff_factor: 待機時間の増加率
        exceptions: リトライ対象の例外タプル

    Returns:
        デコレータ関数
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}"
                        )

            # すべてのリトライが失敗した場合
            raise last_exception

        return wrapper

    return decorator


def handle_llm_errors(func: Callable[..., T]) -> Callable[..., T]:
    """
    LLM関連のエラーをキャッチして適切なエラーに変換するデコレータ

    Args:
        func: デコレートする関数

    Returns:
        デコレートされた関数
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            logger.error(f"OpenAI rate limit exceeded: {e}")
            raise LLMError(
                "APIのレート制限に達しました。しばらく待ってから再度お試しください。"
            ) from e
        except APIConnectionError as e:
            logger.error(f"OpenAI API connection error: {e}")
            raise LLMError("APIへの接続に失敗しました。ネットワーク接続を確認してください。") from e
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise LLMError(f"APIエラーが発生しました: {str(e)}") from e
        except ValidationError:
            # ValidationErrorはそのまま伝播
            raise
        except CatalystException:
            # 既知のカスタム例外はそのまま伝播
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}", exc_info=True)
            raise LLMError(f"予期しないエラーが発生しました: {str(e)}") from e

    return wrapper


def handle_vectorstore_errors(func: Callable[..., T]) -> Callable[..., T]:
    """
    ベクトルストア関連のエラーをキャッチするデコレータ

    Args:
        func: デコレートする関数

    Returns:
        デコレートされた関数
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except VectorStoreError:
            # VectorStoreErrorはそのまま伝播
            raise
        except Exception as e:
            logger.error(f"Vector store error in {func.__name__}: {e}", exc_info=True)
            raise VectorStoreError(f"ベクトルストアでエラーが発生しました: {str(e)}") from e

    return wrapper


def get_user_friendly_error_message(error: Exception) -> str:
    """
    ユーザーフレンドリーなエラーメッセージを取得

    Args:
        error: 発生した例外

    Returns:
        ユーザー向けのエラーメッセージ
    """
    if isinstance(error, ValidationError):
        return f"入力エラー: {str(error)}"

    elif isinstance(error, LLMError):
        error_str = str(error)
        if "rate limit" in error_str.lower():
            return "APIのレート制限に達しました。しばらく待ってから再度お試しください。"
        elif "connection" in error_str.lower():
            return "API接続エラーが発生しました。ネットワーク接続を確認してください。"
        else:
            return f"AI処理中にエラーが発生しました: {error_str}"

    elif isinstance(error, VectorStoreError):
        return f"データベースエラーが発生しました: {str(error)}"

    elif isinstance(error, CrawlerError):
        return f"ドキュメント取得中にエラーが発生しました: {str(error)}"

    elif isinstance(error, CatalystException):
        return f"エラーが発生しました: {str(error)}"

    else:
        logger.error(f"Unexpected error type: {type(error).__name__}", exc_info=True)
        return "予期しないエラーが発生しました。しばらく待ってから再度お試しください。"


def validate_input(
    value: Any,
    field_name: str,
    required: bool = True,
    min_length: int | None = None,
    max_length: int | None = None,
    allowed_types: tuple | None = None,
) -> None:
    """
    入力値のバリデーション

    Args:
        value: バリデーション対象の値
        field_name: フィールド名
        required: 必須かどうか
        min_length: 最小長（文字列の場合）
        max_length: 最大長（文字列の場合）
        allowed_types: 許可される型のタプル

    Raises:
        ValidationError: バリデーションエラー
    """
    # 必須チェック
    if required and (value is None or (isinstance(value, str) and not value.strip())):
        raise ValidationError(f"{field_name}は必須です")

    # 型チェック
    if allowed_types and value is not None:
        if not isinstance(value, allowed_types):
            raise ValidationError(
                f"{field_name}の型が不正です。期待: {allowed_types}, 実際: {type(value)}"
            )

    # 文字列長チェック
    if isinstance(value, str):
        if min_length is not None and len(value) < min_length:
            raise ValidationError(f"{field_name}は{min_length}文字以上である必要があります")

        if max_length is not None and len(value) > max_length:
            raise ValidationError(f"{field_name}は{max_length}文字以下である必要があります")


class ErrorContext:
    """エラーコンテキストマネージャー"""

    def __init__(self, operation_name: str, user_friendly_message: str | None = None):
        """
        初期化

        Args:
            operation_name: 操作名
            user_friendly_message: ユーザー向けメッセージ
        """
        self.operation_name = operation_name
        self.user_friendly_message = user_friendly_message or f"{operation_name}中にエラーが発生しました"

    def __enter__(self):
        logger.debug(f"Starting operation: {self.operation_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.error(
                f"Error in {self.operation_name}: {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb),
            )

            # カスタム例外の場合はそのまま伝播
            if isinstance(exc_val, CatalystException):
                return False

            # その他の例外は適切なカスタム例外に変換
            if exc_type.__name__ in ["APIError", "RateLimitError", "APIConnectionError"]:
                raise LLMError(self.user_friendly_message) from exc_val
            else:
                raise CatalystException(self.user_friendly_message) from exc_val

        logger.debug(f"Successfully completed operation: {self.operation_name}")
        return False
