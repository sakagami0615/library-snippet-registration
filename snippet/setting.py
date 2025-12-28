"""アプリケーション全体で使用する設定定数を定義するモジュール."""

import os
from pathlib import Path

FILE_ENCODING = "utf-8"

VSCODE_SNIPPET_KEY_PREFIX = "prefix"
VSCODE_SNIPPET_KEY_DESC = "description"
VSCODE_SNIPPET_KEY_BODY = "body"

PACKAGE_PATH = Path(os.path.abspath(__file__).replace("\\", "/")).parent
TEMPLATE_SETTING_PATH = PACKAGE_PATH / Path("config_template/setting.yml")

WORKSPACE_DIRPATH = Path("./.library-snippet-registration")
BACKUP_DIRPATH = WORKSPACE_DIRPATH / Path(".backup_snippet")
SETTING_PATH = WORKSPACE_DIRPATH / Path("setting.yml")
