import json
import re
from logging import getLogger
from pathlib import Path
from typing import Any
from typing import Optional

import yaml

from snippet.setting import FILE_ENCODING
from snippet.src.common.jinja2_helper import create_jinja2_context
from snippet.src.common.jinja2_helper import render_jinja2_template

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


def find_repo_root(start_path: Optional[Path] = None) -> Optional[Path]:
    """リポジトリのルートディレクトリを検出する

    カレントディレクトリまたは指定されたパスから親ディレクトリを遡り、
    .gitディレクトリが存在する最初のディレクトリをリポジトリルートとして返す。

    Args:
        start_path (Optional[Path]): 検索開始パス。Noneの場合はカレントディレクトリから開始

    Returns:
        Optional[Path]: リポジトリルートのパス。見つからない場合はNone

    Note:
        - .gitディレクトリの存在をリポジトリの判定基準とする
        - ファイルシステムのルートまで遡っても見つからない場合はNoneを返す
    """
    current_path = start_path if start_path else Path.cwd()
    current_path = current_path.resolve()

    while True:
        if (current_path / ".git").exists():
            return current_path

        parent = current_path.parent
        if parent == current_path:
            # ファイルシステムのルートに到達
            return None
        current_path = parent


def expand_yaml_templates(data: Any, base_path: Optional[Path] = None) -> Any:
    """YAML データ内の全ての文字列に対してJinja2テンプレート展開を行う

    辞書、リスト、文字列を再帰的に処理し、全ての文字列値に対して
    Jinja2テンプレートレンダリングを適用します。

    Args:
        data (Any): 展開対象のデータ（辞書、リスト、文字列など）
        base_path (Optional[Path]): リポジトリ検索の開始パス

    Returns:
        Any: テンプレートが展開されたデータ

    Note:
        - 辞書のキーは展開されません（値のみ展開）
        - 文字列以外の型（int, bool等）はそのまま返されます

    Examples:
        >>> data = {"path": "{{ repo_root }}/lib", "count": 42}
        >>> expand_yaml_templates(data)
        {"path": "/path/to/repo/lib", "count": 42}
    """
    context = create_jinja2_context(base_path)

    def _expand_recursive(obj: Any) -> Any:
        """再帰的にテンプレート展開を行う内部関数"""
        if isinstance(obj, dict):
            # 辞書の場合、各値を再帰的に展開
            return {key: _expand_recursive(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            # リストの場合、各要素を再帰的に展開
            return [_expand_recursive(item) for item in obj]
        elif isinstance(obj, str):
            # 文字列の場合、テンプレートをレンダリング
            return render_jinja2_template(obj, context)
        else:
            # その他の型（int, bool, None等）はそのまま返す
            return obj

    return _expand_recursive(data)
