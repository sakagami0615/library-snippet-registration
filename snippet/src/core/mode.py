class Mode:
    """ツールの実行モードクラス"""

    REGISTER = "register"
    SETTING = "setting"
    UNKNOWN = "unknown"

    @staticmethod
    def is_exist(mode_name: str) -> bool:
        """存在するモード名かを判定

        Args:
            mode_name (str): 確認するモード名

        Returns:
            bool: 存在する(True) or 存在しない(False)
        """
        modes = [Mode.REGISTER, Mode.SETTING]
        return mode_name in modes
