"""
LangGraph Catalyst - Settings/Config Tests

設定クラスのユニットテスト
"""

import os
from pathlib import Path
from unittest.mock import Mock

import pytest
from pydantic import ValidationError as PydanticValidationError

from src.config.settings import Settings


@pytest.fixture
def mock_no_env_file():
    """
    .envファイルの読み込みを防ぐフィクスチャ

    テスト実行中、一時的に.envファイルを.env.bakにリネームし、
    テスト終了後に復元する。
    """
    import os
    from pathlib import Path

    env_file = Path(".env")
    env_backup = Path(".env.bak")

    # .envファイルが存在する場合は一時的にリネーム
    env_existed = env_file.exists()
    if env_existed:
        env_file.rename(env_backup)

    yield

    # テスト終了後に復元
    if env_existed and env_backup.exists():
        env_backup.rename(env_file)


@pytest.mark.unit
class TestSettings:
    """Settings設定クラスのテスト"""

    # ========================================================================
    # Initialization Tests
    # ========================================================================

    def test_settings_with_valid_env_vars(self, monkeypatch):
        """有効な環境変数での初期化テスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-valid-key")
        monkeypatch.setenv("CHROMA_PERSIST_DIR", "./tests/data/test_chroma")
        monkeypatch.setenv("LOG_LEVEL", "INFO")

        # Act
        settings = Settings()

        # Assert
        assert settings.openai_api_key == "sk-test-valid-key"
        assert settings.chroma_persist_dir == "./tests/data/test_chroma"
        assert settings.log_level == "INFO"

    def test_settings_missing_required_openai_api_key(self, monkeypatch, mock_no_env_file):
        """必須のOPENAI_API_KEYが欠損している場合のテスト"""
        # Arrange - OPENAI_API_KEYを設定しない
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # OPENAI_API_KEYが必須であることを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("openai_api_key",) for error in errors)

    def test_settings_with_defaults(self, monkeypatch, mock_no_env_file):
        """デフォルト値が正しく設定されるテスト"""
        # Arrange - 必須項目のみ設定
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")

        # Act
        settings = Settings()

        # Assert - デフォルト値を確認
        assert settings.chroma_persist_dir == "./data/chroma"
        assert settings.log_level == "INFO"
        assert settings.default_llm_model == "gpt-4-turbo-preview"
        assert settings.default_embedding_model == "text-embedding-3-small"
        assert settings.max_tokens == 4096
        assert settings.temperature == 0.1
        assert settings.environment == "development"
        assert settings.streamlit_server_port == 8501
        assert settings.rag_top_k == 3
        assert settings.rag_chunk_size == 800
        assert settings.rag_chunk_overlap == 150

    def test_settings_custom_values(self, monkeypatch):
        """カスタム値が正しく設定されるテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-custom-key")
        monkeypatch.setenv("DEFAULT_LLM_MODEL", "gpt-4")
        monkeypatch.setenv("TEMPERATURE", "0.7")
        monkeypatch.setenv("MAX_TOKENS", "8000")
        monkeypatch.setenv("ENVIRONMENT", "production")

        # Act
        settings = Settings()

        # Assert
        assert settings.openai_api_key == "sk-custom-key"
        assert settings.default_llm_model == "gpt-4"
        assert settings.temperature == 0.7
        assert settings.max_tokens == 8000
        assert settings.environment == "production"

    # ========================================================================
    # Validation Tests
    # ========================================================================

    def test_settings_invalid_log_level(self, monkeypatch):
        """無効なログレベルのテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("LOG_LEVEL", "INVALID_LEVEL")

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # LOG_LEVELのバリデーションエラーを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("log_level",) for error in errors)

    def test_settings_invalid_environment(self, monkeypatch):
        """無効な環境設定のテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("ENVIRONMENT", "invalid_env")

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # ENVIRONMENTのバリデーションエラーを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("environment",) for error in errors)

    def test_settings_max_tokens_out_of_range(self, monkeypatch):
        """MAX_TOKENSが範囲外のテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("MAX_TOKENS", "200000")  # 範囲外

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # MAX_TOKENSのバリデーションエラーを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("max_tokens",) for error in errors)

    def test_settings_temperature_out_of_range(self, monkeypatch):
        """TEMPERATUREが範囲外のテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("TEMPERATURE", "3.0")  # 範囲外

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # TEMPERATUREのバリデーションエラーを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("temperature",) for error in errors)

    def test_settings_port_out_of_range(self, monkeypatch):
        """ポート番号が範囲外のテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("STREAMLIT_SERVER_PORT", "70000")  # 範囲外

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # STREAMLIT_SERVER_PORTのバリデーションエラーを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("streamlit_server_port",) for error in errors)

    # ========================================================================
    # Field Validator Tests
    # ========================================================================

    def test_settings_chroma_dir_creation(self, monkeypatch, tmp_path):
        """Chromaディレクトリが自動作成されるテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        test_dir = tmp_path / "test_chroma_dir"
        monkeypatch.setenv("CHROMA_PERSIST_DIR", str(test_dir))

        # ディレクトリが存在しないことを確認
        assert not test_dir.exists()

        # Act
        settings = Settings()

        # Assert - ディレクトリが作成されたことを確認
        assert test_dir.exists()
        assert test_dir.is_dir()

    # ========================================================================
    # Property Tests
    # ========================================================================

    def test_settings_is_production_property(self, monkeypatch):
        """is_productionプロパティのテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")

        # Act - production環境
        monkeypatch.setenv("ENVIRONMENT", "production")
        settings_prod = Settings()

        # Assert
        assert settings_prod.is_production is True
        assert settings_prod.is_development is False

    def test_settings_is_development_property(self, monkeypatch):
        """is_developmentプロパティのテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")

        # Act - development環境
        monkeypatch.setenv("ENVIRONMENT", "development")
        settings_dev = Settings()

        # Assert
        assert settings_dev.is_development is True
        assert settings_dev.is_production is False

    def test_settings_test_environment(self, monkeypatch):
        """test環境のテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("ENVIRONMENT", "test")

        # Act
        settings = Settings()

        # Assert
        assert settings.environment == "test"
        assert settings.is_production is False
        assert settings.is_development is False

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_settings_empty_api_key(self, monkeypatch):
        """空のAPI Keyのテスト"""
        # Arrange
        monkeypatch.setenv("OPENAI_API_KEY", "")

        # Act & Assert
        with pytest.raises(PydanticValidationError) as exc_info:
            Settings()

        # min_length=1のバリデーションエラーを確認
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("openai_api_key",) for error in errors)

    def test_settings_case_insensitive_env_vars(self, monkeypatch):
        """環境変数が大文字小文字を区別しないテスト"""
        # Arrange - 小文字で設定
        monkeypatch.setenv("openai_api_key", "sk-test-lowercase")
        monkeypatch.setenv("log_level", "ERROR")

        # Act
        settings = Settings()

        # Assert - 正しく読み込まれることを確認
        assert settings.openai_api_key == "sk-test-lowercase"
        assert settings.log_level == "ERROR"
