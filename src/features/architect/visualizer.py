"""
LangGraph Catalyst - Visualizer Module

Mermaid図の生成・検証・操作を行うモジュール。
"""

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def generate_mermaid_diagram(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    diagram_type: str = "flowchart",
) -> str:
    """
    ノードとエッジからMermaid図を生成

    Args:
        nodes: ノードのリスト
        edges: エッジのリスト
        diagram_type: 図のタイプ ("flowchart" or "graph")

    Returns:
        Mermaid記法の文字列

    Example:
        ```python
        nodes = [
            {"node_id": "A", "name": "開始", "purpose": "入力受付"},
            {"node_id": "B", "name": "処理", "purpose": "データ処理"}
        ]
        edges = [
            {"from_node": "A", "to_node": "B", "description": "データを渡す"}
        ]
        diagram = generate_mermaid_diagram(nodes, edges)
        ```
    """
    if not nodes:
        logger.warning("No nodes provided for Mermaid diagram generation")
        return ""

    # ヘッダー
    if diagram_type == "flowchart":
        lines = ["flowchart TD"]
    else:
        lines = ["graph TD"]

    # 開始・終了ノードの追加
    lines.append("    START([開始])")

    # ノードの追加
    for node in nodes:
        node_id = node.get("node_id", "")
        name = node.get("name", "")

        # ノード形状の決定（判定ノードはひし形）
        if "判定" in name or "分岐" in name or "check" in name.lower():
            lines.append(f"    {node_id}{{{name}}}")
        else:
            lines.append(f"    {node_id}[{name}]")

    # 終了ノードの追加
    lines.append("    END([終了])")

    # エッジの追加
    # 開始ノードから最初のノードへのエッジ
    if nodes:
        first_node_id = nodes[0].get("node_id", "")
        lines.append(f"    START --> {first_node_id}")

    # 通常のエッジ
    for edge in edges:
        from_node = edge.get("from_node", "")
        to_node = edge.get("to_node", "")
        condition = edge.get("condition")

        if condition:
            # 条件付きエッジ
            lines.append(f"    {from_node} -->|{condition}| {to_node}")
        else:
            # 通常のエッジ
            lines.append(f"    {from_node} --> {to_node}")

    # 最後のノードから終了ノードへのエッジ
    # エッジリストから終了点を特定
    last_nodes = _find_terminal_nodes(nodes, edges)
    for last_node_id in last_nodes:
        lines.append(f"    {last_node_id} --> END")

    mermaid_code = "\n".join(lines)

    logger.info(f"Generated Mermaid diagram with {len(nodes)} nodes and {len(edges)} edges")

    return mermaid_code


def validate_mermaid_syntax(mermaid_code: str) -> dict[str, Any]:
    """
    Mermaid記法の構文を検証

    Args:
        mermaid_code: Mermaid記法のコード

    Returns:
        検証結果
            - valid: bool - 有効かどうか
            - errors: list[str] - エラーメッセージのリスト
            - warnings: list[str] - 警告メッセージのリスト
    """
    errors = []
    warnings = []

    if not mermaid_code or not mermaid_code.strip():
        errors.append("Mermaid code is empty")
        return {"valid": False, "errors": errors, "warnings": warnings}

    lines = mermaid_code.strip().split("\n")

    # 1. ヘッダーチェック
    if not lines:
        errors.append("No lines found in Mermaid code")
        return {"valid": False, "errors": errors, "warnings": warnings}

    first_line = lines[0].strip()
    valid_headers = ["flowchart", "graph", "sequenceDiagram", "classDiagram", "stateDiagram"]

    if not any(first_line.startswith(header) for header in valid_headers):
        errors.append(f"Invalid diagram type: {first_line}")

    # 2. ノード定義のチェック（基本的な構文）
    node_pattern = re.compile(r"^\s*[A-Za-z0-9_]+[\[\(\{].*[\]\)\}]")
    edge_pattern = re.compile(r"^\s*[A-Za-z0-9_]+\s*-->.*")

    has_nodes = False
    has_edges = False

    for i, line in enumerate(lines[1:], start=2):
        line = line.strip()
        if not line:
            continue

        if node_pattern.match(line):
            has_nodes = True
        elif edge_pattern.match(line):
            has_edges = True
        elif "-->" in line or "---" in line or "==>" in line:
            has_edges = True

    if not has_nodes:
        warnings.append("No nodes found in diagram")

    if not has_edges:
        warnings.append("No edges found in diagram")

    # 3. 括弧のバランスチェック
    bracket_counts = {
        "[": mermaid_code.count("["),
        "]": mermaid_code.count("]"),
        "(": mermaid_code.count("("),
        ")": mermaid_code.count(")"),
        "{": mermaid_code.count("{"),
        "}": mermaid_code.count("}"),
    }

    if bracket_counts["["] != bracket_counts["]"]:
        errors.append("Unbalanced square brackets")

    if bracket_counts["("] != bracket_counts[")"]:
        errors.append("Unbalanced parentheses")

    if bracket_counts["{"] != bracket_counts["}"]:
        errors.append("Unbalanced curly braces")

    valid = len(errors) == 0

    result = {
        "valid": valid,
        "errors": errors,
        "warnings": warnings,
    }

    if valid:
        logger.info("Mermaid syntax validation passed")
    else:
        logger.warning(f"Mermaid syntax validation failed: {errors}")

    return result


def extract_mermaid_from_markdown(markdown_text: str) -> str | None:
    """
    MarkdownテキストからMermaidコードブロックを抽出

    Args:
        markdown_text: Markdownテキスト

    Returns:
        Mermaidコード（見つからない場合はNone）
    """
    # ```mermaid ... ``` パターンを検索
    pattern = r"```mermaid\s*\n(.*?)\n```"
    match = re.search(pattern, markdown_text, re.DOTALL)

    if match:
        mermaid_code = match.group(1).strip()
        logger.info("Extracted Mermaid code from markdown")
        return mermaid_code

    logger.warning("No Mermaid code block found in markdown")
    return None


def format_mermaid_for_display(mermaid_code: str) -> str:
    """
    表示用にMermaidコードをフォーマット

    Args:
        mermaid_code: Mermaidコード

    Returns:
        フォーマットされたMermaidコード
    """
    if not mermaid_code:
        return ""

    # 既にコードブロックで囲まれている場合はそのまま返す
    if mermaid_code.strip().startswith("```mermaid"):
        return mermaid_code

    # コードブロックで囲む
    formatted = f"```mermaid\n{mermaid_code.strip()}\n```"
    return formatted


def _find_terminal_nodes(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> list[str]:
    """
    終端ノード（他のノードへのエッジがないノード）を検出

    Args:
        nodes: ノードのリスト
        edges: エッジのリスト

    Returns:
        終端ノードIDのリスト
    """
    # すべてのノードID
    all_node_ids = {node.get("node_id") for node in nodes}

    # 出発点となっているノードID（from_node）
    source_nodes = {edge.get("from_node") for edge in edges}

    # 終端ノード = すべてのノード - 出発点ノード
    terminal_nodes = all_node_ids - source_nodes

    # エッジがない場合、最後のノードを終端とする
    if not terminal_nodes and nodes:
        terminal_nodes = {nodes[-1].get("node_id")}

    return list(terminal_nodes)


def add_styling_to_mermaid(mermaid_code: str, style_config: dict[str, str] | None = None) -> str:
    """
    Mermaid図にスタイリングを追加

    Args:
        mermaid_code: Mermaidコード
        style_config: スタイル設定（オプション）

    Returns:
        スタイリングが追加されたMermaidコード

    Example:
        ```python
        style_config = {
            "START": "fill:#e1f5e1,stroke:#4caf50,stroke-width:2px",
            "END": "fill:#ffebee,stroke:#f44336,stroke-width:2px"
        }
        styled_code = add_styling_to_mermaid(mermaid_code, style_config)
        ```
    """
    if not mermaid_code:
        return ""

    if style_config is None:
        # デフォルトのスタイル設定
        style_config = {
            "START": "fill:#e3f2fd,stroke:#2196f3,stroke-width:2px",
            "END": "fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px",
        }

    lines = mermaid_code.split("\n")

    # スタイル定義を追加
    style_lines = []
    for node_id, style in style_config.items():
        style_lines.append(f"    style {node_id} {style}")

    # 最後の行の前にスタイルを挿入
    if lines:
        lines.extend(style_lines)

    styled_code = "\n".join(lines)

    logger.info(f"Added {len(style_config)} style definitions to Mermaid diagram")

    return styled_code
