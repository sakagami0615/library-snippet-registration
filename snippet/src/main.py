import shutil
from logging import DEBUG
from logging import Formatter
from logging import StreamHandler
from logging import getLogger

from snippet.setting import SETTING_PATH
from snippet.setting import TEMPLATE_SETTING_PATH
from snippet.setting import WORKSPACE_DIRPATH
from snippet.src.core.argument import get_argument
from snippet.src.core.mode import Mode
from snippet.src.io import read_setting
from snippet.src.lib_loader.load import load_library
from snippet.src.update_snippet.backup import backup_snippet_files
from snippet.src.update_snippet.update import update_snippet

logger = getLogger("snippet")
handler = StreamHandler()
logger.setLevel(DEBUG)
handler.setLevel(DEBUG)
formatter = Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def resist_snippet() -> None:
    """スニペットへの登録処理"""
    setting_data = read_setting.read_setting_yaml()
    if not setting_data:
        logger.error("設定ファイルの読み込みに失敗しました。設定ファイルの内容を確認してください。")
        return

    device_name = read_setting.select_device_interactive(setting_data)
    if not device_name:
        logger.error("デバイスの選択に失敗しました。設定ファイルのdevices項目を確認してください。")
        return

    logger.info(f"choose device: {device_name}")

    tool_setting = setting_data["tool_config"]
    device_setting = setting_data["devices"][device_name]
    library_settings = setting_data.get("libraries", [])

    lib_codes = load_library(library_settings)

    backup_snippet_files(tool_setting, device_setting)
    update_snippet(device_setting, lib_codes)


def prepare_setting_file() -> None:
    """カレントパスに設定ファイルを用意(コピー)する"""
    if not SETTING_PATH.exists():
        WORKSPACE_DIRPATH.mkdir(exist_ok=True)
        shutil.copy2(TEMPLATE_SETTING_PATH, SETTING_PATH)
    else:
        logger.warning(f"{SETTING_PATH} は既に存在しています")


def display_usage() -> None:
    """コマンドライン引数のヘルプを表示する"""
    usage = (
        ""
        "[usage]\n"
        "python -m snippet setting    # 設定ファイルのテンプレートを生成\n"
        "python -m snippet register   # スニペットを登録"
    )
    print(usage)


def main() -> None:
    """メイン処理"""
    args = get_argument()

    match args.mode:
        case Mode.SETTING:
            prepare_setting_file()
        case Mode.REGISTER:
            resist_snippet()
        case _:
            display_usage()
