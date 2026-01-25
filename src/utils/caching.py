"""
LangGraph Catalyst - Caching Utilities

キャッシング関連のユーティリティ
"""

import hashlib
import logging
from functools import wraps
from typing import Any, Callable, TypeVar

import streamlit as st

logger = logging.getLogger(__name__)

T = TypeVar("T")


def get_vectorstore_cached():
    """
    ベクトルストアをキャッシュして取得

    Streamlitのst.cache_resourceを使用して、
    アプリケーション全体で共有されるベクトルストアをキャッシュします。

    Returns:
        ChromaVectorStore: キャッシュされたベクトルストア
    """
    from src.features.rag.vectorstore import ChromaVectorStore

    @st.cache_resource(show_spinner=False)
    def _create_vectorstore():
        logger.info("Creating new vectorstore instance (cached)")
        return ChromaVectorStore()

    return _create_vectorstore()


def get_rag_chain_cached():
    """
    RAGチェーンをキャッシュして取得

    Returns:
        RAGChain: キャッシュされたRAGチェーン
    """
    from src.features.rag.chain import RAGChain

    @st.cache_resource(show_spinner=False)
    def _create_rag_chain():
        logger.info("Creating new RAG chain instance (cached)")
        vectorstore = get_vectorstore_cached()
        return RAGChain(vectorstore=vectorstore)

    return _create_rag_chain()


def get_architect_graph_cached():
    """
    構成案生成グラフをキャッシュして取得

    Returns:
        ArchitectGraph: キャッシュされた構成案生成グラフ
    """
    from src.features.architect.graph import ArchitectGraph

    @st.cache_resource(show_spinner=False)
    def _create_architect_graph():
        logger.info("Creating new architect graph instance (cached)")
        return ArchitectGraph()

    return _create_architect_graph()


def cache_rag_query_result(query: str, k: int = 5, ttl: int = 3600):
    """
    RAGクエリ結果をキャッシュするデコレータ

    Args:
        query: クエリ文字列
        k: 検索する関連ドキュメント数
        ttl: キャッシュの有効期限（秒）

    Returns:
        デコレータ関数
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @st.cache_data(ttl=ttl, show_spinner=False)
        def cached_func(*args, **kwargs) -> T:
            logger.debug(f"Caching RAG query result for: {query[:50]}...")
            return func(*args, **kwargs)

        return cached_func

    return decorator


def generate_cache_key(*args, **kwargs) -> str:
    """
    引数からキャッシュキーを生成

    Args:
        *args: 位置引数
        **kwargs: キーワード引数

    Returns:
        str: ハッシュ化されたキャッシュキー
    """
    # 引数を文字列に変換してソート
    args_str = str(args)
    kwargs_str = str(sorted(kwargs.items()))

    # ハッシュ化
    combined = args_str + kwargs_str
    return hashlib.md5(combined.encode()).hexdigest()


class SimpleCache:
    """シンプルなインメモリキャッシュ"""

    def __init__(self, max_size: int = 100):
        """
        初期化

        Args:
            max_size: キャッシュの最大サイズ
        """
        self._cache: dict[str, Any] = {}
        self._max_size = max_size
        self._access_order: list[str] = []

    def get(self, key: str) -> Any | None:
        """
        キャッシュから値を取得

        Args:
            key: キャッシュキー

        Returns:
            キャッシュされた値、存在しない場合はNone
        """
        if key in self._cache:
            # アクセス順を更新（LRU）
            self._access_order.remove(key)
            self._access_order.append(key)
            logger.debug(f"Cache hit: {key}")
            return self._cache[key]

        logger.debug(f"Cache miss: {key}")
        return None

    def set(self, key: str, value: Any) -> None:
        """
        キャッシュに値を設定

        Args:
            key: キャッシュキー
            value: キャッシュする値
        """
        # 既存のキーの場合は削除
        if key in self._cache:
            self._access_order.remove(key)

        # サイズ制限チェック
        if len(self._cache) >= self._max_size:
            # 最も古いエントリを削除（LRU）
            oldest_key = self._access_order.pop(0)
            del self._cache[oldest_key]
            logger.debug(f"Cache eviction: {oldest_key}")

        # 新しいエントリを追加
        self._cache[key] = value
        self._access_order.append(key)
        logger.debug(f"Cache set: {key}")

    def clear(self) -> None:
        """キャッシュをクリア"""
        self._cache.clear()
        self._access_order.clear()
        logger.info("Cache cleared")

    def size(self) -> int:
        """キャッシュのサイズを取得"""
        return len(self._cache)


# グローバルキャッシュインスタンス
_global_cache = SimpleCache(max_size=100)


def get_global_cache() -> SimpleCache:
    """
    グローバルキャッシュを取得

    Returns:
        SimpleCache: グローバルキャッシュインスタンス
    """
    return _global_cache


def cached(cache_key_fn: Callable[..., str] | None = None):
    """
    関数の戻り値をキャッシュするデコレータ

    Args:
        cache_key_fn: キャッシュキーを生成する関数

    Returns:
        デコレータ関数
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # キャッシュキーを生成
            if cache_key_fn:
                key = cache_key_fn(*args, **kwargs)
            else:
                key = f"{func.__name__}:{generate_cache_key(*args, **kwargs)}"

            # キャッシュから取得
            cache = get_global_cache()
            cached_value = cache.get(key)

            if cached_value is not None:
                return cached_value

            # キャッシュにない場合は実行
            result = func(*args, **kwargs)

            # キャッシュに保存
            cache.set(key, result)

            return result

        return wrapper

    return decorator


def clear_all_caches():
    """すべてのキャッシュをクリア"""
    logger.info("Clearing all caches")

    # Streamlitキャッシュをクリア
    st.cache_data.clear()
    st.cache_resource.clear()

    # グローバルキャッシュをクリア
    get_global_cache().clear()

    logger.info("All caches cleared successfully")
