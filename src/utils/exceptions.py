"""
LangGraph Catalyst - Custom Exceptions

カスタム例外クラスを定義するモジュール。
"""


class CatalystException(Exception):
    """基底例外クラス"""

    pass


class VectorStoreError(CatalystException):
    """ベクトルストア関連エラー"""

    pass


class LLMError(CatalystException):
    """LLM呼び出しエラー"""

    pass


class CrawlerError(CatalystException):
    """クローラーエラー"""

    pass


class ValidationError(CatalystException):
    """バリデーションエラー"""

    pass


class ConfigurationError(CatalystException):
    """設定エラー"""

    pass
