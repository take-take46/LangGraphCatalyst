"""
LangGraph Catalyst - Styles Module

プロフェッショナルなカスタムCSSスタイルを提供するモジュール。
企業向けポートフォリオとして洗練されたデザインを実現。
"""

import streamlit as st


def inject_custom_css():
    """カスタムCSSをStreamlitアプリに注入"""
    st.markdown(
        """
        <style>
        /* ========== グローバルスタイル ========== */

        /* ルート要素 */
        :root {
            --primary-color: #2563EB;
            --primary-dark: #1E40AF;
            --primary-light: #3B82F6;
            --secondary-color: #64748B;
            --success-color: #10B981;
            --warning-color: #F59E0B;
            --error-color: #EF4444;
            --info-color: #06B6D4;

            --bg-primary: #FFFFFF;
            --bg-secondary: #F8FAFC;
            --bg-tertiary: #F1F5F9;

            --text-primary: #1E293B;
            --text-secondary: #475569;
            --text-tertiary: #94A3B8;

            --border-color: #E2E8F0;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
        }

        /* ========== タイポグラフィ ========== */

        h1 {
            font-weight: 700;
            font-size: 2.5rem;
            line-height: 1.2;
            color: var(--text-primary);
            margin-bottom: 1.5rem;
            letter-spacing: -0.025em;
        }

        h2 {
            font-weight: 700;
            font-size: 2rem;
            line-height: 1.3;
            color: var(--text-primary);
            margin-top: 2rem;
            margin-bottom: 1rem;
            letter-spacing: -0.025em;
        }

        h3 {
            font-weight: 600;
            font-size: 1.5rem;
            line-height: 1.4;
            color: var(--text-primary);
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        h4 {
            font-weight: 600;
            font-size: 1.25rem;
            line-height: 1.5;
            color: var(--text-primary);
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }

        p {
            line-height: 1.75;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }

        /* ========== リンク ========== */

        a {
            color: var(--primary-color);
            text-decoration: none;
            transition: all 0.2s ease-in-out;
            font-weight: 500;
        }

        a:hover {
            color: var(--primary-dark);
            text-decoration: underline;
        }

        /* ========== ボタン ========== */

        .stButton > button {
            border-radius: var(--radius-md);
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            border: none;
            padding: 0.625rem 1.25rem;
            font-size: 0.95rem;
            letter-spacing: 0.01em;
            box-shadow: var(--shadow-sm);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .stButton > button:active {
            transform: translateY(0);
            box-shadow: var(--shadow-sm);
        }

        /* プライマリボタン */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
        }

        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-color) 100%);
        }

        /* セカンダリボタン */
        .stButton > button[kind="secondary"] {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }

        .stButton > button[kind="secondary"]:hover {
            background-color: var(--bg-tertiary);
            border-color: var(--primary-color);
        }

        /* ========== カード ========== */

        .card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease-in-out;
        }

        .card:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-2px);
        }

        .card-header {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--border-color);
        }

        .card-body {
            color: var(--text-secondary);
            line-height: 1.75;
        }

        /* ========== アラート・通知 ========== */

        .stAlert {
            border-radius: var(--radius-md);
            border-left: 4px solid;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
            box-shadow: var(--shadow-sm);
        }

        /* インフォ */
        [data-baseweb="notification"][kind="info"] {
            background-color: #EFF6FF;
            border-left-color: var(--info-color);
        }

        /* 成功 */
        [data-baseweb="notification"][kind="success"] {
            background-color: #F0FDF4;
            border-left-color: var(--success-color);
        }

        /* 警告 */
        [data-baseweb="notification"][kind="warning"] {
            background-color: #FFFBEB;
            border-left-color: var(--warning-color);
        }

        /* エラー */
        [data-baseweb="notification"][kind="error"] {
            background-color: #FEF2F2;
            border-left-color: var(--error-color);
        }

        /* ========== 入力フィールド ========== */

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: var(--radius-md);
            border: 2px solid var(--border-color);
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            transition: all 0.2s ease-in-out;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        /* ========== セレクトボックス ========== */

        .stSelectbox > div > div > div {
            border-radius: var(--radius-md);
            border: 2px solid var(--border-color);
            transition: all 0.2s ease-in-out;
        }

        .stSelectbox > div > div > div:hover {
            border-color: var(--primary-color);
        }

        /* ========== エキスパンダー ========== */

        .streamlit-expanderHeader {
            font-weight: 600;
            border-radius: var(--radius-md);
            background-color: var(--bg-secondary);
            padding: 1rem 1.25rem;
            border: 1px solid var(--border-color);
            transition: all 0.2s ease-in-out;
        }

        .streamlit-expanderHeader:hover {
            background-color: var(--bg-tertiary);
            border-color: var(--primary-color);
        }

        .streamlit-expanderContent {
            border-radius: 0 0 var(--radius-md) var(--radius-md);
            padding: 1.25rem;
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-top: none;
        }

        /* ========== タブ ========== */

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-bottom: none;
            transition: all 0.2s ease-in-out;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: var(--bg-tertiary);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white !important;
            border-color: var(--primary-color);
        }

        /* ========== メトリクス ========== */

        [data-testid="stMetricValue"] {
            font-size: 2.25rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.875rem;
            font-weight: 600;
        }

        /* ========== プログレスバー ========== */

        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            border-radius: var(--radius-sm);
        }

        .stProgress > div > div {
            border-radius: var(--radius-sm);
            background-color: var(--bg-tertiary);
        }

        /* ========== スピナー ========== */

        .stSpinner > div {
            border-top-color: var(--primary-color) !important;
            border-right-color: var(--primary-light) !important;
        }

        /* ========== コードブロック ========== */

        .stCodeBlock {
            border-radius: var(--radius-md);
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
            margin: 1rem 0;
        }

        code {
            background-color: var(--bg-tertiary);
            padding: 0.2rem 0.4rem;
            border-radius: var(--radius-sm);
            font-size: 0.9em;
            color: var(--primary-dark);
            font-weight: 500;
        }

        pre {
            background-color: var(--bg-secondary);
            padding: 1rem;
            border-radius: var(--radius-md);
            overflow-x: auto;
            border: 1px solid var(--border-color);
        }

        /* ========== サイドバー ========== */

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
            border-right: 1px solid var(--border-color);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 2rem;
        }

        /* サイドバーのボタン */
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            justify-content: flex-start;
            text-align: left;
        }

        /* ========== スクロールバー ========== */

        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--secondary-color) 0%, var(--text-tertiary) 100%);
            border-radius: var(--radius-md);
            border: 2px solid var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, var(--text-secondary) 0%, var(--secondary-color) 100%);
        }

        /* ========== ディバイダー ========== */

        hr {
            border: none;
            border-top: 2px solid var(--border-color);
            margin: 2rem 0;
        }

        /* ========== バッジ ========== */

        .badge {
            display: inline-block;
            padding: 0.375rem 0.875rem;
            border-radius: var(--radius-xl);
            font-size: 0.875rem;
            font-weight: 600;
            letter-spacing: 0.025em;
        }

        .badge-primary {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
            color: white;
        }

        .badge-success {
            background-color: var(--success-color);
            color: white;
        }

        .badge-warning {
            background-color: var(--warning-color);
            color: white;
        }

        .badge-info {
            background-color: var(--info-color);
            color: white;
        }

        /* ========== グラデーション背景 ========== */

        .gradient-bg {
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            color: white;
            padding: 2rem;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
        }

        .gradient-bg-blue {
            background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
            color: white;
            padding: 2rem;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
        }

        /* ========== ローディングステート ========== */

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }

        .loading-pulse {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes shimmer {
            0% {
                background-position: -1000px 0;
            }
            100% {
                background-position: 1000px 0;
            }
        }

        .loading-shimmer {
            background: linear-gradient(90deg, #F1F5F9 0%, #E2E8F0 50%, #F1F5F9 100%);
            background-size: 1000px 100%;
            animation: shimmer 2s infinite;
        }

        /* ========== レスポンシブデザイン ========== */

        @media (max-width: 768px) {
            h1 {
                font-size: 2rem;
            }

            h2 {
                font-size: 1.75rem;
            }

            h3 {
                font-size: 1.25rem;
            }

            .card {
                padding: 1.25rem;
                margin: 1rem 0;
            }

            .stButton > button {
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
            }
        }

        @media (max-width: 480px) {
            h1 {
                font-size: 1.75rem;
            }

            h2 {
                font-size: 1.5rem;
            }

            .card {
                padding: 1rem;
            }
        }

        /* ========== アクセシビリティ ========== */

        /* フォーカス表示を改善 */
        *:focus-visible {
            outline: 2px solid var(--primary-color);
            outline-offset: 2px;
            border-radius: var(--radius-sm);
        }

        /* 高コントラストモード対応 */
        @media (prefers-contrast: high) {
            :root {
                --text-primary: #000000;
                --text-secondary: #1E293B;
                --border-color: #475569;
            }
        }

        /* ダークモード対応（将来的な拡張用） */
        @media (prefers-color-scheme: dark) {
            /* ダークモードのスタイルをここに追加 */
        }

        /* ========== アニメーション ========== */

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }

        @keyframes slideIn {
            from {
                transform: translateX(-100%);
            }
            to {
                transform: translateX(0);
            }
        }

        .slide-in {
            animation: slideIn 0.3s ease-in-out;
        }

        /* ========== ユーティリティクラス ========== */

        .text-center {
            text-align: center;
        }

        .text-right {
            text-align: right;
        }

        .mt-1 { margin-top: 0.5rem; }
        .mt-2 { margin-top: 1rem; }
        .mt-3 { margin-top: 1.5rem; }
        .mt-4 { margin-top: 2rem; }

        .mb-1 { margin-bottom: 0.5rem; }
        .mb-2 { margin-bottom: 1rem; }
        .mb-3 { margin-bottom: 1.5rem; }
        .mb-4 { margin-bottom: 2rem; }

        .p-1 { padding: 0.5rem; }
        .p-2 { padding: 1rem; }
        .p-3 { padding: 1.5rem; }
        .p-4 { padding: 2rem; }

        </style>
        """,
        unsafe_allow_html=True,
    )


def create_card(content: str, title: str | None = None, card_type: str = "default") -> str:
    """
    カード風レイアウトのHTMLを生成

    Args:
        content: カード内のコンテンツ
        title: カードのタイトル（オプション）
        card_type: カードのタイプ（default, primary, success, warning, info）

    Returns:
        カードのHTML文字列
    """
    title_html = f"<div class='card-header'>{title}</div>" if title else ""

    card_classes = {
        "default": "card",
        "primary": "card gradient-bg-blue",
        "success": "card",
        "warning": "card",
        "info": "card",
    }

    card_class = card_classes.get(card_type, "card")

    return f"""
    <div class='{card_class} fade-in'>
        {title_html}
        <div class='card-body'>
            {content}
        </div>
    </div>
    """


def create_badge(text: str, badge_type: str = "primary") -> str:
    """
    バッジのHTMLを生成

    Args:
        text: バッジのテキスト
        badge_type: バッジのタイプ（primary, success, warning, info）

    Returns:
        バッジのHTML文字列
    """
    return f"<span class='badge badge-{badge_type}'>{text}</span>"


def create_gradient_header(title: str, subtitle: str | None = None) -> str:
    """
    グラデーション背景のヘッダーを生成

    Args:
        title: ヘッダーのタイトル
        subtitle: サブタイトル（オプション）

    Returns:
        ヘッダーのHTML文字列
    """
    subtitle_html = f"<p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>{subtitle}</p>" if subtitle else ""

    return f"""
    <div class='gradient-bg-blue fade-in' style='margin-bottom: 2rem;'>
        <h2 style='margin: 0; color: white; font-size: 2rem;'>{title}</h2>
        {subtitle_html}
    </div>
    """


def create_loading_skeleton(height: str = "100px") -> str:
    """
    ローディングスケルトンのHTMLを生成

    Args:
        height: スケルトンの高さ

    Returns:
        スケルトンのHTML文字列
    """
    return f"""
    <div class='loading-shimmer' style='
        height: {height};
        border-radius: var(--radius-md);
        margin: 1rem 0;
    '></div>
    """


def create_feature_card(icon: str, title: str, description: str) -> str:
    """
    機能紹介カードのHTMLを生成

    Args:
        icon: アイコン（絵文字）
        title: タイトル
        description: 説明文

    Returns:
        機能カードのHTML文字列
    """
    return f"""
    <div class='card fade-in' style='text-align: center;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>{icon}</div>
        <h3 style='margin: 0.5rem 0; color: var(--text-primary);'>{title}</h3>
        <p style='color: var(--text-secondary); margin: 0.5rem 0 0 0;'>{description}</p>
    </div>
    """


def create_step_indicator(current_step: int, total_steps: int, step_names: list[str]) -> str:
    """
    ステップインジケーターのHTMLを生成

    Args:
        current_step: 現在のステップ（1から開始）
        total_steps: 総ステップ数
        step_names: ステップ名のリスト

    Returns:
        ステップインジケーターのHTML文字列
    """
    steps_html = ""

    for i in range(1, total_steps + 1):
        is_active = i == current_step
        is_completed = i < current_step

        if is_completed:
            step_class = "background: var(--success-color); color: white;"
        elif is_active:
            step_class = "background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%); color: white;"
        else:
            step_class = "background: var(--bg-tertiary); color: var(--text-tertiary);"

        step_name = step_names[i-1] if i-1 < len(step_names) else f"Step {i}"

        steps_html += f"""
        <div style='flex: 1; text-align: center;'>
            <div style='
                {step_class}
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 0.5rem auto;
                font-weight: 700;
                box-shadow: var(--shadow-sm);
            '>{i}</div>
            <div style='font-size: 0.875rem; color: var(--text-secondary);'>{step_name}</div>
        </div>
        """

    return f"""
    <div style='
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin: 2rem 0;
        padding: 1.5rem;
        background-color: var(--bg-secondary);
        border-radius: var(--radius-lg);
    '>
        {steps_html}
    </div>
    """
