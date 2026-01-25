"""
学習進捗管理モジュール

ユーザーの学習進捗をJSONファイルに保存・読み込みします。
"""

import json
import os
from pathlib import Path


class ProgressManager:
    """進捗管理クラス"""

    def __init__(self, data_dir: str = "./data"):
        """
        Args:
            data_dir: データ保存ディレクトリ
        """
        self.data_dir = Path(data_dir)
        self.progress_file = self.data_dir / "learning_progress.json"

        # ディレクトリが存在しない場合は作成
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def load_progress(self) -> list[str]:
        """
        進捗を読み込む

        Returns:
            完了したトピックIDのリスト
        """
        try:
            if self.progress_file.exists():
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("completed_topics", [])
            return []
        except Exception as e:
            print(f"進捗の読み込みに失敗しました: {e}")
            return []

    def save_progress(self, completed_topics: list[str]) -> bool:
        """
        進捗を保存する

        Args:
            completed_topics: 完了したトピックIDのリスト

        Returns:
            成功したかどうか
        """
        try:
            data = {
                "completed_topics": completed_topics,
                "last_updated": self._get_current_timestamp(),
            }

            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"進捗の保存に失敗しました: {e}")
            return False

    def reset_progress(self) -> bool:
        """
        進捗をリセットする

        Returns:
            成功したかどうか
        """
        try:
            if self.progress_file.exists():
                self.progress_file.unlink()
            return True
        except Exception as e:
            print(f"進捗のリセットに失敗しました: {e}")
            return False

    def _get_current_timestamp(self) -> str:
        """現在のタイムスタンプを取得"""
        from datetime import datetime

        return datetime.now().isoformat()
