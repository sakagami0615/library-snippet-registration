import argparse
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path

from snippet.src.file_helper import FileHelper
from snippet.src.snippet_updater import Mode

logger = getLogger("snippet").getChild("snippet_updater")


@dataclass
class Argument:
    """コマンドライン引数の情報格納データクラス

    Attributes:
        mode (Mode): 実行モード(DELETE/RESIST/PREPARE/UNKNOWN)
        is_overwrite (bool): 上書きするかどうか(Trueは上書き)
        backup_path (Path): バックアップフォルダパス
        library_path (Path): ライブラリフォルダパス
        mark_path (Path): ライブラリコード関連のマークを記載した設定ファイル
        snippet_path (Path): スニペットファイルパス
        extensions (list[str]): ライブラリスクリプトの拡張子
        excludes (list[str]): ライブラリスクリプト探索時、無視する文字列
    """

    mode: Mode
    is_overwrite: bool
    backup_path: Path
    library_path: Path
    mark_path: Path
    snippet_path: Path
    extensions: list[str]
    excludes: list[str]

    def is_invalid(self) -> bool:
        """無効なパラメータがないかどうか

        Returns:
            bool: 無効な値があるかどうか(Trueは無効、Falseは有効)
        """

        def is_invalid_mode() -> bool:
            if self.mode == Mode.UNKNOWN:
                logger.info("存在しない mode が設定されています")
                return True
            return False

        def is_invalid_parameter() -> bool:
            # NOTE: Mode.PREPARE の場合は、コマンドライン引数を使用しないためチェック不要
            if self.mode == Mode.PREPARE:
                return False

            invalid = False
            if self.snippet_path == Path(""):
                logger.warning("snippet_path が設定されていません")
                invalid = True
            if not self.extensions:
                logger.warning("extensions が設定されていません")
                invalid = True
            if not self.library_path.exists():
                logger.warning("library_path が存在しません")
                invalid = True
            if not self.mark_path.exists():
                logger.warning("mark_path が存在しません")
                invalid = True
            return invalid

        return is_invalid_mode() or is_invalid_parameter()


class SnippetArgument:
    """コマンドライン引数取得クラス"""

    def __init__(self) -> None:
        self._cmd_args = self._parse_argument()

    def _parse_argument(self) -> argparse.Namespace:
        """コマンドライン引数をパースする

        Returns:
            argparse.Namespace: パースしたコマンドライン引数
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("mode", type=str, help="")
        parser.add_argument("-c", "--config_path", type=str, default="./config.yaml", help="")
        parser.add_argument("-l", "--library_path", type=str, default="./lib", help="")
        parser.add_argument("-m", "--mark_path", type=str, default="./library_mark.yaml", help="")
        parser.add_argument("-s", "--snippet_path", type=str, default="", help="")
        parser.add_argument("-e", "--extensions", nargs="*", type=str, help="")
        parser.add_argument("--excludes", nargs="*", type=str, help="")
        parser.add_argument("--overwrite", type=int, default=1, help="")
        parser.add_argument("--backup_path", type=str, default="./.backup_snippet", help="")
        return parser.parse_args()

    def get_argument(self) -> Argument:
        """コマンドライン引数を取得する

        Raises:
            ValueError: コマンドライン引数に不足がある場合

        Returns:
            Argument: 取得したコマンドライン引数
        """
        mode = self._cmd_args.mode if Mode.is_exist(self._cmd_args.mode) else Mode.UNKNOWN

        def set_param_in_config() -> Argument:
            config = FileHelper.read_yaml(Path(self._cmd_args.config_path))
            config["is_overwrite"] = config["is_overwrite"] if "is_overwrite" in config else 1
            args = Argument(
                mode,
                bool(max(config["is_overwrite"], 0)),
                Path(config["backup_path"]) if "backup_path" in config else Path(self._cmd_args.backup_path),
                Path(config["library_path"]) if "library_path" in config else Path(self._cmd_args.library_path),
                Path(config["mark_path"]) if "mark_path" in config else Path(self._cmd_args.mark_path),
                Path(config["snippet_path"]),
                config["extensions"] if "extensions" in config else [],
                config["excludes"] if "excludes" in config else [],
            )
            return args

        def set_param_in_args() -> Argument:
            args = Argument(
                mode,
                bool(max(0, self._cmd_args.overwrite)),
                Path(self._cmd_args.backup_path),
                Path(self._cmd_args.library_path),
                Path(self._cmd_args.mark_path),
                Path(self._cmd_args.snippet_path),
                self._cmd_args.extensions if self._cmd_args.extensions else [],
                self._cmd_args.excludes if self._cmd_args.excludes else [],
            )
            return args

        args = set_param_in_args() if not Path(self._cmd_args.config_path).exists() else set_param_in_config()

        if args.is_invalid():
            raise ValueError("引数で指定されたパラメータが適切ではありません")

        return args
