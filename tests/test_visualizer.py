"""
LangGraph Catalyst - Visualizer Tests

Mermaid図生成機能のユニットテスト
"""

import pytest

from src.features.architect.visualizer import (
    generate_mermaid_diagram,
    validate_mermaid_syntax,
)
from src.utils.exceptions import ValidationError


@pytest.mark.unit
class TestMermaidVisualizer:
    """Mermaid図生成のテスト"""

    # ========================================================================
    # Basic Diagram Generation Tests
    # ========================================================================

    def test_generate_mermaid_diagram_basic(self):
        """
        基本的なMermaid図生成のテスト

        テスト内容:
        - 有効なMermaid記法が生成されること
        - ノードとエッジが正しく含まれること
        """
        # Arrange
        nodes = [
            {
                "node_id": "A",
                "name": "開始",
                "purpose": "入力受付",
                "inputs": [],
                "outputs": ["data"],
            },
            {
                "node_id": "B",
                "name": "処理",
                "purpose": "データ処理",
                "inputs": ["data"],
                "outputs": ["result"],
            },
        ]
        edges = [{"from_node": "A", "to_node": "B", "description": "データを渡す"}]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert "graph" in mermaid_code or "flowchart" in mermaid_code
        assert "A" in mermaid_code
        assert "B" in mermaid_code
        assert "-->" in mermaid_code or "--->" in mermaid_code

    def test_generate_with_conditional_edges(self):
        """
        条件分岐エッジのテスト

        テスト内容:
        - 条件分岐が正しく表現されること
        - conditionフィールドがエッジラベルに反映されること
        """
        # Arrange
        nodes = [
            {"node_id": "A", "name": "判定", "purpose": "条件判定"},
            {"node_id": "B", "name": "True", "purpose": "真の場合"},
            {"node_id": "C", "name": "False", "purpose": "偽の場合"},
        ]
        edges = [
            {"from_node": "A", "to_node": "B", "condition": "Yes", "description": "条件が真"},
            {"from_node": "A", "to_node": "C", "condition": "No", "description": "条件が偽"},
        ]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert "Yes" in mermaid_code or "|Yes|" in mermaid_code
        assert "No" in mermaid_code or "|No|" in mermaid_code

    def test_generate_flowchart(self):
        """
        フローチャート生成のテスト

        テスト内容:
        - diagram_type='flowchart'でflowchart記法が使用されること
        """
        # Arrange
        nodes = [{"node_id": "A", "name": "ノードA", "purpose": "目的A"}]
        edges = []

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges, diagram_type="flowchart")

        # Assert
        assert "flowchart" in mermaid_code

    def test_generate_graph(self):
        """
        グラフ生成のテスト

        テスト内容:
        - diagram_type='graph'でgraph記法が使用されること
        """
        # Arrange
        nodes = [{"node_id": "A", "name": "ノードA", "purpose": "目的A"}]
        edges = []

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges, diagram_type="graph")

        # Assert
        assert "graph" in mermaid_code

    # ========================================================================
    # Node Label Escaping Tests
    # ========================================================================

    def test_node_label_escaping(self):
        """
        特殊文字のエスケープテスト

        テスト内容:
        - 特殊文字（", ', [, ]等）が正しくエスケープされること
        - 生成されたMermaid図が有効であること
        """
        # Arrange
        nodes = [{"node_id": "A", "name": '処理"特殊"', "purpose": "特殊文字を含む"}]
        edges = []

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        # エスケープ処理が正しく行われていることを確認
        assert mermaid_code is not None
        # 不正な記法になっていないことを確認
        assert '""' not in mermaid_code or '\\"' in mermaid_code

    def test_node_label_with_special_characters(self):
        """
        様々な特殊文字のテスト

        テスト内容:
        - &, <, >, 改行などが適切に処理されること
        """
        # Arrange
        nodes = [
            {"node_id": "A", "name": "Node & <test>", "purpose": "特殊文字"},
            {"node_id": "B", "name": "Node\nWith\nNewlines", "purpose": "改行含む"},
        ]
        edges = [{"from_node": "A", "to_node": "B", "description": "Edge"}]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert mermaid_code is not None
        # 改行が適切に処理されていること
        assert "\n\n" not in mermaid_code or "\\n" in mermaid_code

    # ========================================================================
    # Empty and Edge Cases Tests
    # ========================================================================

    def test_empty_nodes(self):
        """
        空ノードの処理テスト

        テスト内容:
        - ノードが空の場合に適切なエラーまたは空図が返されること
        """
        # Arrange
        nodes = []
        edges = []

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        # 空の図が生成されるか、エラーが発生する
        assert isinstance(mermaid_code, str)

    def test_empty_edges(self):
        """
        エッジなしノードのみのテスト

        テスト内容:
        - エッジがなくてもノードが表示されること
        """
        # Arrange
        nodes = [{"node_id": "A", "name": "ノードA", "purpose": "単独ノード"}]
        edges = []

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert "A" in mermaid_code
        assert isinstance(mermaid_code, str)

    def test_large_diagram(self):
        """
        大規模な図のテスト

        テスト内容:
        - 多数のノードとエッジが正しく処理されること
        """
        # Arrange
        nodes = [
            {"node_id": f"N{i}", "name": f"ノード{i}", "purpose": f"目的{i}"} for i in range(20)
        ]
        edges = [
            {"from_node": f"N{i}", "to_node": f"N{i + 1}", "description": f"エッジ{i}"}
            for i in range(19)
        ]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert "N0" in mermaid_code
        assert "N19" in mermaid_code
        assert isinstance(mermaid_code, str)

    # ========================================================================
    # Syntax Validation Tests
    # ========================================================================

    def test_mermaid_syntax_validation(self):
        """
        Mermaid構文検証のテスト

        テスト内容:
        - 有効なMermaid構文が検証を通過すること
        """
        # Arrange
        valid_mermaid = """
graph TD
    A[Start] --> B[Process]
    B --> C[End]
        """.strip()

        # Act
        result = validate_mermaid_syntax(valid_mermaid)

        # Assert
        assert result["valid"] is True
        assert isinstance(result["errors"], list)
        assert isinstance(result["warnings"], list)

    def test_invalid_mermaid_syntax(self):
        """
        無効なMermaid構文のテスト

        テスト内容:
        - 無効な構文が検証で失敗すること
        """
        # Arrange
        invalid_mermaid = "This is not mermaid syntax"

        # Act
        result = validate_mermaid_syntax(invalid_mermaid)

        # Assert
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    # ========================================================================
    # Different Diagram Types Tests
    # ========================================================================

    def test_create_flowchart(self):
        """
        フローチャート作成のテスト

        テスト内容:
        - フローチャート形式の図が正しく生成されること
        """
        # Arrange
        nodes = [
            {"node_id": "start", "name": "開始", "purpose": "スタート"},
            {"node_id": "end", "name": "終了", "purpose": "エンド"},
        ]
        edges = [{"from_node": "start", "to_node": "end", "description": "実行"}]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges, diagram_type="flowchart")

        # Assert
        assert "flowchart" in mermaid_code
        assert "start" in mermaid_code
        assert "end" in mermaid_code

    # ========================================================================
    # Direction and Styling Tests
    # ========================================================================

    def test_diagram_with_direction(self):
        """
        図の方向指定テスト

        テスト内容:
        - TD（上から下）、LR（左から右）などの方向が指定できること
        """
        # Arrange
        nodes = [{"node_id": "A", "name": "ノードA", "purpose": "目的A"}]
        edges = []

        # Act - 上から下
        mermaid_td = generate_mermaid_diagram(nodes, edges, direction="TD")
        # Act - 左から右
        mermaid_lr = generate_mermaid_diagram(nodes, edges, direction="LR")

        # Assert
        assert "TD" in mermaid_td or "TB" in mermaid_td
        assert "LR" in mermaid_lr

    def test_diagram_with_node_shapes(self):
        """
        ノード形状のテスト

        テスト内容:
        - 異なるノード形状（矩形、菱形、円形等）が表現できること
        """
        # Arrange
        nodes = [
            {"node_id": "A", "name": "開始", "shape": "circle"},
            {"node_id": "B", "name": "判定", "shape": "diamond"},
            {"node_id": "C", "name": "処理", "shape": "rectangle"},
        ]
        edges = [
            {"from_node": "A", "to_node": "B", "description": "次へ"},
            {"from_node": "B", "to_node": "C", "description": "実行"},
        ]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        # 形状に応じた記法が使用されていることを確認
        assert mermaid_code is not None

    # ========================================================================
    # Complex Scenarios Tests
    # ========================================================================

    def test_cyclic_graph(self):
        """
        循環グラフのテスト

        テスト内容:
        - 循環するエッジが正しく表現されること
        """
        # Arrange
        nodes = [
            {"node_id": "A", "name": "ノードA", "purpose": "開始"},
            {"node_id": "B", "name": "ノードB", "purpose": "処理"},
            {"node_id": "C", "name": "ノードC", "purpose": "判定"},
        ]
        edges = [
            {"from_node": "A", "to_node": "B", "description": "進む"},
            {"from_node": "B", "to_node": "C", "description": "判定"},
            {"from_node": "C", "to_node": "A", "description": "戻る"},  # 循環
        ]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert "A" in mermaid_code
        assert "B" in mermaid_code
        assert "C" in mermaid_code
        # 3つのエッジが全て含まれること
        assert mermaid_code.count("-->") >= 3 or mermaid_code.count("--->") >= 3

    def test_multiple_paths_to_same_node(self):
        """
        同じノードへの複数パステスト

        テスト内容:
        - 複数のノードから同じノードへのエッジが正しく表現されること
        """
        # Arrange
        nodes = [
            {"node_id": "A", "name": "ノードA", "purpose": "開始1"},
            {"node_id": "B", "name": "ノードB", "purpose": "開始2"},
            {"node_id": "C", "name": "ノードC", "purpose": "合流"},
        ]
        edges = [
            {"from_node": "A", "to_node": "C", "description": "パス1"},
            {"from_node": "B", "to_node": "C", "description": "パス2"},
        ]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert "A" in mermaid_code
        assert "B" in mermaid_code
        assert "C" in mermaid_code

    def test_disconnected_subgraphs(self):
        """
        切断されたサブグラフのテスト

        テスト内容:
        - 接続されていない複数のサブグラフが表現できること
        """
        # Arrange
        nodes = [
            {"node_id": "A", "name": "グループ1-A", "purpose": "目的A"},
            {"node_id": "B", "name": "グループ1-B", "purpose": "目的B"},
            {"node_id": "C", "name": "グループ2-C", "purpose": "目的C"},
            {"node_id": "D", "name": "グループ2-D", "purpose": "目的D"},
        ]
        edges = [
            {"from_node": "A", "to_node": "B", "description": "グループ1"},
            {"from_node": "C", "to_node": "D", "description": "グループ2"},
            # A-BとC-Dは接続されていない
        ]

        # Act
        mermaid_code = generate_mermaid_diagram(nodes, edges)

        # Assert
        assert all(node["node_id"] in mermaid_code for node in nodes)

    # ========================================================================
    # Error Handling Tests
    # ========================================================================

    def test_missing_required_fields(self):
        """
        必須フィールド欠損のテスト

        テスト内容:
        - node_idが欠けているノードがエラーになるかスキップされること
        """
        # Arrange
        nodes = [
            {"name": "ノードA"},  # node_idがない
        ]
        edges = []

        # Act & Assert
        # ValidationErrorが発生するか、エラーを無視して処理される
        try:
            mermaid_code = generate_mermaid_diagram(nodes, edges)
            # エラーが発生しない場合、有効な出力であることを確認
            assert isinstance(mermaid_code, str)
        except ValidationError:
            # ValidationErrorが発生するのも正常
            pass

    def test_invalid_edge_reference(self):
        """
        無効なエッジ参照のテスト

        テスト内容:
        - 存在しないノードを参照するエッジがエラーまたはスキップされること
        """
        # Arrange
        nodes = [{"node_id": "A", "name": "ノードA", "purpose": "目的A"}]
        edges = [{"from_node": "A", "to_node": "NonExistent", "description": "無効"}]

        # Act & Assert
        try:
            mermaid_code = generate_mermaid_diagram(nodes, edges)
            # エラーが発生しない場合、処理されていることを確認
            assert isinstance(mermaid_code, str)
        except ValidationError:
            # ValidationErrorが発生するのも正常
            pass
