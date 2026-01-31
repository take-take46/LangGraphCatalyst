"""
LangGraph Catalyst - Helper Functions

ユーティリティ関数を提供するモジュール。
テキスト分割、ログ設定、エラーハンドリングなど。
"""

import logging
import os
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


def extract_code_blocks(text: str, language: str | None = None) -> list[str] | list[dict[str, str]]:
    """
    テキストからコードブロックを抽出（言語情報付き）

    Args:
        text: 元のテキスト
        language: フィルタリングする言語（Noneの場合は全て）

    Returns:
        list[str] | list[dict]: コードブロックのリスト
            - languageが指定された場合: list[str]（該当言語のコードのみ）
            - languageが指定されていない場合: list[dict]（全コードブロック、language/code付き）
    """
    code_blocks_all = []
    lines = text.split("\n")
    in_code_block = False
    current_block = []
    current_language = None  # デフォルトなし

    for line in lines:
        if line.strip().startswith("```"):
            if in_code_block:
                # コードブロック終了
                if current_block:
                    code_blocks_all.append(
                        {
                            "language": current_language or "unknown",
                            "code": "\n".join(current_block)
                        }
                    )
                current_block = []
                in_code_block = False
                current_language = None
            else:
                # コードブロック開始
                in_code_block = True
                # 言語情報を抽出（```python, ```typescript等）
                lang_info = line.strip()[3:].strip().lower()
                if lang_info:
                    current_language = lang_info
        elif in_code_block:
            current_block.append(line)

    # 言語でフィルタリング（指定された場合）
    if language:
        filtered_blocks = [
            block["code"]
            for block in code_blocks_all
            if block["language"] == language.lower()
        ]
        return filtered_blocks
    else:
        # 辞書のリストを返す
        return code_blocks_all


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


def split_text_into_chunks(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    separator: str = "\n\n",
) -> list[str]:
    """
    テキストをチャンクに分割（文字列版）

    Args:
        text: 分割するテキスト
        chunk_size: チャンクサイズ
        chunk_overlap: オーバーラップサイズ
        separator: セパレータ（使用されない、後方互換性のため）

    Returns:
        list[str]: 分割されたテキストのリスト

    Raises:
        ValueError: chunk_sizeが0以下の場合
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    # chunk_overlapがchunk_sizeより大きい場合は調整
    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size - 1)

    text_splitter = create_text_splitter(chunk_size, chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks


def calculate_token_count(text: str, encoding_name: str = "cl100k_base") -> int:
    """
    テキストのトークン数を計算

    Args:
        text: トークン数を計算するテキスト
        encoding_name: エンコーディング名

    Returns:
        int: トークン数
    """
    try:
        import tiktoken

        encoding = tiktoken.get_encoding(encoding_name)
        tokens = encoding.encode(text)
        return len(tokens)
    except ImportError:
        # tiktokenがインストールされていない場合は概算
        # 平均的に1トークン ≈ 4文字
        return len(text) // 4


def format_source_metadata(metadata: dict[str, Any]) -> str:
    """
    ソースメタデータをフォーマット

    Args:
        metadata: メタデータ辞書

    Returns:
        str: フォーマットされたメタデータ
    """
    parts = []
    if "title" in metadata:
        parts.append(f"Title: {metadata['title']}")
    if "source" in metadata:
        parts.append(f"Source: {metadata['source']}")
    if "doc_type" in metadata:
        parts.append(f"Type: {metadata['doc_type']}")
    if "updated_at" in metadata:
        parts.append(f"Updated: {metadata['updated_at']}")

    return " | ".join(parts) if parts else "No metadata"


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    ファイル名をサニタイズ

    Args:
        filename: 元のファイル名
        max_length: 最大長

    Returns:
        str: サニタイズされたファイル名
    """
    import re

    # 危険な文字を除去
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", filename)

    # パストラバーサル攻撃を防ぐ
    sanitized = sanitized.replace("..", "")
    sanitized = sanitized.strip(". ")

    # 最大長に切り詰め
    if len(sanitized) > max_length:
        name, ext = os.path.splitext(sanitized)
        max_name_length = max_length - len(ext)
        sanitized = name[:max_name_length] + ext

    return sanitized or "untitled"


def parse_mermaid_diagram(mermaid_code: str) -> dict[str, Any]:
    """
    Mermaid図をパースして構造化データに変換

    Args:
        mermaid_code: Mermaid記法のコード

    Returns:
        dict: パースされた構造
    """
    import re

    result = {
        "diagram_type": None,
        "nodes": [],
        "edges": [],
        "valid": False,
    }

    if not mermaid_code or not mermaid_code.strip():
        return result

    lines = mermaid_code.strip().split("\n")

    if not lines:
        return result

    # ダイアグラムタイプを抽出
    first_line = lines[0].strip()
    if "flowchart" in first_line or "graph" in first_line:
        result["diagram_type"] = "flowchart"
    elif "sequenceDiagram" in first_line:
        result["diagram_type"] = "sequence"
    else:
        return result

    # ノードとエッジを抽出（簡単なパーサー）
    node_pattern = re.compile(r"^\s*([A-Za-z0-9_]+)[\[\(\{](.+?)[\]\)\}]")
    edge_pattern = re.compile(r"^\s*([A-Za-z0-9_]+)\s*-->\s*([A-Za-z0-9_]+)")

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        # ノードのマッチ
        node_match = node_pattern.match(line)
        if node_match:
            result["nodes"].append(
                {"id": node_match.group(1), "label": node_match.group(2)}
            )

        # エッジのマッチ
        edge_match = edge_pattern.match(line)
        if edge_match:
            result["edges"].append(
                {"from": edge_match.group(1), "to": edge_match.group(2)}
            )

    result["valid"] = len(result["nodes"]) > 0 or len(result["edges"]) > 0

    return result
