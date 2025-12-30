from logging import getLogger

logger = getLogger("snippet").getChild("string_helper")


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
