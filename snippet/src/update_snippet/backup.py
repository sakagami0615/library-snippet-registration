"""スニペットファイルのバックアップを管理するモジュール."""

import shutil
from pathlib import Path

from snippet.setting import WORKSPACE_DIRPATH


def backup_snippet_files(tool_setting: dict, device_setting: dict) -> None:
    """スニペットファイルをバックアップディレクトリにコピーする.

    既存のバックアップディレクトリがあれば削除してから、
    デバイス設定で指定されたスニペットディレクトリ全体をバックアップします。

    Args:
        tool_setting (dict): ツール設定辞書
            - backup_snippet_dirpath: バックアップディレクトリの相対パス
        device_setting (dict): デバイス設定辞書
            - snippet_path: スニペットパスの辞書 {エディタ名: スニペットディレクトリパス}
    """
    backup_dirpath = WORKSPACE_DIRPATH / Path(tool_setting["backup_snippet_dirpath"])

    if backup_dirpath.exists():
        shutil.rmtree(backup_dirpath)

    backup_dirpath.mkdir(parents=True, exist_ok=True)

    for snippet_name, snippet_path in device_setting["snippet_path"].items():
        backup_snippet_path = backup_dirpath / Path(snippet_name)
        shutil.copytree(snippet_path, backup_snippet_path)
