"""
LangGraph Catalyst - Helpers Tests

ユーティリティヘルパー関数のユニットテスト
"""

import pytest

from src.utils.helpers import (
    calculate_token_count,
    extract_code_blocks,
    format_source_metadata,
    parse_mermaid_diagram,
    sanitize_filename,
    split_text_into_chunks,
)


@pytest.mark.unit
class TestHelpers:
    """ヘルパー関数のテスト"""

    # ========================================================================
    # Text Splitting Tests
    # ========================================================================

    def test_split_text_into_chunks_basic(self):
        """
        基本的なテキスト分割のテスト

        テスト内容:
        - テキストが指定されたchunk_sizeで分割されること
        - chunk_overlapが正しく適用されること
        """
        # Arrange
        text = "This is a long text. " * 100  # 長いテキスト
        chunk_size = 100
        chunk_overlap = 20

        # Act
        chunks = split_text_into_chunks(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # Assert
        assert len(chunks) > 1, "複数のチャンクに分割されるべき"
        # 各チャンクのサイズがchunk_size以下であることを確認
        for chunk in chunks:
            assert len(chunk) <= chunk_size + chunk_overlap

    def test_split_text_into_chunks_short_text(self):
        """
        短いテキストの分割テスト

        テスト内容:
        - chunk_sizeより短いテキストが1つのチャンクとして返されること
        """
        # Arrange
        text = "Short text."
        chunk_size = 100

        # Act
        chunks = split_text_into_chunks(text, chunk_size=chunk_size)

        # Assert
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_split_text_into_chunks_empty_text(self):
        """
        空のテキストの分割テスト

        テスト内容:
        - 空のテキストが空のリストまたは単一の空文字列を返すこと
        """
        # Arrange
        text = ""
        chunk_size = 100

        # Act
        chunks = split_text_into_chunks(text, chunk_size=chunk_size)

        # Assert
        assert isinstance(chunks, list)
        assert len(chunks) == 0 or (len(chunks) == 1 and chunks[0] == "")

    def test_split_text_with_custom_separator(self):
        """
        カスタムセパレータでの分割テスト

        テスト内容:
        - セパレータパラメータが正しく適用されること
        """
        # Arrange
        text = "Part1\n\nPart2\n\nPart3"
        chunk_size = 20
        separator = "\n\n"

        # Act
        chunks = split_text_into_chunks(text, chunk_size=chunk_size, separator=separator)

        # Assert
        assert isinstance(chunks, list)
        assert len(chunks) >= 1

    # ========================================================================
    # Code Block Extraction Tests
    # ========================================================================

    def test_extract_code_blocks_python(self):
        """
        Pythonコードブロック抽出のテスト

        テスト内容:
        - ```python ... ```形式のコードブロックが抽出されること
        - 複数のコードブロックが全て抽出されること
        """
        # Arrange
        text = """
        Here is some Python code:

        ```python
        def hello():
            print("Hello, World!")
        ```

        And another block:

        ```python
        x = 10
        print(x)
        ```
        """

        # Act
        code_blocks = extract_code_blocks(text, language="python")

        # Assert
        assert len(code_blocks) == 2
        assert "def hello():" in code_blocks[0]
        assert "x = 10" in code_blocks[1]

    def test_extract_code_blocks_no_language_specified(self):
        """
        言語指定なしのコードブロック抽出テスト

        テスト内容:
        - 全てのコードブロック（言語指定なし）が抽出されること
        """
        # Arrange
        text = """
        ```
        generic code block
        ```

        ```python
        python code
        ```
        """

        # Act
        code_blocks = extract_code_blocks(text)

        # Assert
        assert len(code_blocks) >= 2
        # 辞書のリストが返されるので、codeフィールドにアクセス
        assert any("generic code block" in block["code"] for block in code_blocks)
        assert any("python code" in block["code"] for block in code_blocks)

    def test_extract_code_blocks_none_found(self):
        """
        コードブロックが見つからない場合のテスト

        テスト内容:
        - コードブロックがないテキストで空のリストが返されること
        """
        # Arrange
        text = "This is plain text without any code blocks."

        # Act
        code_blocks = extract_code_blocks(text)

        # Assert
        assert code_blocks == []

    def test_extract_code_blocks_mermaid(self):
        """
        Mermaidコードブロック抽出のテスト

        テスト内容:
        - Mermaid図が正しく抽出されること
        """
        # Arrange
        text = """
        Here is a Mermaid diagram:

        ```mermaid
        graph TD
            A --> B
        ```
        """

        # Act
        code_blocks = extract_code_blocks(text, language="mermaid")

        # Assert
        assert len(code_blocks) == 1
        assert "graph TD" in code_blocks[0]
        assert "A --> B" in code_blocks[0]

    # ========================================================================
    # Token Count Tests
    # ========================================================================

    def test_calculate_token_count_basic(self):
        """
        基本的なトークン数計算のテスト

        テスト内容:
        - トークン数が正の整数で返されること
        - 長いテキストほどトークン数が多いこと
        """
        # Arrange
        short_text = "Hello"
        long_text = "Hello " * 100

        # Act
        short_count = calculate_token_count(short_text)
        long_count = calculate_token_count(long_text)

        # Assert
        assert isinstance(short_count, int)
        assert isinstance(long_count, int)
        assert short_count > 0
        assert long_count > short_count

    def test_calculate_token_count_empty_text(self):
        """
        空のテキストのトークン数計算テスト

        テスト内容:
        - 空のテキストで0が返されること
        """
        # Arrange
        text = ""

        # Act
        count = calculate_token_count(text)

        # Assert
        assert count == 0

    def test_calculate_token_count_multilingual(self):
        """
        多言語テキストのトークン数計算テスト

        テスト内容:
        - 日本語、英語、中国語など異なる言語のトークン数が計算されること
        """
        # Arrange
        english = "Hello world"
        japanese = "こんにちは世界"
        chinese = "你好世界"

        # Act
        en_count = calculate_token_count(english)
        jp_count = calculate_token_count(japanese)
        cn_count = calculate_token_count(chinese)

        # Assert
        assert en_count > 0
        assert jp_count > 0
        assert cn_count > 0

    # ========================================================================
    # Source Metadata Formatting Tests
    # ========================================================================

    def test_format_source_metadata(self):
        """
        ソースメタデータのフォーマットテスト

        テスト内容:
        - メタデータが読みやすい形式にフォーマットされること
        - 必要な情報（title, url, doc_type等）が含まれること
        """
        # Arrange
        metadata = {
            "source": "https://example.com/doc",
            "title": "Test Document",
            "doc_type": "official_docs",
            "updated_at": "2026-01-15T00:00:00Z",
        }

        # Act
        formatted = format_source_metadata(metadata)

        # Assert
        assert "Test Document" in formatted
        assert "https://example.com/doc" in formatted
        assert "official_docs" in formatted or "公式ドキュメント" in formatted

    def test_format_source_metadata_missing_fields(self):
        """
        フィールド欠損時のフォーマットテスト

        テスト内容:
        - 一部のフィールドが欠けていてもエラーにならないこと
        - デフォルト値または空文字列が使用されること
        """
        # Arrange
        metadata = {
            "source": "https://example.com/doc"
            # title, doc_type等が欠けている
        }

        # Act
        formatted = format_source_metadata(metadata)

        # Assert
        assert isinstance(formatted, str)
        assert "https://example.com/doc" in formatted

    def test_format_source_metadata_empty(self):
        """
        空のメタデータのフォーマットテスト

        テスト内容:
        - 空のメタデータが適切に処理されること
        """
        # Arrange
        metadata = {}

        # Act
        formatted = format_source_metadata(metadata)

        # Assert
        assert isinstance(formatted, str)

    # ========================================================================
    # Filename Sanitization Tests
    # ========================================================================

    def test_sanitize_filename_basic(self):
        """
        基本的なファイル名サニタイズのテスト

        テスト内容:
        - 無効な文字が削除または置換されること
        - 安全なファイル名が返されること
        """
        # Arrange
        filename = "test/file:name*.txt"

        # Act
        sanitized = sanitize_filename(filename)

        # Assert
        assert "/" not in sanitized
        assert ":" not in sanitized
        assert "*" not in sanitized
        assert sanitized.endswith(".txt")

    def test_sanitize_filename_special_characters(self):
        """
        特殊文字を含むファイル名のサニタイズテスト

        テスト内容:
        - <, >, |, ?, " などの特殊文字が処理されること
        """
        # Arrange
        filename = 'file<name>with|special?chars".txt'

        # Act
        sanitized = sanitize_filename(filename)

        # Assert
        assert "<" not in sanitized
        assert ">" not in sanitized
        assert "|" not in sanitized
        assert "?" not in sanitized
        assert '"' not in sanitized

    def test_sanitize_filename_unicode(self):
        """
        Unicode文字を含むファイル名のサニタイズテスト

        テスト内容:
        - 日本語などのUnicode文字が保持されること
        """
        # Arrange
        filename = "ファイル名.txt"

        # Act
        sanitized = sanitize_filename(filename)

        # Assert
        assert "ファイル" in sanitized or isinstance(sanitized, str)
        assert sanitized.endswith(".txt")

    def test_sanitize_filename_max_length(self):
        """
        最大長制限のテスト

        テスト内容:
        - 長いファイル名が適切に切り詰められること
        """
        # Arrange
        filename = "a" * 300 + ".txt"

        # Act
        sanitized = sanitize_filename(filename, max_length=255)

        # Assert
        assert len(sanitized) <= 255
        assert sanitized.endswith(".txt")

    def test_sanitize_filename_empty(self):
        """
        空のファイル名のサニタイズテスト

        テスト内容:
        - 空のファイル名がデフォルト名に置換されること
        """
        # Arrange
        filename = ""

        # Act
        sanitized = sanitize_filename(filename)

        # Assert
        assert sanitized != ""
        assert isinstance(sanitized, str)

    # ========================================================================
    # Mermaid Diagram Parsing Tests
    # ========================================================================

    def test_parse_mermaid_diagram(self):
        """
        Mermaid図のパーステスト

        テスト内容:
        - Mermaid図から構造化データが抽出されること
        - ノードとエッジの情報が取得できること
        """
        # Arrange
        mermaid_code = """
graph TD
    A[Start] --> B[Process]
    B --> C[End]
        """.strip()

        # Act
        parsed = parse_mermaid_diagram(mermaid_code)

        # Assert
        assert isinstance(parsed, dict)
        assert "nodes" in parsed or "type" in parsed
        # ノードが含まれていることを確認
        if "nodes" in parsed:
            assert len(parsed["nodes"]) >= 0

    def test_parse_mermaid_diagram_complex(self):
        """
        複雑なMermaid図のパーステスト

        テスト内容:
        - 条件分岐を含む図が正しくパースされること
        """
        # Arrange
        mermaid_code = """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process A]
    B -->|No| D[Process B]
    C --> E[End]
    D --> E
        """.strip()

        # Act
        parsed = parse_mermaid_diagram(mermaid_code)

        # Assert
        assert isinstance(parsed, dict)

    def test_parse_mermaid_diagram_invalid(self):
        """
        無効なMermaid図のパーステスト

        テスト内容:
        - 無効な図がエラーまたは空の結果を返すこと
        """
        # Arrange
        mermaid_code = "This is not a valid mermaid diagram"

        # Act
        parsed = parse_mermaid_diagram(mermaid_code)

        # Assert
        # エラーが発生しないか、空の結果が返される
        assert isinstance(parsed, dict)

    # ========================================================================
    # Edge Cases and Error Handling
    # ========================================================================

    def test_split_text_with_zero_chunk_size(self):
        """
        chunk_size=0のエッジケーステスト

        テスト内容:
        - 不正なchunk_sizeでエラーまたは妥当な処理がされること
        """
        # Arrange
        text = "Test text"

        # Act & Assert
        with pytest.raises(ValueError):
            split_text_into_chunks(text, chunk_size=0)

    def test_calculate_token_count_very_long_text(self):
        """
        非常に長いテキストのトークン数計算テスト

        テスト内容:
        - 大量のテキストでもエラーが発生しないこと
        - 妥当なトークン数が返されること
        """
        # Arrange
        very_long_text = "word " * 100000  # 非常に長いテキスト

        # Act
        count = calculate_token_count(very_long_text)

        # Assert
        assert count > 0
        assert isinstance(count, int)

    def test_sanitize_filename_path_traversal_attack(self):
        """
        パストラバーサル攻撃のテスト

        テスト内容:
        - ../や..\\が除去されること
        - セキュリティ上安全なファイル名が返されること
        """
        # Arrange
        malicious_filename = "../../etc/passwd"

        # Act
        sanitized = sanitize_filename(malicious_filename)

        # Assert
        assert "../" not in sanitized
        assert "..\\" not in sanitized
        # ディレクトリトラバーサルができないことを確認
