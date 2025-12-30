"""file_helperモジュールのユニットテスト."""

import json
import tempfile
from pathlib import Path

import yaml

from snippet.src.common.file_helper import read_json
from snippet.src.common.file_helper import read_jsonc
from snippet.src.common.file_helper import read_text
from snippet.src.common.file_helper import read_yaml
from snippet.src.common.file_helper import write_json


def test_read_text_basic() -> None:
    """基本的なテキストファイル読み込みのテスト."""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as f:
        f.write("line1\n")
        f.write("line2\n")
        f.write("line3\n")
        temp_path = Path(f.name)

    try:
        result = read_text(temp_path)

        assert len(result) == 3
        assert result[0] == "line1"
        assert result[1] == "line2"
        assert result[2] == "line3"
    finally:
        temp_path.unlink()


def test_read_text_empty_file() -> None:
    """空ファイル読み込みのテスト."""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as f:
        temp_path = Path(f.name)

    try:
        result = read_text(temp_path)

        assert len(result) == 0
        assert result == []
    finally:
        temp_path.unlink()


def test_read_text_with_trailing_newline() -> None:
    """末尾改行を含むファイル読み込みのテスト."""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".txt") as f:
        f.write("line1\n")
        f.write("line2\n")
        temp_path = Path(f.name)

    try:
        result = read_text(temp_path)

        assert len(result) == 2
        assert result[0] == "line1"
        assert result[1] == "line2"
    finally:
        temp_path.unlink()


def test_read_yaml_basic() -> None:
    """基本的なYAMLファイル読み込みのテスト."""
    yaml_data = {"key1": "value1", "key2": 123, "key3": ["item1", "item2"]}

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".yml") as f:
        yaml.dump(yaml_data, f)
        temp_path = Path(f.name)

    try:
        result = read_yaml(temp_path)

        assert result["key1"] == "value1"
        assert result["key2"] == 123
        assert result["key3"] == ["item1", "item2"]
    finally:
        temp_path.unlink()


def test_read_yaml_non_existent_file() -> None:
    """存在しないYAMLファイル読み込みのテスト."""
    temp_path = Path("non_existent_file.yml")

    result = read_yaml(temp_path)

    assert result == {}


def test_read_yaml_empty_file() -> None:
    """空のYAMLファイル読み込みのテスト."""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".yml") as f:
        temp_path = Path(f.name)

    try:
        result = read_yaml(temp_path)

        # 空のYAMLファイルはNoneを返すため、Noneになる
        assert result is None
    finally:
        temp_path.unlink()


def test_read_json_basic() -> None:
    """基本的なJSONファイル読み込みのテスト."""
    json_data = {"key1": "value1", "key2": 123, "key3": ["item1", "item2"]}

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".json") as f:
        json.dump(json_data, f)
        temp_path = Path(f.name)

    try:
        result = read_json(temp_path)

        assert result["key1"] == "value1"
        assert result["key2"] == 123
        assert result["key3"] == ["item1", "item2"]
    finally:
        temp_path.unlink()


def test_read_json_non_existent_file() -> None:
    """存在しないJSONファイル読み込みのテスト."""
    temp_path = Path("non_existent_file.json")

    result = read_json(temp_path)

    assert result == {}


def test_read_json_nested_structure() -> None:
    """ネストした構造のJSONファイル読み込みのテスト."""
    json_data = {"parent": {"child1": "value1", "child2": {"grandchild": "value2"}}}

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".json") as f:
        json.dump(json_data, f)
        temp_path = Path(f.name)

    try:
        result = read_json(temp_path)

        assert result["parent"]["child1"] == "value1"
        assert result["parent"]["child2"]["grandchild"] == "value2"
    finally:
        temp_path.unlink()


def test_read_jsonc_with_line_comment() -> None:
    """行コメント付きJSONCファイル読み込みのテスト."""
    jsonc_content = """// This is a comment
{
    "key1": "value1",
    // Another comment
    "key2": 123
}"""

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".jsonc") as f:
        f.write(jsonc_content)
        temp_path = Path(f.name)

    try:
        result = read_jsonc(temp_path)

        assert result["key1"] == "value1"
        assert result["key2"] == 123
    finally:
        temp_path.unlink()


def test_read_jsonc_with_block_comment() -> None:
    """ブロックコメント付きJSONCファイル読み込みのテスト."""
    jsonc_content = """{
    /* This is a
       multi-line comment */
    "key1": "value1",
    "key2": /* inline comment */ 123
}"""

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".jsonc") as f:
        f.write(jsonc_content)
        temp_path = Path(f.name)

    try:
        result = read_jsonc(temp_path)

        assert result["key1"] == "value1"
        assert result["key2"] == 123
    finally:
        temp_path.unlink()


def test_read_jsonc_with_double_slash_in_string() -> None:
    """文字列内の//を含むJSONCファイル読み込みのテスト."""
    jsonc_content = """{
    "url": "https://example.com",
    "expression": "numer // denom"
}"""

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".jsonc") as f:
        f.write(jsonc_content)
        temp_path = Path(f.name)

    try:
        result = read_jsonc(temp_path)

        assert result["url"] == "https://example.com"
        assert result["expression"] == "numer // denom"
    finally:
        temp_path.unlink()


def test_read_jsonc_non_existent_file() -> None:
    """存在しないJSONCファイル読み込みのテスト."""
    temp_path = Path("non_existent_file.jsonc")

    result = read_jsonc(temp_path)

    assert result == {}


def test_read_jsonc_mixed_comments() -> None:
    """複合的なコメントを含むJSONCファイル読み込みのテスト."""
    jsonc_content = """// Line comment at top
{
    /* Block comment before key */
    "key1": "value1",
    // Line comment
    "key2": 123,
    /* Another
       block
       comment */
    "key3": ["item1", "item2"]
}"""

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".jsonc") as f:
        f.write(jsonc_content)
        temp_path = Path(f.name)

    try:
        result = read_jsonc(temp_path)

        assert result["key1"] == "value1"
        assert result["key2"] == 123
        assert result["key3"] == ["item1", "item2"]
    finally:
        temp_path.unlink()


def test_write_json_basic() -> None:
    """基本的なJSON書き込みのテスト."""
    json_data = {"key1": "value1", "key2": 123, "key3": ["item1", "item2"]}

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".json") as f:
        temp_path = Path(f.name)

    try:
        write_json(temp_path, json_data)

        with open(temp_path, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert result["key1"] == "value1"
        assert result["key2"] == 123
        assert result["key3"] == ["item1", "item2"]
    finally:
        temp_path.unlink()


def test_write_json_nested_structure() -> None:
    """ネストした構造のJSON書き込みのテスト."""
    json_data = {"parent": {"child1": "value1", "child2": {"grandchild": "value2"}}}

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".json") as f:
        temp_path = Path(f.name)

    try:
        write_json(temp_path, json_data)

        with open(temp_path, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert result["parent"]["child1"] == "value1"
        assert result["parent"]["child2"]["grandchild"] == "value2"
    finally:
        temp_path.unlink()


def test_write_json_empty_dict() -> None:
    """空の辞書のJSON書き込みのテスト."""
    json_data: dict = {}

    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix=".json") as f:
        temp_path = Path(f.name)

    try:
        write_json(temp_path, json_data)

        with open(temp_path, "r", encoding="utf-8") as f:
            result = json.load(f)

        assert result == {}
    finally:
        temp_path.unlink()
