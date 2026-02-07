"""
LangGraph Catalyst - Architect Graph Tests

構成案生成ワークフローのユニットテスト
"""

import json
from unittest.mock import Mock

import pytest

from src.features.architect.graph import ArchitectGraph
from src.utils.exceptions import ValidationError


@pytest.mark.unit
class TestArchitectGraph:
    """ArchitectGraphのテスト"""

    # ========================================================================
    # Initialization Tests
    # ========================================================================

    def test_architect_graph_initialization(self, mocker, mock_openai_chat):
        """ArchitectGraphの初期化テスト"""
        # Arrange
        mock_openai_chat()

        # Act
        architect = ArchitectGraph()

        # Assert
        assert architect is not None
        assert architect.llm is not None
        assert architect.graph is not None

    def test_architect_graph_initialization_with_custom_params(self, mocker, mock_openai_chat):
        """カスタムパラメータでの初期化テスト"""
        # Arrange
        mock_openai_chat()
        custom_model = "gpt-4"
        custom_temp = 0.8

        # Act
        architect = ArchitectGraph(llm_model=custom_model, temperature=custom_temp)

        # Assert
        assert architect.llm_model == custom_model
        assert architect.temperature == custom_temp

    def test_architect_graph_initialization_failure(self, mocker):
        """LLM初期化失敗のテスト"""
        # Arrange
        mocker.patch("src.features.architect.graph.ChatOpenAI", side_effect=Exception("API Error"))

        # Act & Assert
        with pytest.raises(ValidationError, match="Failed to initialize LLM"):
            ArchitectGraph()

    # ========================================================================
    # Generate Architecture Tests
    # ========================================================================

    def test_generate_architecture_success(
        self,
        mocker,
        sample_business_challenge,
        sample_industry,
        sample_constraints,
    ):
        """構成案生成の成功テスト"""
        # Arrange
        # 各ノードのレスポンスを直接モック（mock_openai_chat fixureは使わない）
        analysis_response = json.dumps(
            {
                "summary": "カスタマーサポート自動化の課題分析",
                "key_requirements": ["FAQ自動回答", "エスカレーション機能"],
                "suggested_approach": "LangGraphの条件分岐を活用",
            }
        )

        architecture_response = json.dumps(
            {
                "nodes": [
                    {"node_id": "start", "name": "開始", "purpose": "入力受付"},
                    {"node_id": "faq", "name": "FAQ検索", "purpose": "FAQ検索"},
                ],
                "edges": [{"from_node": "start", "to_node": "faq", "description": "入力を渡す"}],
                "state_schema": {"query": "str", "response": "str"},
            }
        )

        mermaid_response = """```mermaid
graph TD
    start[開始] --> faq[FAQ検索]
    faq --> end[終了]
```"""

        code_response = """```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
graph.add_node("faq_search", faq_search_node)
```

このコードは、FAQ検索ノードを追加する例です。"""

        explanation_response = (
            "このシステムは、ユーザーの問い合わせを受け付け、まずFAQデータベースで検索します..."
        )

        notes_response = """- FAQ検索にはベクトルDBを使用することを推奨
- Zendesk APIの認証情報が必要"""

        responses = [
            analysis_response,
            architecture_response,
            mermaid_response,
            code_response,
            explanation_response,
            notes_response,
        ]

        # モックを直接設定
        mock_llm = mocker.patch("src.features.architect.graph.ChatOpenAI")
        mock_llm.return_value.invoke.side_effect = [
            Mock(content=resp, response_metadata={"token_usage": {"total_tokens": 100}})
            for resp in responses
        ]

        # ArchitectGraph作成（この時点でChatOpenAIが初期化される）
        architect = ArchitectGraph()

        # Act
        response = architect.generate_architecture(
            business_challenge=sample_business_challenge,
            industry=sample_industry,
            constraints=sample_constraints,
        )

        # Assert
        assert "challenge_analysis" in response
        assert "architecture" in response
        assert "code_example" in response
        assert "business_explanation" in response
        assert "implementation_notes" in response
        assert "metadata" in response

        # 各フィールドの詳細確認
        assert response["challenge_analysis"]["summary"] is not None
        assert len(response["architecture"]["node_descriptions"]) > 0
        assert response["architecture"]["mermaid_diagram"] is not None
        assert response["code_example"]["code"] is not None
        assert response["business_explanation"] is not None
        assert len(response["implementation_notes"]) > 0

    def test_generate_architecture_empty_challenge(self, mocker, mock_openai_chat):
        """空のビジネス課題のテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        # Act & Assert
        with pytest.raises(ValidationError, match="Business challenge cannot be empty"):
            architect.generate_architecture(business_challenge="")

    def test_generate_architecture_with_industry_only(self, mocker, sample_business_challenge):
        """業界のみ指定のテスト"""
        # Arrange
        responses = [
            json.dumps(
                {"summary": "分析結果", "key_requirements": [], "suggested_approach": "方法"}
            ),
            json.dumps({"nodes": [], "edges": [], "state_schema": {}}),
            "```mermaid\ngraph TD\n```",
            "```python\ncode\n```",
            "説明",
            "- ノート",
        ]

        # モックを直接設定
        mock_llm = mocker.patch("src.features.architect.graph.ChatOpenAI")
        mock_llm.return_value.invoke.side_effect = [
            Mock(content=resp, response_metadata={"token_usage": {"total_tokens": 50}})
            for resp in responses
        ]

        architect = ArchitectGraph()

        # Act
        response = architect.generate_architecture(
            business_challenge=sample_business_challenge, industry="製造業"
        )

        # Assert
        assert response is not None

    # ========================================================================
    # Node Tests
    # ========================================================================

    def test_analyze_challenge_node(self, mocker, mock_openai_chat, sample_business_challenge):
        """課題分析ノードのテスト"""
        # Arrange
        analysis_json = json.dumps(
            {
                "summary": "課題の要約",
                "key_requirements": ["要件1", "要件2"],
                "suggested_approach": "推奨アプローチ",
            }
        )

        mock_openai_chat(response_content=analysis_json)
        architect = ArchitectGraph()

        # Act
        state = {
            "business_challenge": sample_business_challenge,
            "industry": "EC",
            "constraints": ["制約1"],
        }
        result = architect._analyze_challenge_node(state)

        # Assert
        assert "challenge_analysis" in result
        assert result["challenge_analysis"]["summary"] is not None

    def test_generate_architecture_node(self, mocker, mock_openai_chat):
        """構成案生成ノードのテスト"""
        # Arrange
        architecture_json = json.dumps(
            {
                "nodes": [{"node_id": "A", "name": "ノードA", "purpose": "目的A"}],
                "edges": [{"from_node": "A", "to_node": "B", "description": "説明"}],
                "state_schema": {},
            }
        )

        mock_openai_chat(response_content=architecture_json)
        architect = ArchitectGraph()

        # Act
        state = {
            "business_challenge": "課題",
            "challenge_analysis": {"summary": "分析"},
            "constraints": None,
        }
        result = architect._generate_architecture_node(state)

        # Assert
        assert "architecture" in result
        assert len(result["architecture"]["nodes"]) > 0

    def test_generate_mermaid_node(self, mocker, mock_openai_chat):
        """Mermaid図生成ノードのテスト"""
        # Arrange
        mermaid_code = """```mermaid
graph TD
    A[ノードA] --> B[ノードB]
```"""

        mock_openai_chat(response_content=mermaid_code)
        architect = ArchitectGraph()

        # Act
        state = {
            "architecture": {"nodes": [], "edges": []},
        }
        result = architect._generate_mermaid_node(state)

        # Assert
        assert "mermaid_diagram" in result
        assert "graph TD" in result["mermaid_diagram"] or "flowchart" in result["mermaid_diagram"]

    def test_generate_code_node(self, mocker, mock_openai_chat):
        """コード生成ノードのテスト"""
        # Arrange
        code_response = """コードの説明

```python
from langgraph.graph import StateGraph

graph = StateGraph(State)
```

上記のコードは基本的な例です。"""

        mock_openai_chat(response_content=code_response)
        architect = ArchitectGraph()

        # Act
        state = {
            "challenge_analysis": {"summary": "分析"},
            "architecture": {"nodes": [], "edges": []},
        }
        result = architect._generate_code_node(state)

        # Assert
        assert "code_example" in result
        assert result["code_example"]["language"] == "python"
        assert result["code_example"]["code"] is not None
        assert "StateGraph" in result["code_example"]["code"]

    def test_generate_explanation_node(self, mocker, mock_openai_chat):
        """ビジネス説明生成ノードのテスト"""
        # Arrange
        explanation = "このシステムは、ユーザーの問い合わせを自動的に処理します..."

        mock_openai_chat(response_content=explanation)
        architect = ArchitectGraph()

        # Act
        state = {
            "business_challenge": "課題",
            "challenge_analysis": {"summary": "分析"},
            "architecture": {"nodes": [], "edges": []},
        }
        result = architect._generate_explanation_node(state)

        # Assert
        assert "business_explanation" in result
        assert result["business_explanation"] is not None

    def test_generate_notes_node(self, mocker, mock_openai_chat):
        """実装ノート生成ノードのテスト"""
        # Arrange
        notes_response = """実装時の注意点：

- ベクトルDBの選択が重要
- API認証情報の管理
- エラーハンドリングの実装"""

        mock_openai_chat(response_content=notes_response)
        architect = ArchitectGraph()

        # Act
        state = {
            "architecture": {"nodes": [], "edges": []},
            "constraints": ["制約1"],
        }
        result = architect._generate_notes_node(state)

        # Assert
        assert "implementation_notes" in result
        assert len(result["implementation_notes"]) > 0

    # ========================================================================
    # Helper Method Tests
    # ========================================================================

    def test_extract_json_from_response_with_code_block(self, mocker, mock_openai_chat):
        """JSONコードブロック抽出のテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        content = """以下はJSONです：

```json
{"key": "value", "number": 42}
```

以上です。"""

        # Act
        result = architect._extract_json_from_response(content)

        # Assert
        assert result == {"key": "value", "number": 42}

    def test_extract_json_from_response_plain(self, mocker, mock_openai_chat):
        """プレーンJSON抽出のテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        content = '{"key": "value", "number": 42}'

        # Act
        result = architect._extract_json_from_response(content)

        # Assert
        assert result == {"key": "value", "number": 42}

    def test_extract_json_from_response_error(self, mocker, mock_openai_chat):
        """JSON抽出エラーのテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        content = "This is not JSON"

        # Act & Assert
        with pytest.raises(ValidationError, match="Failed to parse JSON"):
            architect._extract_json_from_response(content)

    def test_extract_code_block_python(self, mocker, mock_openai_chat):
        """Pythonコードブロック抽出のテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        content = """説明文

```python
def hello():
    print("Hello")
```

終わり"""

        # Act
        result = architect._extract_code_block(content, "python")

        # Assert
        assert "def hello():" in result
        assert 'print("Hello")' in result

    def test_extract_code_block_mermaid(self, mocker, mock_openai_chat):
        """Mermaidコードブロック抽出のテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        content = """```mermaid
graph TD
    A --> B
```"""

        # Act
        result = architect._extract_code_block(content, "mermaid")

        # Assert
        assert "graph TD" in result
        assert "A --> B" in result

    def test_extract_bullet_points(self, mocker, mock_openai_chat):
        """箇条書き抽出のテスト"""
        # Arrange
        mock_openai_chat()
        architect = ArchitectGraph()

        content = """注意点：

- 項目1
- 項目2
* 項目3

番号付き：
1. 項目4
2. 項目5"""

        # Act
        result = architect._extract_bullet_points(content)

        # Assert
        assert len(result) >= 5
        assert "項目1" in result
        assert "項目5" in result

    # ========================================================================
    # Error Handling Tests
    # ========================================================================

    def test_node_error_propagation(self, mocker):
        """ノードエラーの伝播テスト"""
        # Arrange
        # 初期化時のLLMは成功させる
        mock_init = mocker.patch("src.features.architect.graph.ChatOpenAI")
        mock_llm_instance = Mock()
        mock_init.return_value = mock_llm_instance

        # ノード実行時にエラーを発生させる
        mock_llm_instance.invoke.side_effect = Exception("LLM Error")

        architect = ArchitectGraph()

        # Act
        state = {"business_challenge": "課題"}
        result = architect._analyze_challenge_node(state)

        # Assert
        assert "error" in result
        assert "課題分析に失敗しました" in result["error"]
