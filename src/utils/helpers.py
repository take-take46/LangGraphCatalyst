"""
LangGraph Catalyst - Helper Functions

ユーティリティ関数を提供するモジュール。
テキスト分割、ログ設定、エラーハンドリングなど。
"""

import logging
from datetime import datetime
from typing import Any

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.settings import settings

logger = logging.getLogger(__name__)


def create_text_splitter(
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> RecursiveCharacterTextSplitter:
    """
    RecursiveCharacterTextSplitterを作成

    Args:
        chunk_size: チャンクサイズ（デフォルトは設定から取得）
        chunk_overlap: オーバーラップサイズ（デフォルトは設定から取得）

    Returns:
        RecursiveCharacterTextSplitter: テキスト分割器
    """
    chunk_size = chunk_size or settings.rag_chunk_size
    chunk_overlap = chunk_overlap or settings.rag_chunk_overlap

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )


def split_documents(
    documents: list[Document],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[Document]:
    """
    ドキュメントを分割

    Args:
        documents: 分割するドキュメントのリスト
        chunk_size: チャンクサイズ
        chunk_overlap: オーバーラップサイズ

    Returns:
        list[Document]: 分割されたドキュメントのリスト
    """
    text_splitter = create_text_splitter(chunk_size, chunk_overlap)
    splits = text_splitter.split_documents(documents)

    logger.info(f"Split {len(documents)} documents into {len(splits)} chunks")

    return splits


def get_current_timestamp() -> str:
    """
    現在のタイムスタンプをISO 8601形式で取得

    Returns:
        str: ISO 8601形式のタイムスタンプ
    """
    return datetime.utcnow().isoformat() + "Z"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    テキストを指定の長さに切り詰める

    Args:
        text: 元のテキスト
        max_length: 最大長

    Returns:
        str: 切り詰められたテキスト
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_sources(documents: list[Document]) -> list[dict[str, Any]]:
    """
    ドキュメントをソース情報の形式に変換

    Args:
        documents: ドキュメントのリスト

    Returns:
        list[dict]: ソース情報のリスト
    """
    sources = []
    for doc in documents:
        source = {
            "title": doc.metadata.get("title", "Untitled"),
            "url": doc.metadata.get("source", ""),
            "excerpt": truncate_text(doc.page_content, 200),
            "doc_type": doc.metadata.get("doc_type", "unknown"),
        }
        sources.append(source)

    return sources


def extract_code_blocks(text: str) -> list[dict[str, str]]:
    """
    テキストからコードブロックを抽出（言語情報付き）

    Args:
        text: 元のテキスト

    Returns:
        list[dict]: コードブロック情報のリスト
            - language: プログラミング言語（python, typescript等）
            - code: コードの内容
    """
    code_blocks = []
    lines = text.split("\n")
    in_code_block = False
    current_block = []
    current_language = "python"  # デフォルト

    for line in lines:
        if line.strip().startswith("```"):
            if in_code_block:
                # コードブロック終了
                if current_block:
                    code_blocks.append(
                        {"language": current_language, "code": "\n".join(current_block)}
                    )
                current_block = []
                in_code_block = False
                current_language = "python"
            else:
                # コードブロック開始
                in_code_block = True
                # 言語情報を抽出（```python, ```typescript等）
                lang_info = line.strip()[3:].strip().lower()
                if lang_info:
                    current_language = lang_info
        elif in_code_block:
            current_block.append(line)

    return code_blocks


def safe_get(dictionary: dict[str, Any], key: str, default: Any = None) -> Any:
    """
    辞書から安全に値を取得

    Args:
        dictionary: 辞書
        key: キー
        default: デフォルト値

    Returns:
        Any: 値またはデフォルト値
    """
    try:
        return dictionary.get(key, default)
    except (AttributeError, KeyError):
        return default


def setup_logger(name: str, level: str | None = None) -> logging.Logger:
    """
    ロガーをセットアップ

    Args:
        name: ロガー名
        level: ログレベル

    Returns:
        logging.Logger: ロガーインスタンス
    """
    logger_instance = logging.getLogger(name)

    if level:
        logger_instance.setLevel(getattr(logging, level.upper()))
    else:
        logger_instance.setLevel(getattr(logging, settings.log_level))

    return logger_instance


def validate_url(url: str) -> bool:
    """
    URLの形式を検証

    Args:
        url: 検証するURL

    Returns:
        bool: 有効なURLの場合True
    """
    import re

    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return bool(url_pattern.match(url))
