import argparse
from dataclasses import dataclass
from logging import getLogger

from snippet.src.core.mode import Mode

logger = getLogger("snippet").getChild("argument")


@dataclass
class Argument:
    """コマンドライン引数の情報格納データクラス

    Attributes:
        mode (str): 実行モード(REGISTER/PREPARE/UNKNOWN)
    """

    mode: str


def get_argument() -> Argument:
    """コマンドライン引数を取得する

    Returns:
        Argument: 取得したコマンドライン引数
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, nargs="?", default=Mode.UNKNOWN, help="")
    parse_args = parser.parse_args()

    mode_value: str = parse_args.mode
    resolved_mode: str = mode_value if Mode.is_exist(mode_value) else Mode.UNKNOWN
    return Argument(mode=resolved_mode)
