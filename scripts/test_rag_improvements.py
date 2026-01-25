"""
LangGraph Catalyst - RAG Improvements Test Script

RAG機能の改善をテストするスクリプト。
- コード提示の制御
- LangChainドキュメントの活用
- エラーハンドリング
"""

import sys
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.features.rag.chain import RAGChain
from src.features.rag.vectorstore import ChromaVectorStore

# カラー出力用のANSIエスケープコード
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_section(title: str):
    """セクションタイトルを表示"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_test_case(number: int, question: str, expected_code: bool):
    """テストケースを表示"""
    expected = "コード含む" if expected_code else "概念説明のみ"
    print(f"{Colors.OKBLUE}{Colors.BOLD}Test Case {number}:{Colors.ENDC}")
    print(f"{Colors.OKCYAN}質問: {question}{Colors.ENDC}")
    print(f"{Colors.WARNING}期待: {expected}{Colors.ENDC}")


def print_result(response: dict, test_num: int):
    """テスト結果を表示"""
    print(f"\n{Colors.OKGREEN}--- Result {test_num} ---{Colors.ENDC}")
    print(f"{Colors.BOLD}回答:{Colors.ENDC}")
    print(response['answer'][:300] + "..." if len(response['answer']) > 300 else response['answer'])

    print(f"\n{Colors.BOLD}メタデータ:{Colors.ENDC}")
    print(f"  - Model: {response['metadata']['model']}")
    print(f"  - Tokens: {response['metadata']['tokens_used']}")
    print(f"  - Response Time: {response['metadata']['response_time']:.2f}s")
    print(f"  - Confidence: {response['confidence']:.2f}")

    print(f"\n{Colors.BOLD}ソース数: {len(response['sources'])}{Colors.ENDC}")
    for i, source in enumerate(response['sources'][:2], 1):
        print(f"  {i}. {source['title']} ({source['url']})")

    print(f"\n{Colors.BOLD}コード例数: {len(response['code_examples'])}{Colors.ENDC}")
    if response['code_examples']:
        for i, code_ex in enumerate(response['code_examples'][:2], 1):
            print(f"  {i}. {code_ex['language']} - {code_ex['description']}")


def main():
    """メイン処理"""
    print_section("LangGraph Catalyst - RAG Improvements Test")

    # ベクトルストアとRAGチェーンの初期化
    print(f"{Colors.OKCYAN}Initializing RAG system...{Colors.ENDC}")
    vectorstore = ChromaVectorStore()
    rag_chain = RAGChain(vectorstore=vectorstore)
    print(f"{Colors.OKGREEN}✅ RAG system initialized{Colors.ENDC}\n")

    # テストケース定義
    test_cases = [
        # カテゴリ1: 概念的な質問（コードなし期待）
        {
            "category": "概念的な質問（コードなし期待）",
            "questions": [
                ("LangGraphとは何ですか？", False),
                ("StateGraphの役割を教えてください", False),
                ("LangGraphとLangChainの違いは？", False),
            ]
        },
        # カテゴリ2: 実装の質問（コードあり期待）
        {
            "category": "実装の質問（コードあり期待）",
            "questions": [
                ("LangGraphでグラフを作る方法のコードを見せてください", True),
                ("conditional edgeの実装例を教えて", True),
                ("StateGraphのサンプルコードを書いて", True),
            ]
        },
        # カテゴリ3: LangChainエコシステムの質問
        {
            "category": "LangChainエコシステムの質問",
            "questions": [
                ("エージェントとは何ですか？", False),
                ("ツールの使い方を教えてください", False),
                ("メッセージの構造について説明してください", False),
            ]
        },
    ]

    total_tests = sum(len(cat["questions"]) for cat in test_cases)
    current_test = 0

    # 各カテゴリのテストを実行
    for category_data in test_cases:
        print_section(category_data["category"])

        for question, expected_code in category_data["questions"]:
            current_test += 1
            print_test_case(current_test, question, expected_code)

            try:
                # RAGクエリ実行（include_code_examples=Noneで自動判定）
                response = rag_chain.query(
                    question=question,
                    k=3,
                    include_sources=True,
                    include_code_examples=None  # 自動判定
                )

                print_result(response, current_test)

                # コード検出の検証
                has_code = len(response['code_examples']) > 0
                if has_code == expected_code:
                    print(f"{Colors.OKGREEN}✅ コード検出: 期待通り{Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}⚠️  コード検出: 期待と異なる (期待: {expected_code}, 実際: {has_code}){Colors.ENDC}")

            except Exception as e:
                print(f"{Colors.FAIL}❌ Error: {e}{Colors.ENDC}")

            print()

    # エラーハンドリングテスト
    print_section("エラーハンドリングテスト")

    # テスト: 空の質問
    print(f"{Colors.OKBLUE}{Colors.BOLD}Test Case: 空の質問{Colors.ENDC}")
    try:
        response = rag_chain.query("")
        print(f"{Colors.FAIL}❌ エラーが発生しませんでした（期待: ValidationError）{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.OKGREEN}✅ 正しくエラーが発生: {type(e).__name__}{Colors.ENDC}")

    print()

    # サマリー
    print_section("テスト完了")
    print(f"{Colors.OKGREEN}✅ 合計 {total_tests + 1} 件のテストを実行しました{Colors.ENDC}")
    print(f"\n{Colors.OKCYAN}Streamlit UIでも確認してください:{Colors.ENDC}")
    print(f"  {Colors.BOLD}http://localhost:8502{Colors.ENDC}")
    print()


if __name__ == "__main__":
    main()
