"""
Architect API Endpoint Tests

構成案生成APIのテスト。
"""

from unittest.mock import patch


def test_architect_generate_success(authenticated_client, mock_architect_graph):
    """構成案生成正常実行テスト"""
    with patch("backend.api.v1.architect.get_architect_graph", return_value=mock_architect_graph):
        response = authenticated_client.post(
            "/api/v1/architect/generate",
            json={
                "business_challenge": "カスタマーサポートの自動化を実現したい。FAQへの自動回答と、複雑な問い合わせは人間にエスカレーションする仕組みが必要。",
                "industry": "EC",
                "constraints": ["日本語対応必須", "既存のZendeskと連携"],
            },
        )

    assert response.status_code == 200
    data = response.json()

    # 課題分析が含まれること
    assert "challenge_analysis" in data
    analysis = data["challenge_analysis"]
    assert "summary" in analysis
    assert "key_requirements" in analysis
    assert isinstance(analysis["key_requirements"], list)
    assert len(analysis["key_requirements"]) > 0
    assert "suggested_approach" in analysis
    assert "langgraph_fit_reason" in analysis

    # アーキテクチャが含まれること
    assert "architecture" in data
    architecture = data["architecture"]
    assert "mermaid_diagram" in architecture
    assert "node_descriptions" in architecture
    assert "edge_descriptions" in architecture
    assert "state_schema" in architecture

    # ノード説明の確認
    nodes = architecture["node_descriptions"]
    assert isinstance(nodes, list)
    assert len(nodes) > 0
    node = nodes[0]
    assert "node_id" in node
    assert "name" in node
    assert "purpose" in node
    assert "description" in node
    assert "inputs" in node
    assert "outputs" in node

    # エッジ説明の確認
    edges = architecture["edge_descriptions"]
    assert isinstance(edges, list)
    assert len(edges) > 0
    edge = edges[0]
    assert "from_node" in edge
    assert "to_node" in edge
    assert "description" in edge

    # コード例が含まれること
    assert "code_example" in data
    code = data["code_example"]
    assert "language" in code
    assert code["language"] == "python"
    assert "code" in code
    assert "explanation" in code

    # ビジネス説明が含まれること
    assert "business_explanation" in data
    assert isinstance(data["business_explanation"], str)
    assert len(data["business_explanation"]) > 0

    # 実装ノートが含まれること
    assert "implementation_notes" in data
    assert isinstance(data["implementation_notes"], list)

    # メタデータが含まれること
    assert "metadata" in data
    assert "model" in data["metadata"]
    assert "tokens_used" in data["metadata"]
    assert "response_time" in data["metadata"]


def test_architect_generate_without_optional_fields(authenticated_client, mock_architect_graph):
    """オプションフィールドなしでの構成案生成テスト"""
    with patch("backend.api.v1.architect.get_architect_graph", return_value=mock_architect_graph):
        response = authenticated_client.post(
            "/api/v1/architect/generate",
            json={
                "business_challenge": "簡単な自動化システムを作りたい",
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "challenge_analysis" in data
    assert "architecture" in data


def test_architect_generate_empty_challenge(authenticated_client):
    """空のビジネス課題でのバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/architect/generate",
        json={
            "business_challenge": "",
        },
    )

    assert response.status_code == 422  # Pydantic validation error


def test_architect_generate_challenge_too_short(authenticated_client):
    """ビジネス課題が短すぎる場合のバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/architect/generate",
        json={
            "business_challenge": "短い",  # min_length=10
        },
    )

    assert response.status_code == 422


def test_architect_generate_challenge_too_long(authenticated_client):
    """ビジネス課題が長すぎる場合のバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/architect/generate",
        json={
            "business_challenge": "あ" * 2001,  # max_length=2000
        },
    )

    assert response.status_code == 422


def test_architect_generate_too_many_constraints(authenticated_client):
    """制約が多すぎる場合のバリデーションエラーテスト"""
    response = authenticated_client.post(
        "/api/v1/architect/generate",
        json={
            "business_challenge": "システムを作りたい" * 5,
            "constraints": ["制約" + str(i) for i in range(11)],  # max_length=10
        },
    )

    assert response.status_code == 422


def test_architect_generate_llm_error(authenticated_client, mock_architect_graph):
    """LLMエラー時のテスト"""
    from src.utils.exceptions import LLMError

    mock_architect_graph.generate_architecture.side_effect = LLMError("OpenAI API error")

    with patch("backend.api.v1.architect.get_architect_graph", return_value=mock_architect_graph):
        response = authenticated_client.post(
            "/api/v1/architect/generate",
            json={
                "business_challenge": "システムを作りたい" * 5,
            },
        )

    assert response.status_code == 500
    assert "LLMエラー" in response.json()["detail"]


def test_architect_generate_validation_error(authenticated_client, mock_architect_graph):
    """バリデーションエラー時のテスト"""
    from src.utils.exceptions import ValidationError

    mock_architect_graph.generate_architecture.side_effect = ValidationError(
        "Invalid business challenge"
    )

    with patch("backend.api.v1.architect.get_architect_graph", return_value=mock_architect_graph):
        response = authenticated_client.post(
            "/api/v1/architect/generate",
            json={
                "business_challenge": "システムを作りたい" * 5,
            },
        )

    assert response.status_code == 400
    assert "バリデーションエラー" in response.json()["detail"]


def test_architect_generate_with_japanese_input(authenticated_client, mock_architect_graph):
    """日本語入力での構成案生成テスト"""
    with patch("backend.api.v1.architect.get_architect_graph", return_value=mock_architect_graph):
        response = authenticated_client.post(
            "/api/v1/architect/generate",
            json={
                "business_challenge": "在庫管理システムの自動化を実現したい。リアルタイムで在庫状況を把握し、発注を自動化する仕組みが必要。",
                "industry": "製造業",
                "constraints": ["既存のERPシステムと連携", "日本語対応"],
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "challenge_analysis" in data
    assert "architecture" in data


def test_architect_generate_with_english_input(authenticated_client, mock_architect_graph):
    """英語入力での構成案生成テスト"""
    with patch("backend.api.v1.architect.get_architect_graph", return_value=mock_architect_graph):
        response = authenticated_client.post(
            "/api/v1/architect/generate",
            json={
                "business_challenge": "I want to automate customer support. Need a system that can automatically answer FAQs and escalate complex inquiries to humans.",
                "industry": "E-commerce",
                "constraints": ["Must support English", "Integrate with Zendesk"],
            },
        )

    assert response.status_code == 200
    data = response.json()
    assert "challenge_analysis" in data
    assert "architecture" in data
