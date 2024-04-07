from logging import DEBUG
from logging import Formatter
from logging import StreamHandler
from logging import getLogger

from snippet.src.library_loader import LibraryLoader
from snippet.src.snippet_argument import Argument
from snippet.src.snippet_argument import SnippetArgument
from snippet.src.snippet_updater import Mode
from snippet.src.snippet_updater import SnippetUpdater

logger = getLogger("snippet")
handler = StreamHandler()

logger.setLevel(DEBUG)
handler.setLevel(DEBUG)
formatter = Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def delete_snippet(args: Argument) -> None:
    """スニペットの削除処理

    Args:
        args (Argument): コマンドライン引数
    """
    updater = SnippetUpdater(args.is_overwrite, args.backup_path)
    updater.delete_snippet(args.snippet_path)


def resist_snippet(args: Argument) -> None:
    """スニペットへの登録処理

    Args:
        args (Argument): コマンドライン引数
    """
    updater = SnippetUpdater(args.is_overwrite, args.backup_path)
    loader = LibraryLoader(args.mark_path, args.library_path, args.extensions, args.excludes)

    code_infos = loader.read_lib_codes()
    updater.resist_snippet(args.snippet_path, code_infos)


def prepare_config_file(args: Argument) -> None:
    """コンフィグファイル用意(生成)処理

    Args:
        args (Argument): コマンドライン引数
    """
    updater = SnippetUpdater()
    updater.prepare_config_file()


def main() -> None:
    """メイン処理"""
    args = SnippetArgument().get_argument()

    match args.mode:
        case Mode.DELETE:
            # delete_snippet(args)
            pass
        case Mode.RESIST:
            # resist_snippet(args)
            pass
        case Mode.PREPARE:
            prepare_config_file(args)
