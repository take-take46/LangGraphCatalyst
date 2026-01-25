"""
LangGraph Catalyst - Architect Graph

ビジネス課題からLangGraph構成案を生成するワークフロー。
LangGraphのStateGraphを使用して、段階的に構成案を生成します。
"""

import json
import logging
import time
from typing import Any

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph

from src.config.settings import settings
from src.features.architect.prompts import (
    ARCHITECTURE_GENERATION_PROMPT,
    BUSINESS_EXPLANATION_PROMPT,
    CHALLENGE_ANALYSIS_PROMPT,
    CODE_GENERATION_PROMPT,
    IMPLEMENTATION_NOTES_PROMPT,
    MERMAID_GENERATION_PROMPT,
    format_constraints_context,
    format_industry_context,
)
from src.utils.exceptions import LLMError, ValidationError

logger = logging.getLogger(__name__)


# 状態定義
class ArchitectState(TypedDict):
    """構成案生成ワークフローの状態"""

    # 入力
    business_challenge: str
    industry: str | None
    constraints: list[str] | None

    # 課題分析結果
    challenge_analysis: dict[str, Any] | None

    # LangGraph構成案
    architecture: dict[str, Any] | None

    # Mermaid図
    mermaid_diagram: str | None

    # コード例
    code_example: dict[str, str] | None

    # ビジネス説明
    business_explanation: str | None

    # 実装ノート
    implementation_notes: list[str] | None

    # メタデータ
    metadata: dict[str, Any] | None

    # エラー情報
    error: str | None


class ArchitectGraph:
    """構成案生成グラフのクラス"""

    def __init__(
        self,
        llm_model: str | None = None,
        temperature: float = 0.7,
        streaming: bool = False,
    ):
        """
        ArchitectGraphの初期化

        Args:
            llm_model: 使用するLLMモデル
            temperature: 温度パラメータ（デフォルト: 0.7 - 創造的な出力向け）
            streaming: ストリーミングを有効にするか
        """
        self.llm_model = llm_model or settings.default_llm_model
        self.temperature = temperature
        self.streaming = streaming

        # LLMの初期化
        try:
            self.llm = ChatOpenAI(
                model=self.llm_model,
                temperature=self.temperature,
                openai_api_key=settings.openai_api_key,
                streaming=self.streaming,
            )
            logger.info(f"Initialized ArchitectGraph with model: {self.llm_model}")
        except Exception as e:
            raise ValidationError(f"Failed to initialize LLM: {e}") from e

        # グラフの構築
        self.graph = self._build_graph()

    def _build_graph(self) -> Any:
        """
        StateGraphを構築

        Returns:
            コンパイル済みのグラフ
        """
        # StateGraphの作成
        builder = StateGraph(ArchitectState)

        # ノードの追加
        builder.add_node("analyze_challenge", self._analyze_challenge_node)
        builder.add_node("generate_architecture", self._generate_architecture_node)
        builder.add_node("generate_mermaid", self._generate_mermaid_node)
        builder.add_node("generate_code", self._generate_code_node)
        builder.add_node("generate_explanation", self._generate_explanation_node)
        builder.add_node("generate_notes", self._generate_notes_node)

        # エッジの定義（線形フロー）
        builder.add_edge(START, "analyze_challenge")
        builder.add_edge("analyze_challenge", "generate_architecture")
        builder.add_edge("generate_architecture", "generate_mermaid")
        builder.add_edge("generate_mermaid", "generate_code")
        builder.add_edge("generate_code", "generate_explanation")
        builder.add_edge("generate_explanation", "generate_notes")
        builder.add_edge("generate_notes", END)

        # グラフのコンパイル
        graph = builder.compile()

        logger.info("ArchitectGraph compiled successfully")
        return graph

    def _analyze_challenge_node(self, state: ArchitectState) -> ArchitectState:
        """
        課題分析ノード

        ビジネス課題を分析し、要件を抽出します。

        Args:
            state: 現在の状態

        Returns:
            更新された状態
        """
        logger.info("Analyzing business challenge...")

        try:
            # プロンプトの構築
            industry_context = format_industry_context(state.get("industry"))
            constraints_context = format_constraints_context(state.get("constraints"))

            prompt = CHALLENGE_ANALYSIS_PROMPT.format(
                business_challenge=state["business_challenge"],
                industry_context=industry_context,
                constraints_context=constraints_context,
            )

            # LLM呼び出し
            response = self.llm.invoke(prompt)
            content = response.content

            # JSONの抽出
            analysis = self._extract_json_from_response(content)

            logger.info(f"Challenge analysis completed: {analysis.get('summary', '')[:50]}...")

            return {"challenge_analysis": analysis}

        except Exception as e:
            logger.error(f"Failed to analyze challenge: {e}")
            return {"error": f"課題分析に失敗しました: {str(e)}"}

    def _generate_architecture_node(self, state: ArchitectState) -> ArchitectState:
        """
        構成案生成ノード

        LangGraph構成案（ノード、エッジ、状態）を生成します。

        Args:
            state: 現在の状態

        Returns:
            更新された状態
        """
        logger.info("Generating LangGraph architecture...")

        # エラーチェック
        if state.get("error"):
            return {}

        try:
            # プロンプトの構築
            challenge_analysis_str = json.dumps(state["challenge_analysis"], ensure_ascii=False, indent=2)
            constraints_context = format_constraints_context(state.get("constraints"))

            prompt = ARCHITECTURE_GENERATION_PROMPT.format(
                challenge_analysis=challenge_analysis_str,
                business_challenge=state["business_challenge"],
                constraints_context=constraints_context,
            )

            # LLM呼び出し
            response = self.llm.invoke(prompt)
            content = response.content

            # JSONの抽出
            architecture = self._extract_json_from_response(content)

            logger.info(f"Architecture generated with {len(architecture.get('nodes', []))} nodes")

            return {"architecture": architecture}

        except Exception as e:
            logger.error(f"Failed to generate architecture: {e}")
            return {"error": f"構成案生成に失敗しました: {str(e)}"}

    def _generate_mermaid_node(self, state: ArchitectState) -> ArchitectState:
        """
        Mermaid図生成ノード

        LangGraph構成案からMermaidフローチャートを生成します。

        Args:
            state: 現在の状態

        Returns:
            更新された状態
        """
        logger.info("Generating Mermaid diagram...")

        # エラーチェック
        if state.get("error"):
            return {}

        try:
            # プロンプトの構築
            architecture_str = json.dumps(state["architecture"], ensure_ascii=False, indent=2)

            prompt = MERMAID_GENERATION_PROMPT.format(architecture=architecture_str)

            # LLM呼び出し
            response = self.llm.invoke(prompt)
            content = response.content

            # Mermaidコードブロックの抽出
            mermaid_diagram = self._extract_code_block(content, "mermaid")

            if not mermaid_diagram:
                logger.warning("Mermaid diagram not found in response, using full content")
                mermaid_diagram = content

            logger.info("Mermaid diagram generated successfully")

            return {"mermaid_diagram": mermaid_diagram}

        except Exception as e:
            logger.error(f"Failed to generate Mermaid diagram: {e}")
            return {"error": f"Mermaid図生成に失敗しました: {str(e)}"}

    def _generate_code_node(self, state: ArchitectState) -> ArchitectState:
        """
        コード例生成ノード

        LangGraph構成案を実装するPythonコードを生成します。

        Args:
            state: 現在の状態

        Returns:
            更新された状態
        """
        logger.info("Generating code example...")

        # エラーチェック
        if state.get("error"):
            return {}

        try:
            # プロンプトの構築
            challenge_analysis_str = json.dumps(state["challenge_analysis"], ensure_ascii=False, indent=2)
            architecture_str = json.dumps(state["architecture"], ensure_ascii=False, indent=2)

            prompt = CODE_GENERATION_PROMPT.format(
                challenge_analysis=challenge_analysis_str,
                architecture=architecture_str,
            )

            # LLM呼び出し
            response = self.llm.invoke(prompt)
            content = response.content

            # Pythonコードブロックの抽出
            code = self._extract_code_block(content, "python")

            # 説明部分の抽出（コードブロック以外の部分）
            explanation = content.replace(f"```python\n{code}\n```", "").strip()

            if not code:
                logger.warning("Python code not found in response")
                code = content

            logger.info("Code example generated successfully")

            return {"code_example": {"language": "python", "code": code, "explanation": explanation}}

        except Exception as e:
            logger.error(f"Failed to generate code: {e}")
            return {"error": f"コード生成に失敗しました: {str(e)}"}

    def _generate_explanation_node(self, state: ArchitectState) -> ArchitectState:
        """
        ビジネス説明生成ノード

        非技術者向けの分かりやすい説明を生成します。

        Args:
            state: 現在の状態

        Returns:
            更新された状態
        """
        logger.info("Generating business explanation...")

        # エラーチェック
        if state.get("error"):
            return {}

        try:
            # プロンプトの構築
            challenge_analysis_str = json.dumps(state["challenge_analysis"], ensure_ascii=False, indent=2)
            architecture_str = json.dumps(state["architecture"], ensure_ascii=False, indent=2)

            prompt = BUSINESS_EXPLANATION_PROMPT.format(
                business_challenge=state["business_challenge"],
                challenge_analysis=challenge_analysis_str,
                architecture=architecture_str,
            )

            # LLM呼び出し
            response = self.llm.invoke(prompt)
            explanation = response.content

            logger.info("Business explanation generated successfully")

            return {"business_explanation": explanation}

        except Exception as e:
            logger.error(f"Failed to generate explanation: {e}")
            return {"error": f"ビジネス説明生成に失敗しました: {str(e)}"}

    def _generate_notes_node(self, state: ArchitectState) -> ArchitectState:
        """
        実装ノート生成ノード

        実装時の注意点やベストプラクティスを生成します。

        Args:
            state: 現在の状態

        Returns:
            更新された状態
        """
        logger.info("Generating implementation notes...")

        # エラーチェック
        if state.get("error"):
            return {}

        try:
            # プロンプトの構築
            architecture_str = json.dumps(state["architecture"], ensure_ascii=False, indent=2)
            constraints_context = format_constraints_context(state.get("constraints"))

            prompt = IMPLEMENTATION_NOTES_PROMPT.format(
                architecture=architecture_str,
                constraints_context=constraints_context,
            )

            # LLM呼び出し
            response = self.llm.invoke(prompt)
            content = response.content

            # 箇条書きの抽出
            notes = self._extract_bullet_points(content)

            logger.info(f"Implementation notes generated: {len(notes)} items")

            return {"implementation_notes": notes}

        except Exception as e:
            logger.error(f"Failed to generate implementation notes: {e}")
            return {"error": f"実装ノート生成に失敗しました: {str(e)}"}

    def generate_architecture(
        self,
        business_challenge: str,
        industry: str | None = None,
        constraints: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        ビジネス課題からLangGraph構成案を生成

        Args:
            business_challenge: ビジネス課題の説明
            industry: 業界（オプション）
            constraints: 制約条件のリスト（オプション）

        Returns:
            構成案レスポンス

        Raises:
            ValidationError: バリデーションエラー
            LLMError: LLM呼び出しエラー
        """
        if not business_challenge or not business_challenge.strip():
            raise ValidationError("Business challenge cannot be empty")

        logger.info(f"Starting architecture generation for: {business_challenge[:50]}...")

        start_time = time.time()

        try:
            # 初期状態の設定
            initial_state: ArchitectState = {
                "business_challenge": business_challenge,
                "industry": industry,
                "constraints": constraints,
                "challenge_analysis": None,
                "architecture": None,
                "mermaid_diagram": None,
                "code_example": None,
                "business_explanation": None,
                "implementation_notes": None,
                "metadata": None,
                "error": None,
            }

            # グラフの実行
            result_state = self.graph.invoke(initial_state)

            # エラーチェック
            if result_state.get("error"):
                raise LLMError(result_state["error"])

            # レスポンスの構築
            response_time = time.time() - start_time

            response = {
                "challenge_analysis": result_state["challenge_analysis"],
                "architecture": {
                    "mermaid_diagram": result_state["mermaid_diagram"],
                    "node_descriptions": result_state["architecture"].get("nodes", []),
                    "edge_descriptions": result_state["architecture"].get("edges", []),
                    "state_schema": result_state["architecture"].get("state_schema", {}),
                },
                "code_example": result_state["code_example"],
                "business_explanation": result_state["business_explanation"],
                "implementation_notes": result_state["implementation_notes"],
                "metadata": {
                    "model": self.llm_model,
                    "response_time": response_time,
                },
            }

            logger.info(f"Architecture generation completed in {response_time:.2f}s")

            return response

        except Exception as e:
            logger.error(f"Failed to generate architecture: {e}")
            raise LLMError(f"Failed to generate architecture: {e}") from e

    def _extract_json_from_response(self, content: str) -> dict[str, Any]:
        """
        LLMレスポンスからJSONを抽出

        Args:
            content: LLMレスポンス

        Returns:
            抽出されたJSON

        Raises:
            ValidationError: JSON抽出失敗
        """
        # コードブロック内のJSONを探す
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_str = content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_str = content[start:end].strip()
        else:
            # コードブロックなしでJSONを探す
            json_str = content.strip()

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}\nContent: {json_str[:200]}...")
            raise ValidationError(f"Failed to parse JSON from LLM response: {e}") from e

    def _extract_code_block(self, content: str, language: str = "python") -> str:
        """
        コードブロックを抽出

        Args:
            content: LLMレスポンス
            language: コードブロックの言語

        Returns:
            抽出されたコード
        """
        marker = f"```{language}"
        if marker in content:
            start = content.find(marker) + len(marker)
            end = content.find("```", start)
            return content[start:end].strip()
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            return content[start:end].strip()
        return ""

    def _extract_bullet_points(self, content: str) -> list[str]:
        """
        箇条書きを抽出

        Args:
            content: LLMレスポンス

        Returns:
            箇条書きのリスト
        """
        lines = content.split("\n")
        bullet_points = []

        for line in lines:
            line = line.strip()
            # Markdown形式の箇条書き
            if line.startswith("- ") or line.startswith("* ") or line.startswith("+ "):
                bullet_points.append(line[2:].strip())
            # 番号付きリスト
            elif line and line[0].isdigit() and ". " in line:
                bullet_points.append(line.split(". ", 1)[1].strip())

        return bullet_points
