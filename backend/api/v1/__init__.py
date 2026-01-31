"""
LangGraph Catalyst - API v1 Router

APIバージョン1のルーター統合。
全エンドポイントを `/api/v1` プレフィックスで提供します。
"""

from fastapi import APIRouter

from backend.api.v1 import architect, auth, learning_path, rag, templates

# v1 APIルーター
api_router = APIRouter()

# 各機能のルーター登録
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(rag.router, tags=["RAG"])
api_router.include_router(architect.router, tags=["Architect"])
api_router.include_router(learning_path.router, tags=["Learning Path"])
api_router.include_router(templates.router, tags=["Templates"])
