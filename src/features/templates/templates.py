"""
LangGraph テンプレートデータ定義

ユースケース別のLangGraphテンプレートコレクション。
"""

from typing import TypedDict


class Template(TypedDict):
    """テンプレート型定義"""

    id: str
    title: str
    description: str
    category: str
    difficulty: str  # "初級", "中級", "上級"
    code: str
    mermaid: str
    explanation: str
    use_cases: list[str]
    tags: list[str]


# テンプレートカテゴリ
TEMPLATE_CATEGORIES = {
    "customer_support": "カスタマーサポート",
    "data_analysis": "データ分析",
    "content_generation": "コンテンツ生成",
    "workflow_automation": "ワークフロー自動化",
    "multi_agent": "マルチエージェント",
}

# テンプレートデータ
TEMPLATES: list[Template] = [
    # 1. カスタマーサポート自動化（初級）
    {
        "id": "customer_support_basic",
        "title": "カスタマーサポート自動化（基本）",
        "description": "FAQ検索と人間へのエスカレーションを組み合わせたシンプルなサポートフロー",
        "category": "customer_support",
        "difficulty": "初級",
        "code": '''"""
カスタマーサポート自動化 - 基本テンプレート
FAQ検索 → 意図分析 → 自動回答 or 人間にエスカレーション
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 状態定義
class SupportState(TypedDict):
    query: str
    user_id: str
    faq_match: bool
    complexity: str  # "simple" or "complex"
    response: str
    escalated: bool

# ノード定義
def faq_search(state: SupportState) -> SupportState:
    """FAQ検索ノード"""
    query = state["query"]
    # 実際にはベクトル検索などを実装
    faq_match = "返品" in query or "配送" in query
    return {**state, "faq_match": faq_match}

def analyze_complexity(state: SupportState) -> SupportState:
    """複雑度分析ノード"""
    query = state["query"]
    # 実際にはLLMで判定
    complexity = "simple" if len(query) < 50 else "complex"
    return {**state, "complexity": complexity}

def auto_respond(state: SupportState) -> SupportState:
    """自動回答ノード"""
    response = f"ご質問ありがとうございます。{state['query']}に関する回答は..."
    return {**state, "response": response, "escalated": False}

def escalate_to_human(state: SupportState) -> SupportState:
    """人間へのエスカレーションノード"""
    response = "担当者におつなぎします。少々お待ちください。"
    return {**state, "response": response, "escalated": True}

# ルーティング関数
def should_escalate(state: SupportState) -> str:
    """エスカレーション判定"""
    if not state["faq_match"]:
        return "escalate"
    if state["complexity"] == "complex":
        return "escalate"
    return "respond"

# グラフ構築
workflow = StateGraph(SupportState)

# ノード追加
workflow.add_node("faq_search", faq_search)
workflow.add_node("analyze", analyze_complexity)
workflow.add_node("respond", auto_respond)
workflow.add_node("escalate", escalate_to_human)

# エッジ追加
workflow.set_entry_point("faq_search")
workflow.add_edge("faq_search", "analyze")
workflow.add_conditional_edges(
    "analyze",
    should_escalate,
    {
        "respond": "respond",
        "escalate": "escalate",
    }
)
workflow.add_edge("respond", END)
workflow.add_edge("escalate", END)

# グラフのコンパイル
app = workflow.compile()

# 実行例
if __name__ == "__main__":
    result = app.invoke({
        "query": "商品を返品したいのですが",
        "user_id": "user123",
        "faq_match": False,
        "complexity": "",
        "response": "",
        "escalated": False
    })
    print(f"Response: {result['response']}")
    print(f"Escalated: {result['escalated']}")
''',
        "mermaid": """graph TD
    A[問い合わせ受付] --> B[FAQ検索]
    B --> C[複雑度分析]
    C --> D{判定}
    D -->|シンプル & FAQ一致| E[自動回答]
    D -->|複雑 or FAQ不一致| F[人間にエスカレーション]
    E --> G[完了]
    F --> G[完了]

    style A fill:#667eea,color:#fff
    style E fill:#28a745,color:#fff
    style F fill:#ffc107,color:#333
    style G fill:#17a2b8,color:#fff""",
        "explanation": "お客様からの問い合わせをまず自動的にFAQデータベースで検索します。"
        "見つかった場合でも、質問が複雑な場合は人間のオペレーターにエスカレーションします。"
        "シンプルな質問にはAIが自動で回答し、複雑な質問は人間が対応することで、"
        "効率と品質のバランスを保ちます。",
        "use_cases": [
            "ECサイトの返品・配送に関する問い合わせ対応",
            "製品の使い方に関する一次サポート",
            "よくある質問への24時間自動対応",
        ],
        "tags": ["FAQ", "エスカレーション", "条件分岐", "初心者向け"],
    },
    # 2. データ分析パイプライン（中級）
    {
        "id": "data_analysis_pipeline",
        "title": "データ分析パイプライン",
        "description": "データ取得、前処理、分析、レポート生成の一連の流れを自動化",
        "category": "data_analysis",
        "difficulty": "中級",
        "code": '''"""
データ分析パイプライン - 中級テンプレート
データ取得 → 前処理 → 分析 → レポート生成
"""

from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

# 状態定義
class AnalysisState(TypedDict):
    data_source: str
    raw_data: Any
    cleaned_data: Any
    analysis_results: dict
    report: str
    error: str | None

# ノード定義
def fetch_data(state: AnalysisState) -> AnalysisState:
    """データ取得ノード"""
    # 実際にはAPI呼び出しやDB接続
    raw_data = {"sales": [100, 200, 150, 300], "dates": ["2024-01", "2024-02", "2024-03", "2024-04"]}
    return {**state, "raw_data": raw_data}

def clean_data(state: AnalysisState) -> AnalysisState:
    """データ前処理ノード"""
    raw_data = state["raw_data"]
    # 実際にはpandasなどで処理
    cleaned_data = {
        "sales": [x for x in raw_data["sales"] if x > 0],
        "dates": raw_data["dates"]
    }
    return {**state, "cleaned_data": cleaned_data}

def analyze_data(state: AnalysisState) -> AnalysisState:
    """データ分析ノード"""
    data = state["cleaned_data"]
    # 実際には統計分析、ML予測など
    total_sales = sum(data["sales"])
    avg_sales = total_sales / len(data["sales"])

    analysis_results = {
        "total_sales": total_sales,
        "average_sales": avg_sales,
        "trend": "increasing" if data["sales"][-1] > data["sales"][0] else "decreasing"
    }
    return {**state, "analysis_results": analysis_results}

def generate_report(state: AnalysisState) -> AnalysisState:
    """レポート生成ノード"""
    results = state["analysis_results"]
    report = f"""
## 営業データ分析レポート

**期間:** {state["cleaned_data"]["dates"][0]} - {state["cleaned_data"]["dates"][-1]}

### サマリー
- 総売上: ¥{results["total_sales"]:,}
- 平均売上: ¥{results["average_sales"]:,.0f}
- トレンド: {results["trend"]}

### 推奨アクション
{"売上は増加傾向にあります。この勢いを維持しましょう。" if results["trend"] == "increasing" else "売上が減少しています。対策が必要です。"}
    """
    return {**state, "report": report.strip()}

# グラフ構築
workflow = StateGraph(AnalysisState)

workflow.add_node("fetch", fetch_data)
workflow.add_node("clean", clean_data)
workflow.add_node("analyze", analyze_data)
workflow.add_node("report", generate_report)

workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "clean")
workflow.add_edge("clean", "analyze")
workflow.add_edge("analyze", "report")
workflow.add_edge("report", END)

app = workflow.compile()

# 実行例
if __name__ == "__main__":
    result = app.invoke({
        "data_source": "sales_db",
        "raw_data": None,
        "cleaned_data": None,
        "analysis_results": {},
        "report": "",
        "error": None
    })
    print(result["report"])
''',
        "mermaid": """graph LR
    A[データ取得] --> B[前処理]
    B --> C[データ分析]
    C --> D[レポート生成]
    D --> E[完了]

    style A fill:#667eea,color:#fff
    style B fill:#17a2b8,color:#fff
    style C fill:#764ba2,color:#fff
    style D fill:#28a745,color:#fff
    style E fill:#ffc107,color:#333""",
        "explanation": "営業データなどを自動的に取得し、前処理（クリーニング）を行い、"
        "統計分析や予測を実施します。最終的に経営層向けのレポートを自動生成します。"
        "毎週自動実行することで、週次レポート作成の工数を大幅に削減できます。",
        "use_cases": [
            "営業データの週次分析レポート自動生成",
            "在庫データの異常検知と通知",
            "顧客行動分析とインサイト抽出",
        ],
        "tags": ["データ分析", "レポート生成", "自動化", "ビジネスインテリジェンス"],
    },
    # 3. コンテンツ生成ワークフロー（中級）
    {
        "id": "content_generation_workflow",
        "title": "コンテンツ生成ワークフロー",
        "description": "アイデア生成→下書き→レビュー→公開の一連のコンテンツ作成プロセス",
        "category": "content_generation",
        "difficulty": "中級",
        "code": '''"""
コンテンツ生成ワークフロー - 中級テンプレート
アイデア生成 → 下書き → レビュー → 修正 → 公開
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 状態定義
class ContentState(TypedDict):
    topic: str
    ideas: list[str]
    draft: str
    review_feedback: str
    final_content: str
    approved: bool
    revision_count: int

# ノード定義
def generate_ideas(state: ContentState) -> ContentState:
    """アイデア生成ノード"""
    topic = state["topic"]
    # 実際にはLLMで複数アイデアを生成
    ideas = [
        f"{topic}の基礎知識",
        f"{topic}の実践例",
        f"{topic}のベストプラクティス",
    ]
    return {**state, "ideas": ideas}

def write_draft(state: ContentState) -> ContentState:
    """下書き作成ノード"""
    ideas = state["ideas"]
    # 実際にはLLMで本文を生成
    draft = f"""
# {state['topic']}について

## はじめに
{state['topic']}は...

## {ideas[0]}
...

## {ideas[1]}
...

## まとめ
今回は{state['topic']}について解説しました。
    """
    return {**state, "draft": draft.strip()}

def review_content(state: ContentState) -> ContentState:
    """レビューノード"""
    draft = state["draft"]
    # 実際にはLLMでレビュー
    review_feedback = "全体的に良い内容です。ただし、具体例を追加してください。"
    approved = len(draft) > 200  # 簡易判定
    return {**state, "review_feedback": review_feedback, "approved": approved}

def revise_content(state: ContentState) -> ContentState:
    """修正ノード"""
    draft = state["draft"]
    feedback = state["review_feedback"]
    # 実際にはLLMでフィードバックに基づき修正
    revised = draft + "\n\n## 具体例\n実際の活用例として..."
    return {**state, "draft": revised, "revision_count": state["revision_count"] + 1}

def publish_content(state: ContentState) -> ContentState:
    """公開ノード"""
    return {**state, "final_content": state["draft"]}

# ルーティング関数
def check_approval(state: ContentState) -> str:
    """承認チェック"""
    if state["approved"]:
        return "publish"
    if state["revision_count"] >= 3:
        return "publish"  # 最大3回まで修正
    return "revise"

# グラフ構築
workflow = StateGraph(ContentState)

workflow.add_node("generate_ideas", generate_ideas)
workflow.add_node("write_draft", write_draft)
workflow.add_node("review", review_content)
workflow.add_node("revise", revise_content)
workflow.add_node("publish", publish_content)

workflow.set_entry_point("generate_ideas")
workflow.add_edge("generate_ideas", "write_draft")
workflow.add_edge("write_draft", "review")
workflow.add_conditional_edges(
    "review",
    check_approval,
    {
        "revise": "revise",
        "publish": "publish",
    }
)
workflow.add_edge("revise", "review")  # 修正後に再レビュー
workflow.add_edge("publish", END)

app = workflow.compile()

# 実行例
if __name__ == "__main__":
    result = app.invoke({
        "topic": "LangGraphの使い方",
        "ideas": [],
        "draft": "",
        "review_feedback": "",
        "final_content": "",
        "approved": False,
        "revision_count": 0
    })
    print(result["final_content"])
''',
        "mermaid": """graph TD
    A[アイデア生成] --> B[下書き作成]
    B --> C[レビュー]
    C --> D{承認?}
    D -->|No| E[修正]
    E --> C
    D -->|Yes| F[公開]
    F --> G[完了]

    style A fill:#667eea,color:#fff
    style B fill:#17a2b8,color:#fff
    style C fill:#ffc107,color:#333
    style E fill:#ff6b6b,color:#fff
    style F fill:#28a745,color:#fff
    style G fill:#764ba2,color:#fff""",
        "explanation": "ブログ記事や技術ドキュメントの作成を自動化します。"
        "トピックを入力すると、AIがアイデアを生成し、下書きを作成します。"
        "自動レビュー機能で品質をチェックし、必要に応じて修正を繰り返します。"
        "最終的に承認された内容を公開します。",
        "use_cases": [
            "ブログ記事の自動生成と公開",
            "技術ドキュメントの作成支援",
            "SNS投稿コンテンツの大量生成",
        ],
        "tags": ["コンテンツ生成", "レビュー", "反復処理", "クリエイティブ"],
    },
    # 4. ドキュメント処理自動化（初級）
    {
        "id": "document_processing",
        "title": "ドキュメント処理自動化",
        "description": "ドキュメントの読み込み、分類、要約、保存の流れを自動化",
        "category": "workflow_automation",
        "difficulty": "初級",
        "code": '''"""
ドキュメント処理自動化 - 初級テンプレート
読み込み → 分類 → 要約 → 保存
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 状態定義
class DocumentState(TypedDict):
    file_path: str
    content: str
    category: str
    summary: str
    saved_path: str

# ノード定義
def load_document(state: DocumentState) -> DocumentState:
    """ドキュメント読み込みノード"""
    # 実際にはファイル読み込み
    content = f"これは{state['file_path']}の内容です..."
    return {**state, "content": content}

def classify_document(state: DocumentState) -> DocumentState:
    """ドキュメント分類ノード"""
    content = state["content"]
    # 実際にはLLMで分類
    if "契約" in content:
        category = "契約書"
    elif "請求" in content:
        category = "請求書"
    else:
        category = "その他"
    return {**state, "category": category}

def summarize_document(state: DocumentState) -> DocumentState:
    """ドキュメント要約ノード"""
    content = state["content"]
    # 実際にはLLMで要約
    summary = f"{state['category']}の要約: " + content[:100] + "..."
    return {**state, "summary": summary}

def save_document(state: DocumentState) -> DocumentState:
    """ドキュメント保存ノード"""
    category = state["category"]
    # 実際にはファイル保存
    saved_path = f"/archive/{category}/{state['file_path']}"
    return {**state, "saved_path": saved_path}

# グラフ構築
workflow = StateGraph(DocumentState)

workflow.add_node("load", load_document)
workflow.add_node("classify", classify_document)
workflow.add_node("summarize", summarize_document)
workflow.add_node("save", save_document)

workflow.set_entry_point("load")
workflow.add_edge("load", "classify")
workflow.add_edge("classify", "summarize")
workflow.add_edge("summarize", "save")
workflow.add_edge("save", END)

app = workflow.compile()

# 実行例
if __name__ == "__main__":
    result = app.invoke({
        "file_path": "contract_001.pdf",
        "content": "",
        "category": "",
        "summary": "",
        "saved_path": ""
    })
    print(f"Category: {result['category']}")
    print(f"Summary: {result['summary']}")
    print(f"Saved to: {result['saved_path']}")
''',
        "mermaid": """graph LR
    A[ドキュメント読み込み] --> B[分類]
    B --> C[要約生成]
    C --> D[保存]
    D --> E[完了]

    style A fill:#667eea,color:#fff
    style B fill:#ffc107,color:#333
    style C fill:#17a2b8,color:#fff
    style D fill:#28a745,color:#fff
    style E fill:#764ba2,color:#fff""",
        "explanation": "大量のドキュメントを自動的に処理します。"
        "契約書、請求書、レポートなどを自動で分類し、要約を生成して、"
        "適切なフォルダに保存します。手動での仕分け作業を大幅に削減できます。",
        "use_cases": [
            "契約書の自動分類とアーカイブ",
            "メール添付ファイルの自動整理",
            "レポートの要約生成と共有",
        ],
        "tags": ["ドキュメント処理", "分類", "要約", "シンプル"],
    },
    # 5. マルチエージェント調査システム（上級）
    {
        "id": "multi_agent_research",
        "title": "マルチエージェント調査システム",
        "description": "複数の専門エージェントが協力して調査タスクを実行",
        "category": "multi_agent",
        "difficulty": "上級",
        "code": '''"""
マルチエージェント調査システム - 上級テンプレート
タスク分解 → 並列調査 → 統合 → レポート作成
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END

# 状態定義
class ResearchState(TypedDict):
    query: str
    subtasks: list[str]
    web_results: str
    academic_results: str
    news_results: str
    integrated_findings: str
    final_report: str

# ノード定義
def decompose_task(state: ResearchState) -> ResearchState:
    """タスク分解ノード"""
    query = state["query"]
    # 実際にはLLMでサブタスクに分解
    subtasks = [
        f"{query}のWeb情報調査",
        f"{query}の学術論文調査",
        f"{query}の最新ニュース調査",
    ]
    return {**state, "subtasks": subtasks}

def web_search_agent(state: ResearchState) -> ResearchState:
    """Web検索エージェント"""
    # 実際にはWeb検索API呼び出し
    web_results = f"Webから{state['query']}に関する情報を収集しました..."
    return {**state, "web_results": web_results}

def academic_search_agent(state: ResearchState) -> ResearchState:
    """学術論文検索エージェント"""
    # 実際には論文DBを検索
    academic_results = f"{state['query']}に関する学術論文を3件見つけました..."
    return {**state, "academic_results": academic_results}

def news_search_agent(state: ResearchState) -> ResearchState:
    """ニュース検索エージェント"""
    # 実際にはニュースAPI呼び出し
    news_results = f"{state['query']}に関する最新ニュースを5件見つけました..."
    return {**state, "news_results": news_results}

def integrate_findings(state: ResearchState) -> ResearchState:
    """調査結果統合ノード"""
    integrated = f"""
総合調査結果:
- Web情報: {state['web_results']}
- 学術情報: {state['academic_results']}
- ニュース: {state['news_results']}
    """
    return {**state, "integrated_findings": integrated.strip()}

def create_report(state: ResearchState) -> ResearchState:
    """レポート作成ノード"""
    report = f"""
# {state['query']} 調査レポート

## サマリー
{state['integrated_findings']}

## 結論
...
    """
    return {**state, "final_report": report.strip()}

# グラフ構築
workflow = StateGraph(ResearchState)

workflow.add_node("decompose", decompose_task)
workflow.add_node("web_agent", web_search_agent)
workflow.add_node("academic_agent", academic_search_agent)
workflow.add_node("news_agent", news_search_agent)
workflow.add_node("integrate", integrate_findings)
workflow.add_node("report", create_report)

workflow.set_entry_point("decompose")

# 並列実行（各エージェントが同時に動く）
workflow.add_edge("decompose", "web_agent")
workflow.add_edge("decompose", "academic_agent")
workflow.add_edge("decompose", "news_agent")

# 全エージェントの完了後に統合
workflow.add_edge("web_agent", "integrate")
workflow.add_edge("academic_agent", "integrate")
workflow.add_edge("news_agent", "integrate")

workflow.add_edge("integrate", "report")
workflow.add_edge("report", END)

app = workflow.compile()

# 実行例
if __name__ == "__main__":
    result = app.invoke({
        "query": "生成AIの最新動向",
        "subtasks": [],
        "web_results": "",
        "academic_results": "",
        "news_results": "",
        "integrated_findings": "",
        "final_report": ""
    })
    print(result["final_report"])
''',
        "mermaid": """graph TD
    A[タスク分解] --> B[Web検索エージェント]
    A --> C[学術論文エージェント]
    A --> D[ニュース検索エージェント]

    B --> E[結果統合]
    C --> E
    D --> E

    E --> F[レポート作成]
    F --> G[完了]

    style A fill:#667eea,color:#fff
    style B fill:#17a2b8,color:#fff
    style C fill:#17a2b8,color:#fff
    style D fill:#17a2b8,color:#fff
    style E fill:#ffc107,color:#333
    style F fill:#28a745,color:#fff
    style G fill:#764ba2,color:#fff""",
        "explanation": "複数の専門エージェントが並列で調査を実行します。"
        "Web検索、学術論文、最新ニュースの3つのエージェントが同時に動き、"
        "それぞれの専門分野の情報を収集します。最後に全ての情報を統合し、"
        "包括的な調査レポートを作成します。",
        "use_cases": [
            "市場調査の自動化",
            "競合分析レポート作成",
            "技術トレンド調査",
        ],
        "tags": ["マルチエージェント", "並列処理", "調査", "上級者向け"],
    },
]


def get_template_by_id(template_id: str) -> Template | None:
    """IDでテンプレートを取得"""
    for template in TEMPLATES:
        if template["id"] == template_id:
            return template
    return None


def get_templates_by_category(category: str) -> list[Template]:
    """カテゴリでテンプレートをフィルタリング"""
    return [t for t in TEMPLATES if t["category"] == category]


def get_templates_by_difficulty(difficulty: str) -> list[Template]:
    """難易度でテンプレートをフィルタリング"""
    return [t for t in TEMPLATES if t["difficulty"] == difficulty]
