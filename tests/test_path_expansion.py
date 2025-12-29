"""パス展開機能のユニットテスト"""

from pathlib import Path

import pytest

from snippet.src.common.file_helper import expand_yaml_templates
from snippet.src.common.file_helper import find_repo_root


def test_find_repo_root_from_cwd() -> None:
    """カレントディレクトリからリポジトリルートを検出できることを確認"""
    repo_root = find_repo_root()
    assert repo_root is not None
    assert (repo_root / ".git").exists()


def test_find_repo_root_from_specific_path() -> None:
    """指定したパスからリポジトリルートを検出できることを確認"""
    # testsディレクトリから検索しても、リポジトリルートが見つかることを確認
    test_dir = Path(__file__).parent
    repo_root = find_repo_root(test_dir)
    assert repo_root is not None
    assert (repo_root / ".git").exists()


def test_expand_yaml_templates_with_dict() -> None:
    """辞書データ内のテンプレートが正しく展開されることを確認"""
    test_data = {
        "path": "{{ repo_root }}/tests",
        "count": 42,
        "enabled": True,
    }
    expanded = expand_yaml_templates(test_data)

    # テンプレートが展開されていることを確認
    assert "{{ repo_root }}" not in expanded["path"]
    assert expanded["path"].endswith("/tests")
    # 数値とブール値はそのまま
    assert expanded["count"] == 42
    assert expanded["enabled"] is True


def test_expand_yaml_templates_with_nested_dict() -> None:
    """ネストされた辞書内のテンプレートが正しく展開されることを確認"""
    test_data = {
        "library": {
            "path": "{{ repo_root }}/lib",
            "config": {
                "home": "{{ env.HOME }}",
                "enabled": True,
            },
        }
    }
    expanded = expand_yaml_templates(test_data)

    # ネストされたテンプレートが展開されていることを確認
    assert "{{ repo_root }}" not in expanded["library"]["path"]
    assert "{{ env.HOME }}" not in expanded["library"]["config"]["home"]
    assert expanded["library"]["config"]["enabled"] is True


def test_expand_yaml_templates_with_list() -> None:
    """リスト内のテンプレートが正しく展開されることを確認"""
    import os

    test_data = {
        "paths": [
            "{{ repo_root }}/lib1",
            "{{ repo_root }}/lib2",
            "{{ env.HOME }}/lib3",
        ]
    }
    expanded = expand_yaml_templates(test_data)

    # リスト内の全てのテンプレートが展開されていることを確認
    assert len(expanded["paths"]) == 3
    assert all("{{" not in path for path in expanded["paths"])
    assert expanded["paths"][0].endswith("/lib1")
    assert expanded["paths"][1].endswith("/lib2")
    assert os.environ["HOME"] in expanded["paths"][2]


def test_expand_yaml_templates_with_complex_structure() -> None:
    """複雑な構造のYAMLデータが正しく展開されることを確認"""
    test_data = {
        "libraries": {
            "lib1": {
                "path": "{{ repo_root }}/lib1",
                "extensions": [".py", ".pyx"],
                "excludes": ["__pycache__"],
            },
            "lib2": {
                "path": "{{ env.HOME }}/lib2",
                "enabled": True,
            },
        },
        "count": 2,
    }
    expanded = expand_yaml_templates(test_data)

    # 全てのテンプレートが展開されていることを確認
    assert "{{ repo_root }}" not in expanded["libraries"]["lib1"]["path"]
    assert "{{ env.HOME }}" not in expanded["libraries"]["lib2"]["path"]
    # リストと他の型が保持されていることを確認
    assert expanded["libraries"]["lib1"]["extensions"] == [".py", ".pyx"]
    assert expanded["libraries"]["lib1"]["excludes"] == ["__pycache__"]
    assert expanded["libraries"]["lib2"]["enabled"] is True
    assert expanded["count"] == 2
