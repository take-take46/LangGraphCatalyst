"""
LangGraph Catalyst - Settings Module

環境変数と設定を管理するPydantic Settingsクラス。
型安全な設定管理を提供します。
"""

import logging
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """アプリケーション設定クラス"""

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
        default=0.1,
        ge=0.0,
        le=2.0,
        description="LLMの温度パラメータ",
    )

    # 環境設定
    environment: Literal["development", "test", "production"] = Field(
        default="development",
        description="実行環境",
    )

    # Streamlit設定
    streamlit_server_port: int = Field(
        default=8501,
        ge=1,
        le=65535,
        description="Streamlitサーバーのポート",
    )

    # RAG設定
    rag_top_k: int = Field(
        default=3,
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


# グローバル設定インスタンス
settings = Settings()

# ログ設定を初期化
settings.setup_logging()
