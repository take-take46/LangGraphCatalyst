"""
LangGraph Catalyst - Backend API Configuration

FastAPI用の設定管理モジュール。
既存のsrc/config/settings.pyの設定を流用しつつ、FastAPI固有の設定を追加します。
"""

import logging
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """FastAPI アプリケーション設定クラス"""

    # OpenAI API設定
    openai_api_key: str = Field(
        ...,
        description="OpenAI API Key",
        min_length=1,
    )

    # Chroma Vector DB設定
    chroma_persist_dir: str = Field(
        default="./data/chroma",
        description="Chromaベクトルストアの永続化ディレクトリ",
    )

    # ログ設定
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="ログレベル",
    )

    # LLM設定
    default_llm_model: str = Field(
        default="gpt-4-turbo-preview",
        description="デフォルトのLLMモデル",
    )

    default_embedding_model: str = Field(
        default="text-embedding-3-small",
        description="デフォルトの埋め込みモデル",
    )

    max_tokens: int = Field(
        default=4096,
        ge=1,
        le=128000,
        description="最大トークン数",
    )

    temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="LLMの温度パラメータ",
    )

    # 環境設定
    environment: Literal["development", "test", "production"] = Field(
        default="development",
        description="実行環境",
    )

    # FastAPI設定
    api_title: str = Field(
        default="LangGraph Catalyst API",
        description="API タイトル",
    )

    api_version: str = Field(
        default="1.0.0",
        description="API バージョン",
    )

    api_description: str = Field(
        default="LangGraph学習支援とビジネス活用を促進するAPI",
        description="API 説明",
    )

    # CORS設定
    cors_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="CORS許可オリジン（カンマ区切り）",
    )

    cors_allow_credentials: bool = Field(
        default=True,
        description="CORS資格情報許可",
    )

    # JWT設定（将来のユーザー認証用）
    jwt_secret_key: str = Field(
        default="your-secret-key-change-in-production",
        description="JWT署名用秘密鍵",
    )

    jwt_algorithm: str = Field(
        default="HS256",
        description="JWTアルゴリズム",
    )

    jwt_access_token_expire_minutes: int = Field(
        default=1440,  # 24時間
        ge=1,
        description="JWTアクセストークン有効期限（分）",
    )

    # RAG設定
    rag_top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="RAG検索で取得する上位k件",
    )

    rag_chunk_size: int = Field(
        default=800,
        ge=100,
        le=5000,
        description="ドキュメント分割のチャンクサイズ",
    )

    rag_chunk_overlap: int = Field(
        default=150,
        ge=0,
        le=1000,
        description="ドキュメント分割のオーバーラップサイズ",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("chroma_persist_dir")
    @classmethod
    def create_chroma_dir(cls, v: str) -> str:
        """Chromaディレクトリが存在しない場合は作成"""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return v

    def setup_logging(self) -> None:
        """ログ設定をセットアップ"""
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @property
    def is_production(self) -> bool:
        """本番環境かどうかを判定"""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """開発環境かどうかを判定"""
        return self.environment == "development"

    @property
    def cors_origins_list(self) -> list[str]:
        """CORS許可オリジンをリストとして取得"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# 設定インスタンスを返す依存性注入用関数
@lru_cache
def get_settings() -> Settings:
    """
    設定インスタンスを取得する依存性注入用関数

    FastAPIの Depends() で使用します。
    lru_cacheでシングルトン化し、同じインスタンスを返します。
    """
    return Settings()


# グローバル設定インスタンス（互換性のため）
settings = Settings()

# ログ設定を初期化
settings.setup_logging()
