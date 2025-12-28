"""groupby関数のユニットテスト."""

from dataclasses import dataclass

import pytest

from snippet.src.common.groupby import groupby


@dataclass
class SampleItem:
    """テスト用データクラス."""
    name: str
    category: str
    value: int


def test_groupby_with_string_key() -> None:
    """文字列キーでグループ化するテスト."""
    items = [
        SampleItem("item1", "cat1", 10),
        SampleItem("item2", "cat1", 20),
        SampleItem("item3", "cat2", 30),
    ]

    result = groupby(items, lambda x: x.category)

    assert len(result) == 2
    assert "cat1" in result
    assert "cat2" in result
    assert len(result["cat1"]) == 2
    assert len(result["cat2"]) == 1
    assert result["cat1"][0].name == "item1"
    assert result["cat1"][1].name == "item2"
    assert result["cat2"][0].name == "item3"


def test_groupby_with_empty_list() -> None:
    """空リストでグループ化するテスト."""
    items: list[SampleItem] = []

    result = groupby(items, lambda x: x.category)

    assert len(result) == 0
    assert result == {}


def test_groupby_single_group() -> None:
    """すべて同じグループに属する場合のテスト."""
    items = [
        SampleItem("item1", "cat1", 10),
        SampleItem("item2", "cat1", 20),
        SampleItem("item3", "cat1", 30),
    ]

    result = groupby(items, lambda x: x.category)

    assert len(result) == 1
    assert "cat1" in result
    assert len(result["cat1"]) == 3


def test_groupby_each_item_different_group() -> None:
    """各アイテムが異なるグループに属する場合のテスト."""
    items = [
        SampleItem("item1", "cat1", 10),
        SampleItem("item2", "cat2", 20),
        SampleItem("item3", "cat3", 30),
    ]

    result = groupby(items, lambda x: x.category)

    assert len(result) == 3
    assert all(len(group) == 1 for group in result.values())


def test_groupby_with_numeric_attribute() -> None:
    """数値属性でグループ化するテスト."""
    items = [
        SampleItem("item1", "cat1", 10),
        SampleItem("item2", "cat1", 10),
        SampleItem("item3", "cat2", 20),
    ]

    result = groupby(items, lambda x: x.value)

    assert len(result) == 2
    assert 10 in result
    assert 20 in result
    assert len(result[10]) == 2
    assert len(result[20]) == 1
