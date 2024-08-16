import os
import shutil
from collections import defaultdict
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Union

from snippet.setting import SNIPPET_KEY_BODY
from snippet.setting import SNIPPET_KEY_DESC
from snippet.setting import SNIPPET_KEY_PREFIX
from snippet.src.file_helper import FileHelper
from snippet.src.library_loader import CodeInfo
from snippet.src.snippet_diff import SnippetDiff

logger = getLogger("snippet").getChild("snippet_updater")


REPO_PATH = Path(os.path.abspath(__file__)).parent.parent.parent
CONFIG_TEMPLATE_PATH = REPO_PATH.joinpath(Path("snippet/config_template"))


class Mode:
    """ツールの実行モードクラス"""

    DELETE = "delete"
    RESIST = "resist"
    PREPARE = "prepare"
    UNKNOWN = "unknown"

    @staticmethod
    def is_exist(mode_name: str) -> bool:
        """存在するモード名かを判定

        Args:
            mode_name (str): 確認するモード名

        Returns:
            bool: 存在する(True) or 存在しない(False)
        """
        modes = [Mode.DELETE, Mode.RESIST, Mode.PREPARE]
        return mode_name in modes


class SnippetUpdater:
    """スニペット更新処理

    Args:
        is_overwrite (bool): 上書き(True) or 置き換え(False)
        backup_folder_path (str, optional): 変更前のスニペットファイルのバックアップ先 (Defaults to "")
    """

    def __init__(self, is_overwrite: bool = True, backup_folder_path: Path = Path()) -> None:
        self._is_overwrite = is_overwrite
        self._backup_folder_path = backup_folder_path

    def _is_invalid_backup_path(self) -> bool:
        """無効なバックアップフォルダパスかを判定する

        バックアップフォルダが未指定の場合、無効と判定する。

        Returns:
            bool: 無効かどうか(無効はTrue)
        """
        return self._backup_folder_path == Path()

    def _prepare_base_snippet_dict(self, snippet_path: Path) -> dict:
        """ベースとなるスニペット情報を用意する

        Args:
            snippet_path (Path): スニペットパス

        Returns:
            dict: ベースとなるスニペット情報
        """
        if self._is_overwrite:
            logger.info("resist mode: overwrite")
            return FileHelper.read_json(snippet_path)
        else:
            logger.info("resist mode: new")
            return defaultdict(dict)

    def _backup_snippet(self, snippet_path: Path) -> Union[Path, None]:
        """スニペットをバックアップする

        時刻の文字をつけたファイル名でバックアップする。

        Args:
            snippet_path (Path): バックアップ対象のスニペットパス

        Returns:
            Union[str, None]: バックアップしたスニペットパス(バックアップしなかった場合はNone)
        """
        if self._is_invalid_backup_path():
            return None
        backup_snippet_dict = FileHelper.read_json(snippet_path)
        if not backup_snippet_dict:
            return None
        cur_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_snippet_path = os.path.join(
            self._backup_folder_path,
            f"{snippet_path.stem}_{cur_datetime}{snippet_path.suffix}",
        )
        os.makedirs(self._backup_folder_path, exist_ok=True)
        FileHelper.write_json(Path(backup_snippet_path), backup_snippet_dict)
        logger.info(f"create backup snippet ({backup_snippet_path})")
        return Path(backup_snippet_path)

    def delete_snippet(self, snippet_path: Path) -> None:
        """スニペットファイルを削除する

        Args:
            snippet_path (Path): 削除するスニペットパス
        """
        if snippet_path.exists():
            self._backup_snippet(snippet_path)
            snippet_path.unlink(missing_ok=False)
            logger.info(f"delete snippet ({snippet_path})")
        else:
            logger.warning(f"failed to delete snippet ({snippet_path} is not exist)")

    def resist_snippet(self, snippet_path: Path, code_infos: list[CodeInfo]) -> dict:
        """ライブラリコード情報をスニペットに登録する

        Args:
            snippet_path (Path): 登録先のスニペットパス
            code_infos (list[CodeInfo]): ライブラリコード情報

        Returns:
            dict: 登録したスニペット辞書
        """
        last_snippet_dict = self._prepare_base_snippet_dict(snippet_path)
        snippet_dict = last_snippet_dict.copy()
        for code_info in code_infos:
            update_snippet_item = {
                SNIPPET_KEY_PREFIX: code_info.snippet_prefix,
                SNIPPET_KEY_DESC: code_info.description,
                SNIPPET_KEY_BODY: code_info.code,
            }
            snippet_dict[code_info.snippet_key] = update_snippet_item

        SnippetDiff.logger_snippet_diff(last_snippet_dict, snippet_dict)
        self._backup_snippet(snippet_path)
        FileHelper.write_json(snippet_path, snippet_dict)
        return snippet_dict

    def prepare_config_file(self) -> Path:
        """カレントパスにコンフィグファイルを用意(生成)する

        Returns:
            Path: 生成したコンフィグパス
        """
        folder_name = CONFIG_TEMPLATE_PATH.name
        cur_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        gen_template_path = Path(os.getcwd()).joinpath(Path(f"{folder_name}_{cur_datetime}"))

        shutil.copytree(CONFIG_TEMPLATE_PATH, gen_template_path)
        logger.info(f"prepare config template (path: {gen_template_path})")
        return gen_template_path
