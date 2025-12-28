from logging import getLogger

logger = getLogger("snippet").getChild("string_helper")


class StringHelper:
    """文字列処理をまとめたクラス"""

    @staticmethod
    def is_include_targets(src: str, targets: list[str]) -> bool:
        """入力文字列にターゲット文字が含まれるかを判定する

        Args:
            src (str): 入力文字列
            targets (list[str]): ターゲット文字列群

        Returns:
            bool: 含まれるかどうか
        """
        for target in targets:
            if target in src:
                return True
        return False

    @staticmethod
    def get_suffix(src: str, label: str) -> str:
        """入力文字列内のラベル文字より後ろの文字を取得する

        Args:
            src (str): 入力文字列
            label (str): ラベル文字

        Returns:
            str: 取得した文字列
        """
        if label not in src:
            logger.warning(f"{src} 内に {label} のラベルがありません")
            return ""
        return src[src.find(label) + len(label) :].lstrip()


def is_real_number(value: str) -> bool:
    """文字列が整数に変換可能かどうかを判定する.

    Args:
        value (str): 判定対象の文字列

    Returns:
        bool: 整数に変換可能な場合True、それ以外False
    """
    try:
        int(value)
        return True

    except ValueError:
        return False
