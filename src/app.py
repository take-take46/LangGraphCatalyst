"""
LangGraph Catalyst - Streamlit Application

LangGraphの学習支援とビジネス活用を促進するポートフォリオシステムのメインエントリーポイント。
"""

import os
import sys

# プロジェクトルートをPythonパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st

from src.components.sidebar import render_sidebar
from src.features.rag.chain import RAGChain
from src.features.rag.vectorstore import ChromaVectorStore
from src.features.architect.graph import ArchitectGraph
from src.features.templates import (
    TEMPLATES,
    TEMPLATE_CATEGORIES,
    get_templates_by_category,
    get_templates_by_difficulty,
)
from src.features.learning_path import (
    LEARNING_PATH,
    get_level_topics,
    calculate_progress,
)
from src.utils.exceptions import LLMError, VectorStoreError, ValidationError
from src.utils.styles import inject_custom_css, create_gradient_header, create_feature_card
from src.utils.progress_manager import ProgressManager

# ページ設定（必ず最初に実行）
st.set_page_config(
    page_title="LangGraph Catalyst",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-username/LangGraphCatalyst",
        "Report a bug": "https://github.com/your-username/LangGraphCatalyst/issues",
        "About": """
        # LangGraph Catalyst ⚡

        LangGraphの学習支援とビジネス活用を促進する「触媒（Catalyst）」となるシステム。

        **機能:**
        - RAG学習支援: LangGraphに関する質問に、ソース付きで回答
        - 構成案生成: ビジネス課題からLangGraph構成案を自動生成

        Built with LangGraph, LangChain, and Streamlit
        """,
    },
)


@st.cache_resource
def get_vectorstore() -> ChromaVectorStore:
    """ベクトルストアを取得（キャッシュ）"""
    try:
        return ChromaVectorStore()
    except VectorStoreError as e:
        st.error(f"ベクトルストアの初期化に失敗しました: {e}")
        raise


@st.cache_resource
def get_rag_chain(_vectorstore: ChromaVectorStore) -> RAGChain:
    """RAGチェーンを取得（キャッシュ）"""
    try:
        return RAGChain(
            vectorstore=_vectorstore,
            llm_model=st.session_state.get("llm_model", "gpt-4-turbo-preview"),
            temperature=st.session_state.get("llm_temperature", 0.3),
        )
    except Exception as e:
        st.error(f"RAGチェーンの初期化に失敗しました: {e}")
        raise


@st.cache_resource
def get_architect_graph() -> ArchitectGraph:
    """構成案生成グラフを取得（キャッシュ）"""
    try:
        return ArchitectGraph(
            llm_model=st.session_state.get("llm_model", "gpt-4-turbo-preview"),
            temperature=0.7,  # 創造的な出力のため高めに設定
        )
    except Exception as e:
        st.error(f"ArchitectGraphの初期化に失敗しました: {e}")
        raise


def initialize_session_state():
    """セッション状態の初期化"""
    # モード選択（RAG学習支援 / テンプレート / 構成案生成）
    if "mode" not in st.session_state:
        st.session_state.mode = "RAG学習支援"

    # チャット履歴（RAGモード用）
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 生成結果（構成案生成モード用）
    if "architecture_result" not in st.session_state:
        st.session_state.architecture_result = None

    # LLM設定
    if "llm_temperature" not in st.session_state:
        st.session_state.llm_temperature = 0.3

    if "llm_model" not in st.session_state:
        st.session_state.llm_model = "gpt-4-turbo-preview"

    # 学習パス進捗管理
    if "completed_topics" not in st.session_state:
        # 保存された進捗を読み込む
        progress_manager = ProgressManager()
        st.session_state.completed_topics = progress_manager.load_progress()


def render_header():
    """ヘッダーセクションの描画"""
    # グラデーションヘッダー
    st.markdown(
        create_gradient_header(
            title="⚡ LangGraph Catalyst",
            subtitle="LangGraphの学習支援とビジネス活用を促進する触媒システム"
        ),
        unsafe_allow_html=True,
    )

    # ヘルプセクション（エキスパンダー）
    with st.expander("❓ このシステムについて", expanded=False):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                create_feature_card(
                    icon="📚",
                    title="RAG学習支援",
                    description="LangGraphに関する質問にソース付きで回答"
                ),
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                create_feature_card(
                    icon="📖",
                    title="学習パス",
                    description="初級から上級まで段階的に学習"
                ),
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                create_feature_card(
                    icon="🎨",
                    title="テンプレート",
                    description="即座に使える実装例を提供"
                ),
                unsafe_allow_html=True,
            )

        st.divider()

        st.markdown("""
        ### 💡 使い方のヒント

        - **RAG学習支援**: サイドバーで「RAG学習支援」を選択し、LangGraphに関する質問を入力
        - **学習パス**: 「学習パス」で体系的にLangGraphを学習
        - **テンプレート**: 「テンプレート」で実践的なコード例を参照
        - **構成案生成**: 「構成案生成」でビジネス課題から自動でシステム設計

        ### 🎯 推奨学習フロー

        1. **学習パス**で基礎を固める
        2. **RAG学習支援**で疑問点を解決
        3. **テンプレート**で実装パターンを学ぶ
        4. **構成案生成**で実践的なシステムを設計
        """)


def render_rag_mode():
    """RAG学習支援モードのUI"""
    st.header("📚 RAG学習支援")

    st.info(
        """
        LangGraphに関する質問を入力してください。
        公式ドキュメント、ブログ記事、GitHubリポジトリから関連情報を検索し、
        **ソース付き + コード例付き**で回答します。
        """
    )

    # サンプル質問ボタン
    st.subheader("サンプル質問")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 LangGraphとは？", use_container_width=True):
            st.session_state.sample_question = (
                "LangGraphとは何ですか？基本的な概念を教えてください。"
            )

    with col2:
        if st.button("⚙️ StateGraphの使い方", use_container_width=True):
            st.session_state.sample_question = (
                "StateGraphの基本的な使い方とコード例を教えてください。"
            )

    with col3:
        if st.button("🔄 条件分岐の実装", use_container_width=True):
            st.session_state.sample_question = (
                "LangGraphで条件分岐エッジを実装する方法を教えてください。"
            )

    # 質問入力
    question = st.text_area(
        "質問を入力してください:",
        value=st.session_state.get("sample_question", ""),
        height=100,
        placeholder="例: LangGraphでマルチエージェントシステムを構築する方法は？",
        key="rag_question",
    )

    # 検索実行ボタン
    if st.button("🔎 検索して回答", type="primary", use_container_width=True):
        if question.strip():
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                # ステップ1: ベクトルストアとRAGチェーンの取得
                status_text.text("🔧 システムを初期化中...")
                progress_bar.progress(20)
                vectorstore = get_vectorstore()
                rag_chain = get_rag_chain(vectorstore)

                # ステップ2: 関連ドキュメント検索
                status_text.text("🔍 関連ドキュメントを検索中...")
                progress_bar.progress(40)

                # ステップ3: RAGクエリ実行
                status_text.text("🤖 AIが回答を生成中...")
                progress_bar.progress(60)

                # RAGクエリ実行
                response = rag_chain.query(
                    question=question,
                    k=st.session_state.get("rag_top_k", 5),
                    include_sources=True,
                    include_code_examples=True,
                )

                # ステップ4: 完了
                status_text.text("✅ 回答生成完了！")
                progress_bar.progress(100)

                # プログレスバーを削除
                import time
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()

                # チャット履歴に追加
                st.session_state.chat_history.append({"question": question, "response": response})

                # 回答を表示
                st.success("✅ 回答が見つかりました！")

                # 回答セクション
                st.markdown("### 📝 回答")
                st.markdown(response["answer"])

                # ソースセクション
                if response.get("sources"):
                    st.divider()
                    st.markdown("### 📚 参照ソース")

                    for i, source in enumerate(response["sources"], 1):
                        with st.expander(f"📄 {source['title']}", expanded=(i == 1)):
                            st.markdown(f"**URL:** [{source['url']}]({source['url']})")
                            st.markdown(f"**タイプ:** {source['doc_type']}")
                            st.markdown("**抜粋:**")
                            st.info(source["excerpt"])

                # コード例セクション
                if response.get("code_examples"):
                    st.divider()
                    st.markdown("### 💻 コード例")

                    for i, code_ex in enumerate(response["code_examples"], 1):
                        st.markdown(f"**例 {i}:** {code_ex.get('description', '')}")
                        st.code(code_ex["code"], language=code_ex["language"])

                # メタデータ
                st.divider()
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("信頼度", f"{response['confidence']:.0%}")
                with col2:
                    st.metric("使用トークン", response["metadata"]["tokens_used"])
                with col3:
                    st.metric("応答時間", f"{response['metadata']['response_time']:.2f}秒")

                # sample_questionをクリア
                if "sample_question" in st.session_state:
                    st.session_state.sample_question = ""

            except VectorStoreError as e:
                st.error(f"ベクトルストアエラー: {e}")
                st.info(
                    "ベクトルストアが初期化されていない可能性があります。"
                    "初期データ投入を実行してください。"
                )
            except LLMError as e:
                st.error(f"LLMエラー: {e}")
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")
        else:
            st.warning("質問を入力してください")

    # チャット履歴表示
    if st.session_state.chat_history:
        st.divider()
        st.subheader("📝 最近の質問履歴")

        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            question_preview = (
                chat["question"][:50] + "..." if len(chat["question"]) > 50 else chat["question"]
            )

            with st.expander(f"❓ {question_preview}", expanded=(i == 0)):
                st.markdown("**質問:**")
                st.info(chat["question"])

                st.markdown("**回答:**")
                st.markdown(chat["response"]["answer"])

                # ソース情報を簡易表示
                if chat["response"].get("sources"):
                    st.markdown("**参照ソース:**")
                    for source in chat["response"]["sources"][:3]:
                        st.markdown(f"- [{source['title']}]({source['url']})")

                # メタデータ
                st.caption(
                    f"信頼度: {chat['response']['confidence']:.0%} | "
                    f"応答時間: {chat['response']['metadata']['response_time']:.2f}秒"
                )


def render_learning_path_mode():
    """学習パスモードのUI"""
    st.header("📖 LangGraph 学習パス")

    st.info(
        """
        初級から上級まで、段階的にLangGraphを習得できるカリキュラムです。
        各トピックをクリックして学習し、習得したらチェックマークを付けましょう。
        """
    )

    # 全体の進捗を計算
    progress_data = calculate_progress(st.session_state.completed_topics)

    # 全体進捗バー
    st.subheader("📊 全体の進捗")
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col1:
        st.progress(progress_data["total_progress"])

    with col2:
        st.metric(
            "完了", f"{progress_data['completed_count']}/{progress_data['total_count']}"
        )

    with col3:
        st.metric("達成率", f"{progress_data['total_progress']:.0%}")

    with col4:
        if st.button("🔄 リセット", help="学習進捗をリセットします"):
            progress_manager = ProgressManager()
            progress_manager.reset_progress()
            st.session_state.completed_topics = []
            st.success("進捗をリセットしました")
            st.rerun()

    st.divider()

    # レベル別表示
    levels = ["初級", "中級", "上級"]
    level_icons = {"初級": "🌱", "中級": "🌿", "上級": "🌳"}
    level_colors = {"初級": "#28a745", "中級": "#ffc107", "上級": "#dc3545"}

    for level in levels:
        st.subheader(f"{level_icons[level]} {level}レベル")

        # レベル別進捗
        level_progress = progress_data["levels"][level]
        col1, col2 = st.columns([4, 1])

        with col1:
            st.progress(level_progress["progress"])

        with col2:
            st.caption(f"{level_progress['completed']}/{level_progress['total']} 完了")

        # トピック一覧
        topics = get_level_topics(level)

        for topic in topics:
            is_completed = topic["id"] in st.session_state.completed_topics

            with st.expander(
                f"{'✅ ' if is_completed else '⬜ '}{topic['order']}. {topic['title']}",
                expanded=False,
            ):
                # 説明
                st.markdown(f"**📝 説明:** {topic['description']}")

                # 推定学習時間
                st.caption(f"⏱️ 推定時間: {topic['estimated_time']}")

                # 前提知識
                if topic["prerequisites"]:
                    st.markdown("**📚 前提知識:**")
                    for prereq in topic["prerequisites"]:
                        st.markdown(f"- {prereq}")

                st.markdown("---")

                # 学習目標
                st.markdown("**🎯 学習目標:**")
                for objective in topic["learning_objectives"]:
                    st.markdown(f"- {objective}")

                st.markdown("---")

                # サンプル質問
                st.markdown("**💡 学習に役立つ質問:**")
                for i, question in enumerate(topic["sample_questions"]):
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.markdown(f"{i+1}. {question}")

                    with col2:
                        if st.button(
                            "質問", key=f"ask_{topic['id']}_{i}", use_container_width=True
                        ):
                            # RAGモードに切り替えて質問を設定
                            st.session_state.mode = "RAG学習支援"
                            st.session_state.sample_question = question
                            st.rerun()

                # 参考リソース
                if topic["resources"]:
                    st.markdown("---")
                    st.markdown("**🔗 参考リソース:**")
                    for resource in topic["resources"]:
                        st.markdown(f"- [{resource['type']}]({resource['url']})")

                st.markdown("---")

                # 習得チェックボックス
                col1, col2 = st.columns([1, 3])

                with col1:
                    if is_completed:
                        if st.button(
                            "✅ 習得済み",
                            key=f"complete_{topic['id']}",
                            use_container_width=True,
                        ):
                            # チェックを外す
                            st.session_state.completed_topics.remove(topic["id"])
                            # 進捗を保存
                            progress_manager = ProgressManager()
                            progress_manager.save_progress(st.session_state.completed_topics)
                            st.rerun()
                    else:
                        if st.button(
                            "☑️ 習得した",
                            key=f"complete_{topic['id']}",
                            use_container_width=True,
                            type="primary",
                        ):
                            # チェックを付ける
                            st.session_state.completed_topics.append(topic["id"])
                            # 進捗を保存
                            progress_manager = ProgressManager()
                            progress_manager.save_progress(st.session_state.completed_topics)
                            st.success(f"「{topic['title']}」を習得済みにしました！")
                            st.rerun()

                with col2:
                    if not is_completed:
                        st.caption(
                            "トピックを学習し終えたら「習得した」ボタンを押してください。"
                        )
                    else:
                        st.caption("おめでとうございます！次のトピックに進みましょう。")

        st.divider()

    # 全て完了時のメッセージ
    if progress_data["total_progress"] == 1.0:
        st.balloons()
        st.success(
            """
            🎉 **おめでとうございます！**

            全てのトピックを習得しました！
            これでLangGraphのエキスパートです。

            次のステップ:
            - 実際のプロジェクトでLangGraphを活用してみましょう
            - テンプレートモードで実践的なコードを試してみましょう
            - 構成案生成モードで独自のシステムを設計してみましょう
            """
        )


def render_template_mode():
    """テンプレートモードのUI"""
    st.header("🎨 LangGraphテンプレート")

    st.info(
        """
        ユースケース別のLangGraphテンプレートを即座に参照・利用できます。
        **完全に動作するコード + Mermaid図 + わかりやすい説明**が含まれています。
        """
    )

    # フィルタリングオプション
    col1, col2 = st.columns(2)

    with col1:
        category_filter = st.selectbox(
            "📂 カテゴリで絞り込み:",
            options=["すべて"] + list(TEMPLATE_CATEGORIES.values()),
            key="template_category_filter",
        )

    with col2:
        difficulty_filter = st.selectbox(
            "📊 難易度で絞り込み:",
            options=["すべて", "初級", "中級", "上級"],
            key="template_difficulty_filter",
        )

    st.divider()

    # テンプレート一覧の取得
    templates = TEMPLATES

    # カテゴリフィルタ適用
    if category_filter != "すべて":
        category_key = [k for k, v in TEMPLATE_CATEGORIES.items() if v == category_filter][0]
        templates = get_templates_by_category(category_key)

    # 難易度フィルタ適用
    if difficulty_filter != "すべて":
        templates = [t for t in templates if t["difficulty"] == difficulty_filter]

    # テンプレートカード表示
    if not templates:
        st.warning("条件に一致するテンプレートが見つかりませんでした。")
    else:
        st.subheader(f"📋 テンプレート一覧 ({len(templates)}件)")

        for template in templates:
            with st.expander(f"**{template['title']}** - {template['difficulty']}", expanded=False):
                # ヘッダー情報
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**カテゴリ:** {TEMPLATE_CATEGORIES[template['category']]}")
                with col2:
                    st.markdown(f"**難易度:** {template['difficulty']}")
                with col3:
                    # タグ表示
                    tags_str = " ".join([f"`{tag}`" for tag in template["tags"][:3]])
                    st.markdown(tags_str)

                st.markdown("---")

                # 説明
                st.markdown("### 📝 概要")
                st.markdown(template["description"])

                st.markdown("### 💡 わかりやすい説明")
                st.info(template["explanation"])

                # ユースケース
                st.markdown("### 🎯 活用例")
                for use_case in template["use_cases"]:
                    st.markdown(f"- {use_case}")

                st.markdown("---")

                # タブで表示内容を切り替え
                tab1, tab2, tab3 = st.tabs(["💻 コード", "📊 アーキテクチャ図", "📦 使い方"])

                with tab1:
                    st.markdown("### 完全な実装コード")
                    st.code(template["code"], language="python")

                    # コピーボタン（ヒント）
                    st.caption(
                        "💡 このコードをコピーして、ローカル環境で実行できます。"
                    )

                with tab2:
                    st.markdown("### システムアーキテクチャ図")
                    # Mermaid図を表示
                    st.markdown(f"```mermaid\n{template['mermaid']}\n```")

                with tab3:
                    st.markdown("### このテンプレートの使い方")
                    st.markdown(
                        f"""
                        1. **コードタブ**から完全な実装コードをコピー
                        2. ローカル環境で新しいPythonファイルを作成
                        3. コードを貼り付けて保存
                        4. 必要な依存パッケージをインストール:
                           ```bash
                           pip install langgraph langchain openai
                           ```
                        5. コードを実行:
                           ```bash
                           python your_file.py
                           ```

                        **カスタマイズのヒント:**
                        - 状態（State）の構造を自分のユースケースに合わせて変更
                        - ノード関数の中身を実際のビジネスロジックに置き換え
                        - 条件分岐ロジックを調整
                        """
                    )

                    st.success(
                        f"**{template['title']}**は、{template['difficulty']}レベルのテンプレートです。"
                        f"基本構造を理解してから、自分のプロジェクトに合わせてカスタマイズしてください。"
                    )


def render_architect_mode():
    """構成案生成モードのUI"""
    st.header("🏛️ 構成案生成")

    st.info(
        """
        ビジネス課題を入力すると、LangGraphを活用した構成案を自動生成します。
        **Mermaid図 + コード例 + わかりやすい説明**の形式で出力されます。
        """
    )

    # サンプル課題ボタン
    st.subheader("サンプル課題")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💬 カスタマーサポート自動化", use_container_width=True):
            st.session_state.sample_challenge = (
                "カスタマーサポートの自動化を実現したい。"
                "FAQへの自動回答と、複雑な問い合わせは人間にエスカレーションする仕組みが必要。"
            )

    with col2:
        if st.button("📊 データ分析ワークフロー", use_container_width=True):
            st.session_state.sample_challenge = (
                "営業データの自動分析と、週次レポートの自動生成を実現したい。"
            )

    # ビジネス課題入力
    challenge = st.text_area(
        "ビジネス課題を入力してください:",
        value=st.session_state.get("sample_challenge", ""),
        height=120,
        placeholder="例: 契約書の自動チェックとリスク箇所の抽出を実現したい",
        key="architect_challenge",
    )

    # 業界・制約条件（オプション）
    col1, col2 = st.columns(2)

    with col1:
        industry = st.text_input(
            "業界（オプション）:", placeholder="例: EC、製造業、法務", key="industry"
        )

    with col2:
        constraints = st.text_input(
            "制約条件（カンマ区切り、オプション）:",
            placeholder="例: 日本語対応必須, オンプレミス環境",
            key="constraints",
        )

    # 生成実行ボタン
    if st.button("🚀 構成案を生成", type="primary", use_container_width=True):
        if challenge.strip():
            try:
                # プログレスバー表示
                progress_bar = st.progress(0)
                status_text = st.empty()

                # ステップ1: システム初期化
                status_text.text("🔧 システムを初期化中...")
                progress_bar.progress(10)
                architect_graph = get_architect_graph()

                # 制約条件をリストに変換
                constraints_list = None
                if constraints and constraints.strip():
                    constraints_list = [c.strip() for c in constraints.split(",")]

                # ステップ2: 課題分析
                status_text.text("📊 ビジネス課題を分析中...")
                progress_bar.progress(25)

                # ステップ3: アーキテクチャ設計
                status_text.text("🏗️ システムアーキテクチャを設計中...")
                progress_bar.progress(50)

                # ステップ4: コード生成
                status_text.text("💻 実装コードを生成中...")
                progress_bar.progress(75)

                # 構成案生成
                result = architect_graph.generate_architecture(
                    business_challenge=challenge,
                    industry=industry if industry.strip() else None,
                    constraints=constraints_list,
                )

                # ステップ5: 完了
                status_text.text("✅ 構成案生成完了！")
                progress_bar.progress(100)

                # プログレスバーを削除
                import time
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()

                # セッション状態に結果を保存
                st.session_state.architecture_result = result

                # sample_challengeをクリア
                if "sample_challenge" in st.session_state:
                    st.session_state.sample_challenge = ""

                st.success("✅ 構成案の生成が完了しました！")

            except ValidationError as e:
                st.error(f"バリデーションエラー: {e}")
            except LLMError as e:
                st.error(f"LLMエラー: {e}")
                st.info(
                    "LLMの応答に問題がありました。"
                    "もう一度試すか、課題の記述を変更してみてください。"
                )
            except Exception as e:
                st.error(f"予期しないエラーが発生しました: {e}")
        else:
            st.warning("ビジネス課題を入力してください")

    # 生成結果の表示
    if st.session_state.architecture_result:
        result = st.session_state.architecture_result

        st.divider()

        # 課題分析結果
        st.markdown("## 📊 課題分析結果")
        analysis = result["challenge_analysis"]

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 📝 課題の要約")
            st.info(analysis.get("summary", ""))

        with col2:
            st.markdown("### 🎯 LangGraph適用の妥当性")
            st.success(analysis.get("langgraph_fit_reason", ""))

        st.markdown("### 📋 主要要件")
        requirements = analysis.get("key_requirements", [])
        for req in requirements:
            st.markdown(f"- {req}")

        st.markdown("### 💡 推奨アプローチ")
        st.markdown(analysis.get("suggested_approach", ""))

        st.divider()

        # アーキテクチャ図
        st.markdown("## 🏗️ システムアーキテクチャ")

        # Mermaid図
        st.markdown("### 📊 フローチャート")
        mermaid_diagram = result["architecture"]["mermaid_diagram"]
        if mermaid_diagram:
            st.markdown(f"```mermaid\n{mermaid_diagram}\n```")
        else:
            st.warning("Mermaid図の生成に失敗しました")

        # ノード説明
        with st.expander("🔍 ノードの詳細説明", expanded=False):
            nodes = result["architecture"]["node_descriptions"]
            for node in nodes:
                st.markdown(f"#### {node.get('name', 'Unnamed Node')}")
                st.markdown(f"**目的:** {node.get('purpose', '')}")
                st.markdown(f"**説明:** {node.get('description', '')}")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**入力:**")
                    for inp in node.get("inputs", []):
                        st.markdown(f"- {inp}")
                with col2:
                    st.markdown("**出力:**")
                    for out in node.get("outputs", []):
                        st.markdown(f"- {out}")

                st.divider()

        # 状態スキーマ
        with st.expander("📦 状態スキーマ", expanded=False):
            state_schema = result["architecture"]["state_schema"]
            if state_schema:
                for field, description in state_schema.items():
                    st.markdown(f"- **{field}**: {description}")
            else:
                st.info("状態スキーマ情報がありません")

        st.divider()

        # コード例
        st.markdown("## 💻 実装コード例")
        code_example = result["code_example"]

        if code_example:
            st.markdown(code_example.get("explanation", ""))

            st.code(code_example["code"], language=code_example["language"])

            # コピーボタンのヒント
            st.caption(
                "💡 このコードをコピーして、ローカル環境で実行・カスタマイズできます。"
            )
        else:
            st.warning("コード例の生成に失敗しました")

        st.divider()

        # ビジネス説明
        st.markdown("## 📖 わかりやすい説明（非技術者向け）")
        st.markdown(result["business_explanation"])

        st.divider()

        # 実装ノート
        st.markdown("## 🔧 実装時の注意点")
        implementation_notes = result["implementation_notes"]
        if implementation_notes:
            for note in implementation_notes:
                st.markdown(f"- {note}")
        else:
            st.info("実装ノートがありません")

        st.divider()

        # メタデータ
        st.markdown("## 📊 生成情報")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("使用モデル", result["metadata"]["model"])
        with col2:
            st.metric("生成時間", f"{result['metadata']['response_time']:.2f}秒")

        # ダウンロードボタン
        st.divider()
        st.markdown("## 💾 結果のダウンロード")

        # Markdown形式でダウンロード
        download_content = f"""# LangGraph 構成案

## 課題分析
{analysis.get("summary", "")}

### 主要要件
{chr(10).join(f"- {req}" for req in requirements)}

### 推奨アプローチ
{analysis.get("suggested_approach", "")}

---

## システムアーキテクチャ

### フローチャート
```mermaid
{mermaid_diagram}
```

---

## 実装コード
```python
{code_example["code"] if code_example else ""}
```

---

## わかりやすい説明
{result["business_explanation"]}

---

## 実装時の注意点
{chr(10).join(f"- {note}" for note in implementation_notes) if implementation_notes else ""}

---

生成日時: {result["metadata"].get("generated_at", "")}
使用モデル: {result["metadata"]["model"]}
"""

        st.download_button(
            label="📥 Markdownファイルとしてダウンロード",
            data=download_content,
            file_name="langgraph_architecture.md",
            mime="text/markdown",
            use_container_width=True,
        )


def render_footer():
    """フッターセクションの描画"""
    st.divider()
    st.markdown(
        """
        <div style='
            background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
            border-radius: 0.75rem;
            padding: 2rem;
            margin-top: 3rem;
            border: 1px solid #E2E8F0;
        '>
            <div style='text-align: center;'>
                <h4 style='
                    color: #1E293B;
                    margin: 0 0 1rem 0;
                    font-weight: 700;
                    font-size: 1.25rem;
                '>⚡ LangGraph Catalyst</h4>
                <p style='
                    color: #475569;
                    margin: 0.5rem 0;
                    line-height: 1.75;
                '>
                    Built with <span style='color: #EF4444;'>❤️</span> using
                    <strong style='color: #2563EB;'>LangGraph</strong>,
                    <strong style='color: #2563EB;'>LangChain</strong>, and
                    <strong style='color: #2563EB;'>Streamlit</strong>
                </p>
                <div style='
                    margin-top: 1.5rem;
                    padding-top: 1.5rem;
                    border-top: 2px solid #E2E8F0;
                '>
                    <p style='
                        color: #94A3B8;
                        font-size: 0.875rem;
                        margin: 0;
                    '>
                        © 2026 LangGraph Catalyst | ポートフォリオプロジェクト
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    """メイン処理"""
    # カスタムCSSの注入
    inject_custom_css()

    # セッション状態の初期化
    initialize_session_state()

    # サイドバーの描画
    render_sidebar()

    # ヘッダーの描画
    render_header()

    # モードに応じたUIの描画
    if st.session_state.mode == "RAG学習支援":
        render_rag_mode()
    elif st.session_state.mode == "学習パス":
        render_learning_path_mode()
    elif st.session_state.mode == "テンプレート":
        render_template_mode()
    elif st.session_state.mode == "構成案生成":
        render_architect_mode()
    else:
        st.error("不明なモードが選択されています")

    # フッターの描画
    render_footer()


if __name__ == "__main__":
    main()
