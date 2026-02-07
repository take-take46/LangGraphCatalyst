"""
ArchitectGraph機能の簡易テストスクリプト
"""

import os
import sys

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.config.settings import settings
from src.features.architect.graph import ArchitectGraph


def test_architect_graph():
    """ArchitectGraphの基本的な動作テスト"""
    print("=" * 60)
    print("ArchitectGraph 動作テスト")
    print("=" * 60)

    # ArchitectGraphの初期化
    print("\n1. ArchitectGraphの初期化...")
    try:
        architect = ArchitectGraph(
            llm_model="gpt-4-turbo-preview",
            temperature=0.7,
        )
        print("✅ ArchitectGraphの初期化成功")
    except Exception as e:
        print(f"❌ ArchitectGraphの初期化失敗: {e}")
        return

    # サンプル課題で構成案生成
    print("\n2. サンプル課題での構成案生成...")
    business_challenge = """
    カスタマーサポートの自動化を実現したい。
    FAQへの自動回答と、複雑な問い合わせは人間にエスカレーションする仕組みが必要。
    """
    industry = "EC"
    constraints = ["日本語対応必須", "既存のZendeskと連携"]

    print(f"課題: {business_challenge.strip()}")
    print(f"業界: {industry}")
    print(f"制約: {constraints}")

    try:
        print("\n構成案を生成中... (30秒〜1分程度かかる場合があります)")
        result = architect.generate_architecture(
            business_challenge=business_challenge,
            industry=industry,
            constraints=constraints,
        )
        print("✅ 構成案生成成功")

        # 結果の表示
        print("\n" + "=" * 60)
        print("生成結果")
        print("=" * 60)

        # 課題分析
        print("\n【課題分析】")
        print(f"要約: {result['challenge_analysis'].get('summary', '')[:100]}...")
        print(f"主要要件: {len(result['challenge_analysis'].get('key_requirements', []))}件")

        # アーキテクチャ
        print("\n【アーキテクチャ】")
        print(f"ノード数: {len(result['architecture']['node_descriptions'])}")
        print(f"エッジ数: {len(result['architecture']['edge_descriptions'])}")
        print(f"Mermaid図: {'生成済み' if result['architecture']['mermaid_diagram'] else '未生成'}")

        # コード例
        print("\n【コード例】")
        if result["code_example"]:
            code_lines = result["code_example"]["code"].split("\n")
            print(f"コード行数: {len(code_lines)}")
            print(f"説明: {result['code_example'].get('explanation', '')[:100]}...")
        else:
            print("コード例なし")

        # ビジネス説明
        print("\n【ビジネス説明】")
        print(f"{result['business_explanation'][:200]}...")

        # 実装ノート
        print("\n【実装ノート】")
        print(f"ノート数: {len(result['implementation_notes'])}")

        # メタデータ
        print("\n【メタデータ】")
        print(f"使用モデル: {result['metadata']['model']}")
        print(f"生成時間: {result['metadata']['response_time']:.2f}秒")

        print("\n✅ テスト完了")

    except Exception as e:
        print(f"❌ 構成案生成失敗: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # 環境変数チェック
    if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key":
        print("❌ OPENAI_API_KEYが設定されていません")
        print("'.env'ファイルにOPENAI_API_KEYを設定してください")
        sys.exit(1)

    test_architect_graph()
