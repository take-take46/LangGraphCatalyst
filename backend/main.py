"""
LangGraph Catalyst - FastAPI Application

FastAPIアプリケーションのエントリーポイント。
CORS設定、ミドルウェア、ルーター登録などを行います。
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.core.config import get_settings
from backend.schemas.common import ErrorResponse, HealthResponse

# 設定を取得
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    アプリケーションのライフサイクル管理

    起動時・終了時の処理を定義します。
    """
    # 起動時の処理
    settings.setup_logging()
    print(f"🚀 Starting {settings.api_title} v{settings.api_version}")
    print(f"   Environment: {settings.environment}")
    print(f"   CORS Origins: {settings.cors_origins_list}")

    yield

    # 終了時の処理
    print(f"🛑 Shutting down {settings.api_title}")


# FastAPIアプリケーション初期化
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# リクエストロギングミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    リクエストのロギングミドルウェア

    各リクエストの処理時間とステータスコードをログに記録します。
    """
    start_time = time.time()

    # リクエスト処理
    response = await call_next(request)

    # 処理時間計算
    process_time = time.time() - start_time

    # ログ出力
    print(
        f"{request.method} {request.url.path} "
        f"- Status: {response.status_code} "
        f"- Time: {process_time:.3f}s"
    )

    # カスタムヘッダー追加
    response.headers["X-Process-Time"] = str(process_time)

    return response


# エラーハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    グローバル例外ハンドラー

    予期しない例外をキャッチしてJSON形式でエラーレスポンスを返します。
    """
    error_response = ErrorResponse(
        error="INTERNAL_ERROR",
        message="予期しないエラーが発生しました",
        details=str(exc) if settings.is_development else None,
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(),
    )


# ヘルスチェックエンドポイント
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="ヘルスチェック",
    description="APIの稼働状態を確認します",
)
async def health_check():
    """
    ヘルスチェックエンドポイント

    APIが正常に稼働しているかを確認します。
    """
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        environment=settings.environment,
    )


@app.get(
    "/ready",
    response_model=HealthResponse,
    tags=["Health"],
    summary="レディネスチェック",
    description="APIが準備完了状態かを確認します",
)
async def readiness_check():
    """
    レディネスチェックエンドポイント

    APIがリクエストを受け付ける準備ができているかを確認します。
    """
    # TODO: 実際のデータベース接続確認などを追加
    return HealthResponse(
        status="ready",
        version=settings.api_version,
        environment=settings.environment,
    )


# ルーター登録
from backend.api.v1 import api_router

app.include_router(api_router, prefix="/api/v1")


# ルートエンドポイント
@app.get(
    "/",
    tags=["Root"],
    summary="APIルート",
    description="API情報を返します",
)
async def root():
    """
    ルートエンドポイント

    API情報を返します。
    """
    return {
        "title": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description,
        "docs_url": "/docs",
        "health_url": "/health",
    }
