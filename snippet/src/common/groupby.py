"""リストをキー関数によってグループ化するユーティリティモジュール."""

from collections import defaultdict
from typing import Any
from typing import Callable
from typing import TypeVar

T = TypeVar("T")


def groupby(items: list[T], key_func: Callable[[T], Any]) -> dict[str, list[T]]:
    """リストをキー関数によってグループ化する.

    Args:
        items (list[T]): グループ化対象のリスト
        key_func (Callable[[T], Any]): 各要素からキーを抽出する関数

    Returns:
        dict[str, list[T]]: キーでグループ化された辞書
            キー: key_funcが返す値（文字列に変換）
            値: 同じキーを持つ要素のリスト
    """
    grouped: dict[str, list[T]] = defaultdict(list)
    for item in items:
        key = key_func(item)
        grouped[key].append(item)
    return dict(grouped)
