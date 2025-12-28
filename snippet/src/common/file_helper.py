import json
import re
from logging import getLogger
from pathlib import Path
from typing import Any

import yaml

from snippet.setting import FILE_ENCODING

logger = getLogger("snippet").getChild("file_helper")


def read_text(file_path: Path) -> list[str]:
    """テキストを読み込む。

    Args:
        file_path (Path): テキストファイルパス

    Returns:
        list[str]: 読み込んだテキスト
    """
    with open(file_path, "r", encoding=FILE_ENCODING) as f:
        return [s.rstrip("\n") for s in f.readlines()]


def read_yaml(yaml_path: Path) -> dict[Any, Any]:
    """yamlデータを読み込む

    Args:
        yaml_path (Path): yamlデータファイル

    Returns:
        dict: 読み込んだyamlデータ
    """
    if not yaml_path.exists():
        return {}
    with open(yaml_path, "r", encoding=FILE_ENCODING) as f:
        result: dict[Any, Any] = yaml.safe_load(f)
        return result


def read_json(json_path: Path) -> dict[Any, Any]:
    """jsonファイルを読み込む

    Args:
        json_path (Path): jsonファイルパス

    Returns:
        dict: 読み込んだjsonデータ
    """
    if not json_path.exists():
        return {}
    with open(json_path, "r", encoding=FILE_ENCODING) as f:
        result: dict[Any, Any] = json.load(f)
        return result


def read_jsonc(json_path: Path) -> dict[Any, Any]:
    """jsoncファイルを読み込む

    Args:
        json_path (Path): jsonファイルパス

    Returns:
        dict: 読み込んだjsonデータ
    """
    if not json_path.exists():
        return {}

    with open(json_path, "r", encoding=FILE_ENCODING) as f:
        lines = f.readlines()

    # 先頭行が // で始まるコメント行のみを削除
    lines = [line for line in lines if not line.lstrip().startswith("//")]
    text = "".join(lines)

    # ブロックコメント /* ... */ を削除
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    result: dict[Any, Any] = json.loads(text)
    return result


def write_json(json_path: Path, json_dict: dict) -> None:
    """jsonファイルを書き込む

    Args:
        json_path (Path): 書き込み先のjsonファイル
        json_dict (dict): 書き込む辞書データ
    """
    with open(json_path, "w", encoding=FILE_ENCODING) as f:
        json.dump(json_dict, f, indent=2)
