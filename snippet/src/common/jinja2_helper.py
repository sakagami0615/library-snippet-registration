"""Jinja2テンプレート処理のヘルパー関数を提供するモジュール"""

import os
from logging import getLogger
from pathlib import Path
from typing import Any
from typing import Optional

from jinja2 import Environment
from jinja2 import StrictUndefined

logger = getLogger("snippet").getChild("jinja2_helper")


def create_jinja2_context(base_path: Optional[Path] = None) -> dict[str, Any]:
    """Jinja2テンプレートのコンテキストを作成する

    Args:
        base_path (Optional[Path]): リポジトリ検索の開始パス

    Returns:
        dict[str, Any]: Jinja2テンプレートコンテキスト
    """
    # 循環インポートを避けるため、関数内でインポート
    from snippet.src.common.file_helper import find_repo_root

    repo_root = find_repo_root(base_path)
    repo_root_str = str(repo_root) if repo_root else ""

    return {
        "repo_root": repo_root_str,
        "env": os.environ,
    }


def render_jinja2_template(template_str: str, context: dict[str, Any]) -> str:
    """Jinja2テンプレートをレンダリングする

    Args:
        template_str (str): テンプレート文字列
        context (dict[str, Any]): テンプレートコンテキスト

    Returns:
        str: レンダリング結果
    """
    # テンプレート変数を含まない場合は早期リターン
    if "{{" not in template_str and "{%" not in template_str:
        return template_str

    # Jinja2環境を作成
    env = Environment(
        variable_start_string="{{",
        variable_end_string="}}",
        block_start_string="{%",
        block_end_string="%}",
        undefined=StrictUndefined,
    )

    try:
        template = env.from_string(template_str)
        return template.render(context)
    except Exception as e:
        logger.error(f"Failed to render template: {template_str}. Error: {e}")
        return template_str
