"""
LangGraph Catalyst - RAG Chain

RAG (Retrieval-Augmented Generation) チェーンを実装するモジュール。
ベクトルストアからの検索結果を使用してLLMで回答を生成します。
"""

import logging
import time
from typing import Any

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from src.config.settings import settings
from src.features.rag.vectorstore import ChromaVectorStore
from src.utils.exceptions import LLMError, ValidationError
from src.utils.helpers import extract_code_blocks, format_sources

logger = logging.getLogger(__name__)

# システムプロンプトテンプレート（学習支援重視版）
SYSTEM_PROMPT_LEARNING = """あなたはLangGraphの学習支援エキスパートです。ユーザーがLangGraphを理解し、学習を進められるよう支援してください。

# 回答のガイドライン:
1. **概念を丁寧に説明する**: 技術用語は分かりやすく解説し、初学者でも理解できるように説明してください
2. **公式ドキュメントへの導線**: より詳細な情報がある公式ドキュメントのページを示唆してください
3. **学習の道筋を示す**: 関連する概念や、次に学ぶべきトピックを提案してください
4. **実用的な文脈を提供**: その機能が「なぜ」必要か、「どういう時に」使うかを説明してください
5. **正確性を重視**: コンテキストに情報がない場合は、推測せず正直に伝えてください

# コンテキスト:
{context}

# 質問:
{question}

上記のコンテキストを参考に、学習者の理解を深める回答を提供してください。コード例は含めず、概念の説明に集中してください。
"""

# システムプロンプトテンプレート（コード提示版）
SYSTEM_PROMPT_WITH_CODE = """あなたはLangGraphの学習支援エキスパートです。ユーザーがLangGraphを理解し、実装できるよう支援してください。

# 回答のガイドライン:
1. **概念を説明してから実装へ**: まず概念を説明し、その後具体的な実装方法を示してください
2. **実行可能なコード例**: 完全で実行可能なコード例を提供してください
3. **コードの説明**: 各コードブロックに、何をしているかの説明を添えてください
4. **ベストプラクティス**: 推奨される実装方法や注意点も含めてください
5. **公式ドキュメント参照**: より詳細な情報源へのリンクも示唆してください

# コンテキスト:
{context}

# 質問:
{question}

上記のコンテキストを参考に、概念説明と具体的な実装例（コード）を含めた回答を提供してください。
"""


class RAGChain:
    """RAG (Retrieval-Augmented Generation) チェーンのクラス"""

    def __init__(
        self,
        vectorstore: ChromaVectorStore,
        llm_model: str | None = None,
        temperature: float | None = None,
        streaming: bool = False,
    ):
        """
        RAGChainの初期化

        Args:
            vectorstore: Chromaベクトルストア
            llm_model: 使用するLLMモデル
            temperature: 温度パラメータ
            streaming: ストリーミングを有効にするか

        Raises:
            ValidationError: バリデーションエラー
        """
        self.vectorstore = vectorstore
        self.llm_model = llm_model or settings.default_llm_model
        self.temperature = temperature if temperature is not None else settings.temperature
        self.streaming = streaming

        # LLMの初期化
        try:
            self.llm = ChatOpenAI(
                model=self.llm_model,
                temperature=self.temperature,
                openai_api_key=settings.openai_api_key,
                streaming=self.streaming,
            )
            logger.info(f"Initialized RAGChain with model: {self.llm_model}")
        except Exception as e:
            raise ValidationError(f"Failed to initialize LLM: {e}") from e

        # プロンプトテンプレートの作成（2種類）
        self.prompt_template_learning = ChatPromptTemplate.from_template(SYSTEM_PROMPT_LEARNING)
        self.prompt_template_with_code = ChatPromptTemplate.from_template(
            SYSTEM_PROMPT_WITH_CODE
        )

    def _should_include_code(self, question: str) -> bool:
        """
        質問からコード例が必要かを判定

        Args:
            question: ユーザーの質問

        Returns:
            bool: コード例が必要な場合True
        """
        # コードを要求するキーワード
        code_keywords = [
            # 日本語
            "コード",
            "実装",
            "書き方",
            "作り方",
            "書いて",
            "示して",
            "見せて",
            "例",
            "サンプル",
            "プログラム",
            "スクリプト",
            # 英語
            "code",
            "example",
            "sample",
            "implement",
            "write",
            "show me",
            "how to write",
            "how to implement",
            "create",
            "build",
        ]

        question_lower = question.lower()
        return any(keyword in question_lower for keyword in code_keywords)

    def query(
        self,
        question: str,
        k: int = 5,
        include_sources: bool = True,
        include_code_examples: bool | None = None,
    ) -> dict[str, Any]:
        """
        RAGクエリを実行

        Args:
            question: ユーザーの質問
            k: 検索する関連ドキュメント数
            include_sources: ソース情報を含めるか
            include_code_examples: コード例を含めるか
                - None: 質問から自動判定（デフォルト）
                - True: 強制的に含める
                - False: 含めない

        Returns:
            dict: RAG応答

        Raises:
            ValidationError: バリデーションエラー
            LLMError: LLM呼び出しエラー
        """
        if not question or not question.strip():
            raise ValidationError("Question cannot be empty")

        # コード例の自動判定
        if include_code_examples is None:
            include_code_examples = self._should_include_code(question)
            logger.info(
                f"Auto-detected code requirement: {include_code_examples} for question: {question[:50]}..."
            )

        logger.info(f"Processing RAG query: {question[:50]}...")

        start_time = time.time()

        try:
            # 1. 類似ドキュメントを検索
            retrieved_docs = self.vectorstore.similarity_search(query=question, k=k)

            if not retrieved_docs:
                logger.warning("No relevant documents found")
                return {
                    "answer": "申し訳ありませんが、関連する情報が見つかりませんでした。別の質問を試してみてください。",
                    "sources": [],
                    "code_examples": [],
                    "confidence": 0.0,
                    "metadata": {
                        "model": self.llm_model,
                        "tokens_used": 0,
                        "response_time": time.time() - start_time,
                    },
                }

            # 2. コンテキストを構築
            context = self._build_context(retrieved_docs)

            # 3. プロンプトテンプレートを選択
            if include_code_examples:
                prompt_template = self.prompt_template_with_code
                logger.info("Using code-inclusive prompt template")
            else:
                prompt_template = self.prompt_template_learning
                logger.info("Using learning-focused prompt template")

            # 4. プロンプトを生成
            prompt = prompt_template.format(context=context, question=question)

            # 5. LLMで回答を生成
            response = self.llm.invoke(prompt)
            answer = response.content

            # 6. ソース情報を抽出
            sources = []
            if include_sources:
                sources = format_sources(retrieved_docs)

            # 7. コード例を抽出（回答 + 検索結果ドキュメントから）
            # コードが要求されている場合のみ抽出
            code_examples = []
            if include_code_examples:
                # 回答からコードブロックを抽出
                answer_code_blocks = extract_code_blocks(answer)
                for block in answer_code_blocks:
                    code_examples.append(
                        {
                            "language": block.get("language", "python"),
                            "code": block["code"],
                            "description": "Code example from AI response",
                        }
                    )

                # 検索結果のドキュメントからもコード例を抽出
                for doc in retrieved_docs[:3]:  # 上位3件から抽出
                    doc_code_blocks = extract_code_blocks(doc.page_content)
                    for block in doc_code_blocks[:2]:  # 各ドキュメントから最大2件
                        code_examples.append(
                            {
                                "language": block.get("language", "python"),
                                "code": block["code"],
                                "description": f"Example from {doc.metadata.get('title', 'documentation')}",
                                "source_url": doc.metadata.get("source"),
                            }
                        )

                # 重複を除去（コード内容でユニーク化）
                seen_codes = set()
                unique_examples = []
                for example in code_examples:
                    code_hash = hash(example["code"].strip())
                    if code_hash not in seen_codes:
                        seen_codes.add(code_hash)
                        unique_examples.append(example)

                code_examples = unique_examples[:5]  # 最大5件

            # 8. レスポンスを構築
            response_time = time.time() - start_time

            result = {
                "answer": answer,
                "sources": sources,
                "code_examples": code_examples,
                "confidence": self._calculate_confidence(retrieved_docs),
                "metadata": {
                    "model": self.llm_model,
                    "tokens_used": response.response_metadata.get("token_usage", {}).get(
                        "total_tokens", 0
                    ),
                    "response_time": response_time,
                },
            }

            logger.info(f"RAG query completed in {response_time:.2f}s with {len(sources)} sources")

            return result

        except Exception as e:
            logger.error(f"Failed to process RAG query: {e}")
            raise LLMError(f"Failed to process RAG query: {e}") from e

    def _build_context(self, documents: list[Document]) -> str:
        """
        ドキュメントからコンテキストを構築

        Args:
            documents: 検索されたドキュメントのリスト

        Returns:
            str: コンテキスト文字列
        """
        context_parts = []

        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown source")
            title = doc.metadata.get("title", "Untitled")
            content = doc.page_content

            context_part = f"""
### ソース {i}: {title}
URL: {source}

{content}
"""
            context_parts.append(context_part)

        return "\n".join(context_parts)

    def _calculate_confidence(self, documents: list[Document]) -> float:
        """
        検索結果の信頼度を計算

        Args:
            documents: 検索されたドキュメントのリスト

        Returns:
            float: 信頼度スコア (0-1)
        """
        if not documents:
            return 0.0

        # シンプルな信頼度計算（ドキュメント数に基づく）
        # 実際にはスコアやその他の指標を使用できます
        doc_count = len(documents)

        if doc_count >= 5:
            return 0.9
        elif doc_count >= 3:
            return 0.7
        elif doc_count >= 1:
            return 0.5
        else:
            return 0.0
