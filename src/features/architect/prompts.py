"""
LangGraph Catalyst - Architect Prompts

構成案生成機能で使用するプロンプトテンプレートを定義します。
"""

# ビジネス課題分析用プロンプト
CHALLENGE_ANALYSIS_PROMPT = """あなたはビジネス課題を分析し、AI/LLMソリューションの適用可能性を評価するエキスパートです。

# ビジネス課題
{business_challenge}

{industry_context}

{constraints_context}

# 分析タスク
以下の観点から課題を分析してください:

1. **課題の要約**: 課題を1-2文で簡潔にまとめる
2. **主要要件**: この課題を解決するために必要な機能・要件をリストアップ
3. **LangGraph適用の妥当性**: LangGraphが適したソリューションである理由
4. **推奨アプローチ**: どのようなワークフローが適しているか

# 出力形式
以下のJSON形式で出力してください:
```json
{{
    "summary": "課題の要約",
    "key_requirements": ["要件1", "要件2", "要件3"],
    "langgraph_fit_reason": "LangGraphが適している理由",
    "suggested_approach": "推奨するアプローチの説明"
}}
```
"""

# LangGraph構成案生成プロンプト
ARCHITECTURE_GENERATION_PROMPT = """あなたはLangGraphアーキテクトです。ビジネス課題を解決するLangGraph構成案を設計してください。

# 課題分析結果
{challenge_analysis}

# ビジネス課題
{business_challenge}

{constraints_context}

# 設計タスク
以下の観点からLangGraph構成案を設計してください:

1. **必要なノード**: 各ノードの役割と処理内容
2. **ノード間の遷移**: どのノードからどのノードへ遷移するか
3. **条件分岐**: どのような条件で分岐するか
4. **状態管理**: どのような状態を管理するか

# LangGraph設計の原則
- StateGraphを使用した状態管理
- 明確な責務を持つノード設計
- 適切な条件分岐によるフロー制御
- エラーハンドリングとフォールバック

# 出力形式
以下のJSON形式で出力してください:
```json
{{
    "nodes": [
        {{
            "node_id": "ノードID",
            "name": "ノード名",
            "purpose": "ノードの目的",
            "inputs": ["入力1", "入力2"],
            "outputs": ["出力1", "出力2"],
            "description": "詳細な説明"
        }}
    ],
    "edges": [
        {{
            "from_node": "開始ノードID",
            "to_node": "終了ノードID",
            "condition": "条件（条件分岐の場合のみ）",
            "description": "エッジの説明"
        }}
    ],
    "state_schema": {{
        "field1": "型と説明",
        "field2": "型と説明"
    }}
}}
```
"""

# Mermaid図生成プロンプト
MERMAID_GENERATION_PROMPT = """あなたはMermaid記法のエキスパートです。LangGraph構成案をMermaidフローチャートとして可視化してください。

# LangGraph構成案
{architecture}

# Mermaid生成タスク
以下の要件を満たすMermaidフローチャートを生成してください:

1. **flowchart TD形式**: 上から下へのフローチャート
2. **ノード表現**: 各ノードを適切な形状で表現
   - 開始/終了: 丸角四角形 `[START]`, `[END]`
   - 処理ノード: 四角形 `[ノード名]`
   - 判定ノード: ひし形 `{{判定}}`
3. **エッジ表現**: ノード間の遷移を矢印で表現
   - 通常遷移: `-->`
   - 条件分岐: `-->|条件|`
4. **日本語ラベル**: 分かりやすい日本語でラベル付け

# 出力形式
Mermaid記法のコードブロックのみを出力してください（説明文は不要）:

```mermaid
flowchart TD
    START([開始])
    A[ノード名]
    ...
    END([終了])
```
"""

# コード例生成プロンプト
CODE_GENERATION_PROMPT = """あなたはLangGraphの実装エキスパートです。ビジネス課題を解決するLangGraphコード例を生成してください。

# 課題分析
{challenge_analysis}

# LangGraph構成案
{architecture}

# コード生成タスク
以下の要件を満たすPythonコードを生成してください:

1. **完全で実行可能**: そのまま実行できる完全なコード
2. **型ヒント**: TypedDictやPydanticを使用した型安全な実装
3. **コメント**: 各ノードと重要な処理にコメント
4. **エラーハンドリング**: 適切な例外処理
5. **ベストプラクティス**: LangGraphの推奨パターンに従う

# コード構造
```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import operator

# 状態定義
class State(TypedDict):
    # 状態フィールド
    pass

# ノード関数
def node_function(state: State) -> State:
    # 処理
    return {{"field": "value"}}

# グラフ構築
builder = StateGraph(State)
builder.add_node("node_name", node_function)
builder.add_edge(START, "node_name")
builder.add_edge("node_name", END)
graph = builder.compile()

# 実行例
result = graph.invoke({{"input": "value"}})
```

# 出力形式
Pythonコードブロックと、その説明を出力してください:

## コード例

```python
# コード
```

## コードの説明
- 主要な処理の説明
- 注意点やカスタマイズ方法
"""

# わかりやすい説明生成プロンプト
BUSINESS_EXPLANATION_PROMPT = """あなたはテクニカルライターです。LangGraph構成案を非技術者にも分かりやすく説明してください。

# ビジネス課題
{business_challenge}

# 課題分析
{challenge_analysis}

# LangGraph構成案
{architecture}

# 説明タスク
以下の観点から、非技術者（ビジネス担当者、経営層）にも理解できる説明を作成してください:

1. **システムの全体像**: どのような処理フローか（技術用語を避けて）
2. **主要な機能**: 各ステップで何をするか
3. **ビジネス価値**: このシステムがもたらす価値・効果
4. **導入のメリット**: 従来の方法と比較した利点
5. **想定される効果**: 期待される改善や効率化

# 説明のガイドライン
- 技術用語は最小限に、使用する場合は説明を添える
- 具体的な例や比喩を使って分かりやすく
- ビジネス価値を明確に示す
- 箇条書きを活用して読みやすく

# 出力形式
以下の構造で説明を作成してください:

## システムの概要
（1-2段落で全体像を説明）

## 処理の流れ
1. ステップ1: 説明
2. ステップ2: 説明
...

## 期待される効果
- 効果1: 説明
- 効果2: 説明
...

## 導入時の注意点
- 注意点1
- 注意点2
...
"""

# 実装ノート生成プロンプト
IMPLEMENTATION_NOTES_PROMPT = """あなたは経験豊富なLangGraph開発者です。この構成案を実装する際の注意点とベストプラクティスを提供してください。

# LangGraph構成案
{architecture}

{constraints_context}

# タスク
以下の観点から実装ノートを作成してください:

1. **技術的な注意点**: 実装時に気をつけるべき技術的なポイント
2. **必要な依存関係**: 追加で必要なライブラリやサービス
3. **設定・環境変数**: 必要な設定項目
4. **テスト方法**: 動作確認の方法
5. **拡張性**: 将来の機能追加に向けた考慮点

# 出力形式
箇条書きのリストで出力してください（各項目は1-2文で簡潔に）:

- 実装ノート1
- 実装ノート2
...
"""


def format_industry_context(industry: str | None) -> str:
    """業界コンテキストをフォーマット"""
    if industry:
        return f"\n# 業界\n{industry}\n"
    return ""


def format_constraints_context(constraints: list[str] | None) -> str:
    """制約条件をフォーマット"""
    if constraints and len(constraints) > 0:
        constraints_list = "\n".join(f"- {c}" for c in constraints)
        return f"\n# 制約条件\n{constraints_list}\n"
    return ""
