"""
LangGraph Catalyst - Vector Store

Chromaベクトルストアを管理するモジュール。
ドキュメントの埋め込み、検索、コレクション管理を提供します。
"""

import logging
from typing import Any

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from src.config.settings import settings
from src.utils.exceptions import VectorStoreError

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """Chromaベクトルストアの操作を管理するクラス"""

    def __init__(
        self,
        collection_name: str = "langgraph_docs",
        persist_directory: str | None = None,
        embedding_model: str | None = None,
    ):
        """
        ChromaVectorStoreの初期化

        Args:
            collection_name: コレクション名
            persist_directory: 永続化ディレクトリ
            embedding_model: 埋め込みモデル名

        Raises:
            VectorStoreError: 初期化エラー
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory or settings.chroma_persist_dir
        self.embedding_model_name = embedding_model or settings.default_embedding_model

        try:
            # OpenAI Embeddings初期化
            self.embeddings = OpenAIEmbeddings(
                model=self.embedding_model_name,
                openai_api_key=settings.openai_api_key,
            )

            # Chromaベクトルストア初期化
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )

            logger.info(f"Initialized ChromaVectorStore with collection: {self.collection_name}")

        except Exception as e:
            raise VectorStoreError(f"Failed to initialize vector store: {e}") from e

    def add_documents(self, documents: list[Document], batch_size: int = 100) -> dict[str, Any]:
        """
        ドキュメントをベクトルストアに追加

        Args:
            documents: 追加するドキュメントのリスト
            batch_size: バッチ処理サイズ

        Returns:
            dict: 追加結果の統計情報

        Raises:
            VectorStoreError: ドキュメント追加エラー
        """
        if not documents:
            logger.warning("No documents to add")
            return {
                "added_count": 0,
                "failed_count": 0,
                "total_documents_in_store": self._get_collection_count(),
                "status": "success",
            }

        logger.info(f"Adding {len(documents)} documents to vector store")

        try:
            added_count = 0
            failed_count = 0

            # バッチ処理でドキュメントを追加
            for i in range(0, len(documents), batch_size):
                batch = documents[i : i + batch_size]

                try:
                    self.vector_store.add_documents(documents=batch)
                    added_count += len(batch)
                    logger.debug(f"Added batch {i // batch_size + 1}: {len(batch)} documents")
                except Exception as e:
                    failed_count += len(batch)
                    logger.error(f"Failed to add batch {i // batch_size + 1}: {e}")

            total_in_store = self._get_collection_count()

            result = {
                "added_count": added_count,
                "failed_count": failed_count,
                "total_documents_in_store": total_in_store,
                "status": "success" if failed_count == 0 else "partial",
            }

            logger.info(
                f"Document addition completed. Added: {added_count}, Failed: {failed_count}, Total in store: {total_in_store}"
            )

            return result

        except Exception as e:
            raise VectorStoreError(f"Failed to add documents: {e}") from e

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[Document]:
        """
        類似度検索を実行

        Args:
            query: 検索クエリ
            k: 取得する上位k件
            filter_metadata: メタデータフィルタ

        Returns:
            list[Document]: 検索結果のドキュメントリスト

        Raises:
            VectorStoreError: 検索エラー
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []

        logger.info(f"Performing similarity search for query: {query[:50]}...")

        try:
            # フィルタなしの場合
            if filter_metadata is None:
                results = self.vector_store.similarity_search(query=query, k=k)
            else:
                # フィルタありの場合
                results = self.vector_store.similarity_search(
                    query=query, k=k, filter=filter_metadata
                )

            logger.info(f"Found {len(results)} similar documents")

            return results

        except Exception as e:
            raise VectorStoreError(f"Failed to perform similarity search: {e}") from e

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
        filter_metadata: dict[str, Any] | None = None,
    ) -> list[tuple[Document, float]]:
        """
        スコア付き類似度検索を実行

        Args:
            query: 検索クエリ
            k: 取得する上位k件
            filter_metadata: メタデータフィルタ

        Returns:
            list[tuple[Document, float]]: (ドキュメント, スコア)のリスト

        Raises:
            VectorStoreError: 検索エラー
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return []

        logger.info(f"Performing similarity search with score for query: {query[:50]}...")

        try:
            if filter_metadata is None:
                results = self.vector_store.similarity_search_with_score(query=query, k=k)
            else:
                results = self.vector_store.similarity_search_with_score(
                    query=query, k=k, filter=filter_metadata
                )

            logger.info(f"Found {len(results)} similar documents with scores")

            return results

        except Exception as e:
            raise VectorStoreError(f"Failed to perform similarity search with score: {e}") from e

    def delete_collection(self) -> bool:
        """
        コレクションを削除

        Returns:
            bool: 成功時True

        Raises:
            VectorStoreError: 削除エラー
        """
        logger.warning(f"Deleting collection: {self.collection_name}")

        try:
            self.vector_store.delete_collection()
            logger.info(f"Successfully deleted collection: {self.collection_name}")
            return True

        except Exception as e:
            raise VectorStoreError(f"Failed to delete collection: {e}") from e

    def get_collection_count(self) -> int:
        """
        コレクション内のドキュメント数を取得

        Returns:
            int: ドキュメント数
        """
        return self._get_collection_count()

    def _get_collection_count(self) -> int:
        """
        コレクション内のドキュメント数を取得（内部用）

        Returns:
            int: ドキュメント数
        """
        try:
            collection = self.vector_store._collection
            return collection.count()
        except Exception as e:
            logger.error(f"Failed to get collection count: {e}")
            return 0

    def as_retriever(self, search_kwargs: dict[str, Any] | None = None):
        """
        Retrieverとして取得

        Args:
            search_kwargs: 検索パラメータ

        Returns:
            Retriever: ベクトルストアのRetriever
        """
        if search_kwargs is None:
            search_kwargs = {"k": settings.rag_top_k}

        return self.vector_store.as_retriever(search_kwargs=search_kwargs)
