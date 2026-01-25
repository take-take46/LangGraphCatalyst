"""
LangGraph Catalyst - Sidebar Component

サイドバーUIコンポーネント。
モード切り替え、設定パネル、使い方説明を提供します。
"""

import streamlit as st

from src.config.settings import settings


def render_sidebar():
    """サイドバー全体の描画"""
    with st.sidebar:
        # ロゴとタイトル
        st.markdown(
            """
            <div style='text-align: center; padding: 1rem 0;'>
                <h1 style='margin: 0;'>⚡</h1>
                <h3 style='margin: 0.5rem 0 0 0;'>LangGraph Catalyst</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # モード切り替えセクション
        render_mode_selector()

        st.divider()

        # 設定パネル
        render_settings_panel()

        st.divider()

        # 使い方説明
        render_help_section()


def render_mode_selector():
    """モード切り替えセクション"""
    st.subheader("📌 モード選択")

    # モードのインデックスを取得
    modes = ["RAG学習支援", "学習パス", "テンプレート", "構成案生成"]
    current_mode = st.session_state.mode
    index = modes.index(current_mode) if current_mode in modes else 0

    mode = st.radio(
        "利用モードを選択してください:",
        options=modes,
        index=index,
        help="RAG学習支援: LangGraphに関する質問に回答\n学習パス: 初級から上級まで段階的に学習\nテンプレート: ユースケース別テンプレートを参照\n構成案生成: ビジネス課題から構成案を生成",
        key="mode_selector",
    )

    # セッション状態を更新
    st.session_state.mode = mode

    # モードの説明
    if mode == "RAG学習支援":
        st.info(
            """
            **📚 RAG学習支援モード**

            LangGraphの公式ドキュメント、ブログ、GitHubから
            関連情報を検索し、ソース付きで回答します。
            """
        )
    elif mode == "学習パス":
        st.info(
            """
            **📖 学習パスモード**

            初級→中級→上級の構造化されたカリキュラムで
            LangGraphを段階的に習得できます。
            進捗も自動管理されます。
            """
        )
    elif mode == "テンプレート":
        st.info(
            """
            **🎨 テンプレートモード**

            カスタマーサポート、データ分析など、
            ユースケース別のLangGraphテンプレートを
            即座に参照・利用できます。
            """
        )
    else:
        st.info(
            """
            **🏛️ 構成案生成モード**

            ビジネス課題を入力すると、LangGraphを活用した
            システム構成案を自動生成します。
            """
        )


def render_settings_panel():
    """設定パネル"""
    with st.expander("⚙️ 詳細設定", expanded=False):
        st.markdown("##### LLMモデル設定")

        # モデル選択
        model = st.selectbox(
            "モデル:",
            options=[
                "gpt-4-turbo-preview",
                "gpt-4",
                "gpt-3.5-turbo",
            ],
            index=0,
            help="使用するOpenAIモデルを選択",
            key="settings_model",
        )
        st.session_state.llm_model = model

        # 温度パラメータ
        temperature = st.slider(
            "Temperature:",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.llm_temperature,
            step=0.1,
            help="値が高いほど創造的な回答、低いほど一貫性のある回答",
            key="settings_temperature",
        )
        st.session_state.llm_temperature = temperature

        # RAG設定（RAGモードの場合のみ）
        if st.session_state.mode == "RAG学習支援":
            st.markdown("---")
            st.markdown("##### RAG設定")

            top_k = st.slider(
                "検索件数 (Top-K):",
                min_value=1,
                max_value=10,
                value=settings.rag_top_k,
                help="検索する関連ドキュメント数",
                key="settings_top_k",
            )

            st.session_state.rag_top_k = top_k

        # 現在の設定を表示
        st.markdown("---")
        st.markdown("##### 現在の設定")
        st.code(
            f"""
モデル: {st.session_state.llm_model}
Temperature: {st.session_state.llm_temperature}
環境: {settings.environment}
            """.strip()
        )


def render_help_section():
    """使い方説明セクション"""
    with st.expander("❓ 使い方", expanded=False):
        if st.session_state.mode == "RAG学習支援":
            st.markdown(
                """
                ### RAG学習支援モードの使い方

                1. **質問を入力**
                   - LangGraphに関する質問を入力欄に記入
                   - サンプル質問ボタンも利用可能

                2. **検索して回答**
                   - 「検索して回答」ボタンをクリック
                   - 公式ドキュメント、ブログ、GitHubから関連情報を検索

                3. **回答を確認**
                   - ソース付きの詳細な回答を確認
                   - コード例も含まれます
                   - ソースリンクから詳細を確認可能

                **ヒント:**
                - 具体的な質問ほど精度が高い回答が得られます
                - 「〜の実装方法」「〜のコード例」など明確に
                """
            )
        else:
            st.markdown(
                """
                ### 構成案生成モードの使い方

                1. **ビジネス課題を入力**
                   - 解決したい課題を具体的に記述
                   - サンプル課題ボタンも利用可能

                2. **オプション設定（任意）**
                   - 業界: 対象業界を入力
                   - 制約条件: 技術的制約などを入力

                3. **構成案を生成**
                   - 「構成案を生成」ボタンをクリック
                   - LangGraphを活用した構成案を生成

                4. **結果を確認**
                   - Mermaid図: システム構成の可視化
                   - コード例: 実装サンプル
                   - 説明: わかりやすいビジネス視点の解説

                **ヒント:**
                - 課題は具体的に記述してください
                - 制約条件を明記すると実用的な提案になります
                """
            )

    # About セクション
    with st.expander("ℹ️ About", expanded=False):
        st.markdown(
            """
            ### LangGraph Catalyst について

            **LangGraph Catalyst** は、LangGraphの学習支援と
            ビジネス活用を促進する「触媒（Catalyst）」となる
            ポートフォリオシステムです。

            #### 主な機能
            - 📚 **RAG学習支援**: ソース付き学習サポート
            - 🏛️ **構成案生成**: ビジネス課題の解決提案

            #### 技術スタック
            - **LangGraph**: エージェントワークフロー
            - **LangChain**: LLMアプリケーション基盤
            - **Chroma**: ベクトルデータベース
            - **OpenAI**: 言語モデル
            - **Streamlit**: Web UI

            #### リンク
            - [GitHub Repository](https://github.com/your-username/LangGraphCatalyst)
            - [LangGraph Docs](https://langchain-ai.github.io/langgraph/)

            ---
            Built with ❤️ by Your Name
            """
        )
