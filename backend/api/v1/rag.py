"""
LangGraph Catalyst - RAG API Endpoints

RAG学習支援機能のAPIエンドポイント。
既存のRAGChainロジックを呼び出します。
"""

import sys
import time
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.core.config import Settings, get_settings
from backend.core.dependencies import UserWithUsageLimit
from backend.schemas.rag import (
    CodeExampleResponse,
    RAGHealthResponse,
    RAGQueryMetadata,
    RAGQueryRequest,
    RAGQueryResponse,
    SourceResponse,
)
from src.features.rag.chain import RAGChain
from src.features.rag.vectorstore import ChromaVectorStore
from src.utils.exceptions import LLMError, ValidationError, VectorStoreError

router = APIRouter()


def get_vectorstore(settings: Settings = Depends(get_settings)) -> ChromaVectorStore:
    """
    VectorStoreインスタンスを取得する依存性注入

    Args:
        settings: アプリケーション設定

    Returns:
        ChromaVectorStoreインスタンス

    Raises:
        HTTPException: VectorStore初期化エラー
    """
    try:
        return ChromaVectorStore(
            persist_directory=settings.chroma_persist_dir,
            embedding_model=settings.default_embedding_model,
        )
    except VectorStoreError as e:
        raise HTTPException(
            status_code=500,
            detail=f"VectorStoreの初期化に失敗しました: {str(e)}",
        )


def get_rag_chain(
    vectorstore: ChromaVectorStore = Depends(get_vectorstore),
    settings: Settings = Depends(get_settings),
) -> RAGChain:
    """
    RAGChainインスタンスを取得する依存性注入

    Args:
        vectorstore: VectorStoreインスタンス
        settings: アプリケーション設定

    Returns:
        RAGChainインスタンス

    Raises:
        HTTPException: RAGChain初期化エラー
    """
    try:
        return RAGChain(
            vectorstore=vectorstore,
            llm_model=settings.default_llm_model,
            temperature=settings.temperature,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"RAGChainの初期化に失敗しました: {str(e)}",
        )


@router.post(
    "/rag/query",
    response_model=RAGQueryResponse,
    summary="RAGクエリ実行",
    description="LangGraphに関する質問に対してソース付きで回答します",
    responses={
        200: {"description": "成功"},
        400: {"description": "不正なリクエスト"},
        500: {"description": "サーバーエラー"},
    },
)
async def query_rag(
    request: RAGQueryRequest,
    current_user: UserWithUsageLimit,
    rag_chain: RAGChain = Depends(get_rag_chain),
    settings: Settings = Depends(get_settings),
) -> RAGQueryResponse:
    """
    RAGクエリエンドポイント

    LangGraphに関する質問に対して、ベクトルストアから関連ドキュメントを検索し、
    LLMを使用してソース付きで回答を生成します。

    **認証必須**: JWTトークンが必要です。
    **使用制限**: テストユーザーは1日5回まで、管理者は無制限です。

    Args:
        request: RAGクエリリクエスト
        current_user: 認証されたユーザー（依存性注入）
        rag_chain: RAGChainインスタンス（依存性注入）
        settings: アプリケーション設定（依存性注入）

    Returns:
        RAGクエリレスポンス

    Raises:
        HTTPException: クエリ実行エラー、認証エラー、使用制限超過
    """
    start_time = time.time()

    try:
        # RAGクエリ実行（既存のロジックをそのまま使用）
        result = rag_chain.query(
            question=request.question,
            k=request.k,
            include_sources=request.include_sources,
            include_code_examples=request.include_code_examples,
        )

        # レスポンススキーマに変換
        sources = [
            SourceResponse(
                title=source["title"],
                url=source["url"],
                excerpt=source["excerpt"],
                relevance=source["relevance"],
                doc_type=source.get("doc_type", "unknown"),
            )
            for source in result.get("sources", [])
        ]

        code_examples = [
            CodeExampleResponse(
                language=example["language"],
                code=example["code"],
                description=example["description"],
                source_url=example.get("source_url"),
            )
            for example in result.get("code_examples", [])
        ]

        response_time = time.time() - start_time

        metadata = RAGQueryMetadata(
            model=result["metadata"]["model"],
            tokens_used=result["metadata"]["tokens_used"],
            response_time=response_time,
        )

        return RAGQueryResponse(
            answer=result["answer"],
            sources=sources,
            code_examples=code_examples,
            confidence=result["confidence"],
            metadata=metadata,
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=f"入力バリデーションエラー: {str(e)}",
        )
    except VectorStoreError as e:
        raise HTTPException(
            status_code=500,
            detail=f"VectorStoreエラー: {str(e)}",
        )
    except LLMError as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLMエラー: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"予期しないエラーが発生しました: {str(e)}",
        )


@router.get(
    "/rag/health",
    response_model=RAGHealthResponse,
    summary="RAGヘルスチェック",
    description="RAGシステムの稼働状態を確認します",
)
async def rag_health(
    vectorstore: ChromaVectorStore = Depends(get_vectorstore),
) -> RAGHealthResponse:
    """
    RAGヘルスチェックエンドポイント

    VectorStoreの接続状態とドキュメント数を確認します。

    Args:
        vectorstore: VectorStoreインスタンス（依存性注入）

    Returns:
        RAGヘルスチェックレスポンス
    """
    try:
        # VectorStore接続確認
        collection_info = vectorstore.get_collection_info()

        return RAGHealthResponse(
            status="healthy",
            vectorstore_connected=True,
            document_count=collection_info.get("document_count", 0),
        )
    except Exception:
        return RAGHealthResponse(
            status="unhealthy",
            vectorstore_connected=False,
            document_count=0,
        )
