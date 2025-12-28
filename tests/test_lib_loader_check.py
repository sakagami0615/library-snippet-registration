"""checkモジュールのユニットテスト."""

import pytest

from snippet.src.lib_loader.check import check_library_code_block
from snippet.src.lib_loader.check import check_library_code_prefix


def test_check_library_code_block_valid_single_block() -> None:
    """正しい単一ブロックのテスト."""
    lines = [
        "# lib:begin",
        "def foo():",
        "    pass",
        "# lib:end",
    ]

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is True


def test_check_library_code_block_valid_multiple_blocks() -> None:
    """正しい複数ブロックのテスト."""
    lines = [
        "# lib:begin",
        "def foo():",
        "    pass",
        "# lib:end",
        "",
        "# lib:begin",
        "def bar():",
        "    pass",
        "# lib:end",
    ]

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is True


def test_check_library_code_block_nested_blocks() -> None:
    """ネストしたブロック（不正）のテスト."""
    lines = [
        "# lib:begin",
        "# lib:begin",
        "def foo():",
        "    pass",
        "# lib:end",
        "# lib:end",
    ]

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is False


def test_check_library_code_block_end_before_begin() -> None:
    """終了マークが先に出現する（不正）テスト."""
    lines = [
        "# lib:end",
        "# lib:begin",
        "def foo():",
        "    pass",
    ]

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is False


def test_check_library_code_block_missing_end_marker() -> None:
    """終了マークがない（不正）テスト."""
    lines = [
        "# lib:begin",
        "def foo():",
        "    pass",
    ]

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is False


def test_check_library_code_block_missing_begin_marker() -> None:
    """開始マークがない（不正）テスト."""
    lines = [
        "def foo():",
        "    pass",
        "# lib:end",
    ]

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is False


def test_check_library_code_block_empty_lines() -> None:
    """空の行リストのテスト."""
    lines: list[str] = []

    result = check_library_code_block(lines, "lib:begin", "lib:end")

    assert result is True


def test_check_library_code_prefix_all_prefixes_present_once() -> None:
    """すべてのプレフィックスが1回ずつ存在するテスト."""
    lines = [
        "# [snippet_key] my_function",
        "# [snippet_prefix] myfunc",
        "# [description] My function description",
        "def my_function():",
        "    pass",
    ]
    prefix_list = ["[snippet_key]", "[snippet_prefix]", "[description]"]

    result = check_library_code_prefix(lines, prefix_list)

    assert result is True


def test_check_library_code_prefix_missing_prefix() -> None:
    """プレフィックスが欠けているテスト."""
    lines = [
        "# [snippet_key] my_function",
        "# [snippet_prefix] myfunc",
        "def my_function():",
        "    pass",
    ]
    prefix_list = ["[snippet_key]", "[snippet_prefix]", "[description]"]

    result = check_library_code_prefix(lines, prefix_list)

    assert result is False


def test_check_library_code_prefix_duplicate_prefix() -> None:
    """プレフィックスが重複しているテスト."""
    lines = [
        "# [snippet_key] my_function",
        "# [snippet_key] duplicate_key",
        "# [snippet_prefix] myfunc",
        "# [description] My function description",
        "def my_function():",
        "    pass",
    ]
    prefix_list = ["[snippet_key]", "[snippet_prefix]", "[description]"]

    result = check_library_code_prefix(lines, prefix_list)

    assert result is False


def test_check_library_code_prefix_empty_lines() -> None:
    """空の行リストのテスト."""
    lines: list[str] = []
    prefix_list = ["[snippet_key]", "[snippet_prefix]", "[description]"]

    result = check_library_code_prefix(lines, prefix_list)

    assert result is False


def test_check_library_code_prefix_empty_prefix_list() -> None:
    """空のプレフィックスリストのテスト."""
    lines = [
        "def my_function():",
        "    pass",
    ]
    prefix_list: list[str] = []

    result = check_library_code_prefix(lines, prefix_list)

    assert result is True


def test_check_library_code_prefix_in_middle_of_line() -> None:
    """プレフィックスが行の途中にある場合のテスト."""
    lines = [
        "# This is [snippet_key] my_function",
        "# [snippet_prefix] myfunc",
        "# [description] My function description",
        "def my_function():",
        "    pass",
    ]
    prefix_list = ["[snippet_key]", "[snippet_prefix]", "[description]"]

    result = check_library_code_prefix(lines, prefix_list)

    assert result is True
