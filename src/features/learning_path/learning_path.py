"""
LangGraph 学習パス データ定義

初級から上級までの構造化された学習カリキュラム。
"""

from typing import TypedDict


class Topic(TypedDict):
    """学習トピック型定義"""

    id: str
    level: str  # "初級", "中級", "上級"
    order: int  # レベル内での順序
    title: str
    description: str
    learning_objectives: list[str]  # 学習目標
    sample_questions: list[str]  # RAGに投げるサンプル質問
    prerequisites: list[str]  # 前提知識
    estimated_time: str  # 推定学習時間
    resources: list[dict]  # 参考リソース


# 学習パス全体の定義
LEARNING_PATH: list[Topic] = [
    # ========== 初級レベル ==========
    {
        "id": "beginner_01",
        "level": "初級",
        "order": 1,
        "title": "LangGraphとは何か",
        "description": "LangGraphの基本概念と、なぜLangGraphが必要なのかを理解します",
        "learning_objectives": [
            "LangGraphの概要を説明できる",
            "従来のLangChainとの違いを理解する",
            "LangGraphが解決する問題を説明できる",
        ],
        "sample_questions": [
            "LangGraphとは何ですか？",
            "LangGraphとLangChainの違いは？",
            "LangGraphを使うメリットは何ですか？",
        ],
        "prerequisites": [],
        "estimated_time": "20分",
        "resources": [
            {"type": "公式ドキュメント", "url": "https://langchain-ai.github.io/langgraph/"},
        ],
    },
    {
        "id": "beginner_02",
        "level": "初級",
        "order": 2,
        "title": "Node（ノード）の基礎",
        "description": "グラフの基本要素であるNodeの概念と実装方法を学びます",
        "learning_objectives": [
            "Nodeの役割を理解する",
            "Node関数の実装方法を理解する",
            "Stateの受け渡し方を理解する",
        ],
        "sample_questions": [
            "LangGraphのNodeとは何ですか？",
            "Node関数の書き方を教えてください",
            "NodeでStateを更新する方法は？",
        ],
        "prerequisites": ["LangGraphとは何か"],
        "estimated_time": "30分",
        "resources": [
            {"type": "公式ドキュメント", "url": "https://langchain-ai.github.io/langgraph/concepts/"},
        ],
    },
    {
        "id": "beginner_03",
        "level": "初級",
        "order": 3,
        "title": "Edge（エッジ）の基礎",
        "description": "ノード間の接続を表すEdgeの概念と使い方を学びます",
        "learning_objectives": [
            "Edgeの役割を理解する",
            "add_edgeの使い方を理解する",
            "グラフのフロー制御の基本を理解する",
        ],
        "sample_questions": [
            "LangGraphのEdgeとは何ですか？",
            "add_edgeの使い方を教えてください",
            "Nodeをつなげる方法は？",
        ],
        "prerequisites": ["Node（ノード）の基礎"],
        "estimated_time": "25分",
        "resources": [],
    },
    {
        "id": "beginner_04",
        "level": "初級",
        "order": 4,
        "title": "State（状態）の管理",
        "description": "グラフ全体で共有されるStateの定義と管理方法を学びます",
        "learning_objectives": [
            "Stateの役割を理解する",
            "TypedDictでStateを定義する方法を理解する",
            "State更新のパターンを理解する",
        ],
        "sample_questions": [
            "LangGraphのStateとは何ですか？",
            "Stateの定義方法を教えてください",
            "Stateを更新する方法は？",
        ],
        "prerequisites": ["Node（ノード）の基礎"],
        "estimated_time": "30分",
        "resources": [],
    },
    {
        "id": "beginner_05",
        "level": "初級",
        "order": 5,
        "title": "StateGraphの作成",
        "description": "実際にStateGraphを作成し、最初のワークフローを実装します",
        "learning_objectives": [
            "StateGraphの基本的な作成手順を理解する",
            "compile()の役割を理解する",
            "invoke()でグラフを実行する方法を理解する",
        ],
        "sample_questions": [
            "StateGraphの作り方を教えてください",
            "最初のLangGraphアプリを作るには？",
            "グラフをコンパイルして実行する方法は？",
        ],
        "prerequisites": ["Node（ノード）の基礎", "Edge（エッジ）の基礎", "State（状態）の管理"],
        "estimated_time": "40分",
        "resources": [
            {"type": "GitHub例", "url": "https://github.com/langchain-ai/langgraph/tree/main/examples"},
        ],
    },
    # ========== 中級レベル ==========
    {
        "id": "intermediate_01",
        "level": "中級",
        "order": 1,
        "title": "条件分岐（Conditional Edges）",
        "description": "Stateに基づいて次のノードを動的に決定する条件分岐を実装します",
        "learning_objectives": [
            "add_conditional_edgesの使い方を理解する",
            "ルーティング関数の実装方法を理解する",
            "複雑なフロー制御を実装できる",
        ],
        "sample_questions": [
            "条件分岐の実装方法を教えてください",
            "add_conditional_edgesの使い方は？",
            "ルーティング関数の書き方は？",
        ],
        "prerequisites": ["StateGraphの作成"],
        "estimated_time": "45分",
        "resources": [],
    },
    {
        "id": "intermediate_02",
        "level": "中級",
        "order": 2,
        "title": "サブグラフ",
        "description": "複雑なワークフローをモジュール化するためのサブグラフを理解します",
        "learning_objectives": [
            "サブグラフの概念を理解する",
            "サブグラフの作成方法を理解する",
            "サブグラフの再利用方法を理解する",
        ],
        "sample_questions": [
            "サブグラフとは何ですか？",
            "サブグラフの作り方を教えてください",
            "グラフをモジュール化する方法は？",
        ],
        "prerequisites": ["StateGraphの作成"],
        "estimated_time": "50分",
        "resources": [],
    },
    {
        "id": "intermediate_03",
        "level": "中級",
        "order": 3,
        "title": "エラーハンドリング",
        "description": "ノード実行時のエラーを適切に処理する方法を学びます",
        "learning_objectives": [
            "エラーハンドリングの重要性を理解する",
            "try-except の適切な使い方を理解する",
            "エラー時のリトライ戦略を実装できる",
        ],
        "sample_questions": [
            "LangGraphでエラーハンドリングする方法は？",
            "ノードでエラーが発生したときの処理は？",
            "リトライ処理の実装方法は？",
        ],
        "prerequisites": ["StateGraphの作成"],
        "estimated_time": "35分",
        "resources": [],
    },
    {
        "id": "intermediate_04",
        "level": "中級",
        "order": 4,
        "title": "チェックポイントと永続化",
        "description": "ワークフローの状態を保存し、中断・再開を可能にする方法を学びます",
        "learning_objectives": [
            "チェックポイントの概念を理解する",
            "Memoryセーバーの使い方を理解する",
            "長時間実行ワークフローの管理方法を理解する",
        ],
        "sample_questions": [
            "チェックポイントとは何ですか？",
            "ワークフローの状態を保存する方法は？",
            "中断したワークフローを再開する方法は？",
        ],
        "prerequisites": ["StateGraphの作成"],
        "estimated_time": "40分",
        "resources": [],
    },
    {
        "id": "intermediate_05",
        "level": "中級",
        "order": 5,
        "title": "並列実行",
        "description": "複数のノードを並列で実行してパフォーマンスを向上させます",
        "learning_objectives": [
            "並列実行の概念を理解する",
            "並列実行のパターンを実装できる",
            "並列実行時の注意点を理解する",
        ],
        "sample_questions": [
            "LangGraphで並列実行する方法は？",
            "複数のノードを同時に実行するには？",
            "並列実行のベストプラクティスは？",
        ],
        "prerequisites": ["条件分岐（Conditional Edges）"],
        "estimated_time": "45分",
        "resources": [],
    },
    # ========== 上級レベル ==========
    {
        "id": "advanced_01",
        "level": "上級",
        "order": 1,
        "title": "Human-in-the-Loop（ヒューマンインザループ）",
        "description": "ワークフロー中に人間の判断を組み込む高度なパターンを実装します",
        "learning_objectives": [
            "Human-in-the-Loopの概念を理解する",
            "interrupt()の使い方を理解する",
            "人間の介入ポイントを適切に設計できる",
        ],
        "sample_questions": [
            "Human-in-the-Loopとは何ですか？",
            "人間の判断をワークフローに組み込む方法は？",
            "interruptの使い方を教えてください",
        ],
        "prerequisites": ["チェックポイントと永続化"],
        "estimated_time": "60分",
        "resources": [],
    },
    {
        "id": "advanced_02",
        "level": "上級",
        "order": 2,
        "title": "ストリーミング",
        "description": "ワークフローの実行状況をリアルタイムで配信する方法を学びます",
        "learning_objectives": [
            "ストリーミングの概念を理解する",
            "stream()メソッドの使い方を理解する",
            "リアルタイムUIを実装できる",
        ],
        "sample_questions": [
            "LangGraphでストリーミングする方法は？",
            "実行状況をリアルタイムで表示するには？",
            "streamメソッドの使い方は？",
        ],
        "prerequisites": ["StateGraphの作成"],
        "estimated_time": "50分",
        "resources": [],
    },
    {
        "id": "advanced_03",
        "level": "上級",
        "order": 3,
        "title": "マルチエージェント システム",
        "description": "複数の専門エージェントを協調動作させる高度なシステムを構築します",
        "learning_objectives": [
            "マルチエージェントの設計パターンを理解する",
            "エージェント間の通信方法を理解する",
            "複雑なエージェントシステムを設計できる",
        ],
        "sample_questions": [
            "マルチエージェントシステムの作り方は？",
            "複数のエージェントを協調動作させる方法は？",
            "エージェント間で情報を共有するには？",
        ],
        "prerequisites": ["条件分岐（Conditional Edges）", "並列実行"],
        "estimated_time": "90分",
        "resources": [
            {"type": "ブログ", "url": "https://blog.langchain.dev/tag/langgraph/"},
        ],
    },
    {
        "id": "advanced_04",
        "level": "上級",
        "order": 4,
        "title": "パフォーマンス最適化",
        "description": "LangGraphアプリケーションのパフォーマンスを最適化する手法を学びます",
        "learning_objectives": [
            "ボトルネックの特定方法を理解する",
            "キャッシング戦略を実装できる",
            "非同期実行を活用できる",
        ],
        "sample_questions": [
            "LangGraphアプリを高速化する方法は？",
            "パフォーマンスのボトルネックを見つけるには？",
            "非同期実行の実装方法は？",
        ],
        "prerequisites": ["並列実行"],
        "estimated_time": "60分",
        "resources": [],
    },
    {
        "id": "advanced_05",
        "level": "上級",
        "order": 5,
        "title": "本番デプロイとモニタリング",
        "description": "LangGraphアプリケーションを本番環境にデプロイし、運用する方法を学びます",
        "learning_objectives": [
            "デプロイのベストプラクティスを理解する",
            "ロギングとモニタリングを実装できる",
            "スケーリング戦略を理解する",
        ],
        "sample_questions": [
            "LangGraphアプリをデプロイする方法は？",
            "本番環境でのモニタリング方法は？",
            "スケーリングのベストプラクティスは？",
        ],
        "prerequisites": ["パフォーマンス最適化"],
        "estimated_time": "75分",
        "resources": [],
    },
]


def get_level_topics(level: str) -> list[Topic]:
    """指定レベルのトピックを取得"""
    return [t for t in LEARNING_PATH if t["level"] == level]


def get_all_topics() -> list[Topic]:
    """全トピックを取得"""
    return LEARNING_PATH


def get_topic_by_id(topic_id: str) -> Topic | None:
    """IDでトピックを取得"""
    for topic in LEARNING_PATH:
        if topic["id"] == topic_id:
            return topic
    return None


def calculate_progress(completed_ids: list[str]) -> dict:
    """進捗を計算"""
    total = len(LEARNING_PATH)
    completed = len([t for t in LEARNING_PATH if t["id"] in completed_ids])

    # レベル別の進捗
    beginner_total = len([t for t in LEARNING_PATH if t["level"] == "初級"])
    beginner_completed = len(
        [t for t in LEARNING_PATH if t["level"] == "初級" and t["id"] in completed_ids]
    )

    intermediate_total = len([t for t in LEARNING_PATH if t["level"] == "中級"])
    intermediate_completed = len(
        [t for t in LEARNING_PATH if t["level"] == "中級" and t["id"] in completed_ids]
    )

    advanced_total = len([t for t in LEARNING_PATH if t["level"] == "上級"])
    advanced_completed = len(
        [t for t in LEARNING_PATH if t["level"] == "上級" and t["id"] in completed_ids]
    )

    return {
        "total_progress": completed / total if total > 0 else 0,
        "completed_count": completed,
        "total_count": total,
        "levels": {
            "初級": {
                "progress": beginner_completed / beginner_total if beginner_total > 0 else 0,
                "completed": beginner_completed,
                "total": beginner_total,
            },
            "中級": {
                "progress": intermediate_completed / intermediate_total
                if intermediate_total > 0
                else 0,
                "completed": intermediate_completed,
                "total": intermediate_total,
            },
            "上級": {
                "progress": advanced_completed / advanced_total if advanced_total > 0 else 0,
                "completed": advanced_completed,
                "total": advanced_total,
            },
        },
    }
