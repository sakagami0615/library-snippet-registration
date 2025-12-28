from logging import getLogger
from typing import Optional

from snippet.setting import SETTING_PATH
from snippet.src.common.file_helper import read_yaml
from snippet.src.common.string_helper import is_real_number

FIN_INPUT_LIST = set({"exit", "e", "quit", "q"})


logger = getLogger("snippet").getChild("read_setting")


def read_setting_yaml() -> Optional[dict]:
    """設定YAMLファイルを読み込む

    SETTING_PATHで指定された設定ファイルを読み込み、設定データを返す。
    エラーが発生した場合はNoneを返す。

    Returns:
        Optional[dict]: 読み込んだ設定データ。エラーが発生した場合はNone
    """
    logger.info(f"setting path: {SETTING_PATH}")
    try:
        setting_data = read_yaml(SETTING_PATH)
        return setting_data
    except Exception:
        return None


def select_device_interactive(setting_data: dict) -> Optional[str]:
    """ターミナルでデバイスを選択する

    Args:
        setting_data (dict): 設定データ

    Returns:
        Optional[str]: 選択されたデバイス名
    """
    device_list: list[str] = list(setting_data.get("devices", {}))

    if not device_list:
        logger.error("`setting.yml` file does not describe the device settings")
        return None

    if len(device_list) == 1:
        device_name = device_list[0]
        return device_name

    messages = ["choose device"]
    for idx, device_name in enumerate(device_list, start=1):
        messages += [f"{idx}. {device_name}"]
    messages += ["other. exit(e) or quit(q)"]
    logger.info("\n".join(messages))

    while True:
        try:
            user_input = input(">>> ").strip()
            if not user_input:
                logger.warning("Input is empty, please input again")
                continue

            if user_input.lower() in FIN_INPUT_LIST:
                return None

            if is_real_number(user_input):
                choice = int(user_input)
                if 1 <= choice <= len(device_list):
                    selected_device = device_list[choice - 1]
                    return selected_device

            logger.warning(f"Please enter a value in the range of 1 to {len(device_list)}.")

        except KeyboardInterrupt:
            return None
