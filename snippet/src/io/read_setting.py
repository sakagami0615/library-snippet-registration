from logging import getLogger
from typing import Any
from typing import Optional
from typing import cast

from snippet.setting import SETTING_PATH
from snippet.src.common.file_helper import expand_yaml_templates
from snippet.src.common.file_helper import read_yaml
from snippet.src.common.string_helper import is_real_number

FIN_INPUT_LIST = set({"exit", "e", "quit", "q"})


logger = getLogger("snippet").getChild("read_setting")


def read_setting_yaml() -> Optional[dict]:
    """設定YAMLファイルを読み込み、Jinja2テンプレートを展開する

    SETTING_PATHで指定された設定ファイルを読み込み、全ての文字列値に対して
    Jinja2テンプレート展開を適用した設定データを返す。
    エラーが発生した場合はNoneを返す。

    Returns:
        Optional[dict]: テンプレートが展開された設定データ。エラーが発生した場合はNone

    Note:
        - 設定ファイル内の全ての文字列に対してJinja2テンプレートレンダリングが適用されます
        - 使用可能な変数: repo_root, env.VARIABLE_NAME
    """
    logger.info(f"setting path: {SETTING_PATH}")
    try:
        setting_data = read_yaml(SETTING_PATH)
        # YAML全体に対してJinja2テンプレート展開を適用
        expanded_data = expand_yaml_templates(setting_data)
        return cast(dict[Any, Any], expanded_data)
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
