"""スニペットファイルの更新処理を行うモジュール."""

from collections import defaultdict
from copy import deepcopy
from logging import getLogger
from pathlib import Path

from snippet.setting import VSCODE_SNIPPET_KEY_BODY
from snippet.setting import VSCODE_SNIPPET_KEY_DESC
from snippet.setting import VSCODE_SNIPPET_KEY_PREFIX
from snippet.src.common.file_helper import read_jsonc
from snippet.src.common.file_helper import write_json
from snippet.src.common.groupby import groupby
from snippet.src.lib_loader.dataclass import LibraryCode

logger = getLogger("snippet").getChild("update_snippet")


def delete_latest_library_snippet(snippet_data: defaultdict, library_name: str) -> defaultdict:
    """指定したライブラリ名で始まるスニペットキーを削除する.

    Args:
        snippet_data (defaultdict): スニペットデータ辞書
        library_name (str): 削除対象のライブラリ名

    Returns:
        defaultdict: 指定ライブラリのスニペットを除いたスニペットデータ
    """
    result_snippet_data: defaultdict = defaultdict()
    for snippet_key, snippet_value in snippet_data.items():
        if not snippet_key.startswith(f"{library_name}@"):
            result_snippet_data[snippet_key] = snippet_value
    return result_snippet_data


def update_library_snippet(snippet_data: defaultdict, lib_codes: list[LibraryCode]) -> defaultdict:
    """ライブラリコードをスニペットデータに追加する.

    Args:
        snippet_data (defaultdict): 既存のスニペットデータ辞書
        lib_codes (list[LibraryCode]): 追加するライブラリコードのリスト

    Returns:
        defaultdict: ライブラリコードを追加したスニペットデータ
    """
    snippet_data = deepcopy(snippet_data)

    for code in lib_codes:
        snippet_key = f"{code.library_name}@{code.snippet_key}"
        snippet_prefix = code.snippet_prefix
        description = code.description
        body = code.code_lines

        if code.enable:
            snippet_data[snippet_key] = {
                VSCODE_SNIPPET_KEY_PREFIX: snippet_prefix,
                VSCODE_SNIPPET_KEY_DESC: description,
                VSCODE_SNIPPET_KEY_BODY: body,
            }
    return snippet_data


def update_language_snippet(snippet_data: defaultdict, lang_codes: list[LibraryCode]) -> defaultdict:
    """言語ごとのスニペットデータを更新する.

    同一ライブラリの既存スニペットを削除してから、
    新しいライブラリコードをスニペットデータに追加します。

    Args:
        snippet_data (defaultdict): 既存のスニペットデータ辞書
        lang_codes (list[LibraryCode]): 言語ごとのライブラリコードリスト

    Returns:
        defaultdict: 更新されたスニペットデータ
    """
    snippet_data = deepcopy(snippet_data)

    # ライブラリごとにコードをグルーピング
    lib_groupby_codes = groupby(lang_codes, lambda code: code.library_name)

    # 以前に登録していたライブラリのスニペットを削除
    for lib_name in lib_groupby_codes.keys():
        snippet_data = delete_latest_library_snippet(snippet_data, lib_name)

    # ライブラリごとにスニペットを追加
    for lib_codes in lib_groupby_codes.values():
        snippet_data = update_library_snippet(snippet_data, lib_codes)

    return snippet_data


def write_device_snippet_file(editor_name: str, snippet_path: Path, snippet_data: defaultdict) -> None:
    """スニペットデータをJSONファイルに書き込む.

    Args:
        editor_name (str): エディタ名（ログ出力用）
        snippet_path (Path): スニペットファイルパス
        snippet_data (defaultdict): 書き込むスニペットデータ
    """
    write_json(snippet_path, snippet_data)
    logger.info(f"[{editor_name}] Snippet file updated: {snippet_path}")


def update_snippet(device_setting: dict, lib_codes: list[LibraryCode]) -> None:
    """デバイスのスニペットファイルを更新する.

    言語ごとにライブラリコードをグループ化し、
    各エディタのスニペットファイルを更新します。

    Args:
        device_setting (dict): デバイス設定辞書
            - snippet_path: スニペットパスの辞書 {エディタ名: スニペットディレクトリパス}
        lib_codes (list[LibraryCode]): 更新するライブラリコードのリスト
    """
    # 言語ごとにコードをグルーピング
    lang_groupby_codes = groupby(lib_codes, lambda code: code.language)

    for lang, lang_codes in lang_groupby_codes.items():
        # 各エディタごとにスニペットファイルを更新
        for editor_name, snippet_dirpath in device_setting["snippet_path"].items():
            snippet_path = Path(snippet_dirpath) / Path(f"{lang}.json")
            jsonc_data = read_jsonc(snippet_path)
            snippet_data = update_language_snippet(defaultdict(dict, jsonc_data), lang_codes)
            write_device_snippet_file(editor_name, snippet_path, snippet_data)
