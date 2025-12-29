import os
from glob import glob
from logging import getLogger
from pathlib import Path
from typing import Optional

from snippet.src.common.file_helper import read_text
from snippet.src.lib_loader.check import check_library_code_block
from snippet.src.lib_loader.check import check_library_code_prefix
from snippet.src.lib_loader.dataclass import LanguageData
from snippet.src.lib_loader.dataclass import LibraryCode
from snippet.src.lib_loader.dataclass import LibrarySettingData

logger = getLogger("snippet").getChild("lib_loader")


def get_library_code_path(lib_dirpath: str, lang_data: LanguageData) -> list[str]:
    """ライブラリディレクトリから条件に合致するコードファイルのパスを取得する.

    指定されたディレクトリを再帰的に探索し、拡張子フィルタと除外フィルタを
    適用してライブラリコードファイルのパスリストを返します。

    Args:
        lib_dirpath (str): ライブラリディレクトリのパス
        lang_data (LanguageData): 言語設定データ
            - extensions: 対象とする拡張子のリスト (ex: [".py", ".cpp"])
            - excludes: 除外する文字列のリスト (ex: ["__pycache__", "_old"])

    Returns:
        list[str]: フィルタリング後のコードファイルパスのリスト

    Note:
        - ファイルパスに excludes の文字列が含まれる場合は除外されます
        - 拡張子が extensions に含まれないファイルは除外されます
    """

    def check_ignore(input_path: str, extensions: list[str], excludes: list[str]) -> bool:
        if os.path.splitext(input_path)[-1] not in extensions:
            return True
        for exclude in excludes:
            if exclude in input_path:
                return True
        return False

    code_path_list = [
        curr_path
        for curr_path in glob(os.path.join(lib_dirpath, "**"), recursive=True)
        if not check_ignore(curr_path, lang_data.extensions, lang_data.excludes)
    ]
    return code_path_list


def extract_library_code(code_path: str, setting_data: LibrarySettingData) -> Optional[list[LibraryCode]]:
    """ライブラリコードファイルからコードブロックを抽出する.

    ファイルを読み込み、開始・終了マークで囲まれたコードブロックを抽出します。
    マーク配置の検証と必須プレフィックスのチェックも行います。

    Args:
        code_path (str): ライブラリコードファイルのパス
        setting_data (LibrarySettingData): ライブラリ設定データ
            - rule: ライブラリコード抽出ルール（コードブロックマーク、プレフィックス情報）
            - enable: ライブラリの有効/無効フラグ
            - relative_path: ライブラリの相対パス
            - language: 言語設定（name, extensions, excludes）

    Returns:
        Optional[list[LibraryCode]]: 抽出されたコードブロックのリスト (各要素はLibraryCodeオブジェクト)。
            マーク配置が不正な場合はNone

    Note:
        - コードブロックは開始マークと終了マークの間の行を抽出します (マーク行自体は含まない)
        - 複数のコードブロックが存在する場合、すべてリストとして返されます
        - マーク配置が不正な場合は警告を出力してNoneを返します
        - 必須プレフィックスが欠けているブロックは警告を出力してスキップされます
    """
    lines: list[str] = read_text(Path(code_path))

    rule = setting_data.rule
    if not check_library_code_block(lines, rule.lib_code_block_begin, rule.lib_code_block_end):
        logger.warning(f"Incorrect placement of start and end marks for library code block -> {code_path}")
        return None

    begin_index_list = [idx for idx, line in enumerate(lines) if rule.lib_code_block_begin in line]
    end_index_list = [idx for idx, line in enumerate(lines) if rule.lib_code_block_end in line]

    lib_lines_list = [
        lines[begin_index + 1 : end_index] for begin_index, end_index in zip(begin_index_list, end_index_list)
    ]

    prefix_list = [
        rule.lib_desc_prefix_snippet_key,
        rule.lib_desc_prefix_snippet_prefix,
        rule.lib_desc_prefix_description,
    ]

    def enable_code_list(lines: list[str]) -> bool:
        if not check_library_code_prefix(lines, prefix_list):
            logger.warning(f"Missing required prefix ({prefix_list}) in library code block -> {code_path}")
            return False
        return True

    lib_lines_list = [lines for lines in lib_lines_list if enable_code_list(lines)]
    lib_codes = [LibraryCode.from_lines(lines, setting_data) for lines in lib_lines_list]
    return lib_codes


def load_library_code(lib_name: str, lib_setting: dict) -> list[LibraryCode]:
    """単一ライブラリの設定からコードブロックを読み込む.

    ライブラリディレクトリをスキャンし、条件に合致するファイルから
    コードブロックを抽出します。

    Args:
        lib_name (str): ライブラリ名
        lib_setting (dict): ライブラリ設定辞書
            - enable: ライブラリの有効/無効フラグ
            - relative_path: ライブラリディレクトリのパス
            - language: 言語設定（name, extensions, excludes）
            - library_code_block: コードブロックマーク設定
            - library_description_prefix: プレフィックス設定

    Returns:
        list[LibraryCode]: 抽出されたライブラリコードのリスト

    Note:
        - 設定辞書からLibrarySettingDataオブジェクトを生成して処理します
        - 各ファイルに対してextract_library_code()を呼び出します
        - relative_pathのJinja2テンプレートは、read_setting_yaml()で既に展開されています
    """
    setting_data = LibrarySettingData.from_setting(lib_name, lib_setting)

    # relative_pathは既にread_setting_yaml()でテンプレート展開済み
    lib_code_path_list = get_library_code_path(setting_data.relative_path, setting_data.language)

    lib_code_list: list[LibraryCode] = []
    for lib_code_path in lib_code_path_list:
        lib_code = extract_library_code(lib_code_path, setting_data)
        if lib_code:
            lib_code_list.extend(lib_code)

    return lib_code_list


def load_library(library_settings: dict) -> list[LibraryCode]:
    """複数のライブラリ設定からコードブロックを一括読み込みする.

    設定ファイルから読み込んだすべてのライブラリに対して、
    コードブロックの抽出処理を実行します。

    Args:
        library_settings (dict): ライブラリ設定辞書
            キー: ライブラリ名
            値: ライブラリ設定辞書（load_library_code関数の引数参照）

    Returns:
        list[LibraryCode]: 抽出されたすべてのライブラリコードのリスト

    Note:
        - 各ライブラリは個別に処理されます
        - エラーが発生したライブラリはスキップされ、次のライブラリの処理が継続されます
    """
    lib_codes: list[LibraryCode] = []

    for lib_name, lib_setting in library_settings.items():
        logger.debug(f"Loading library: {lib_name}")
        curr_lib_codes = load_library_code(lib_name, lib_setting)
        lib_codes.extend(curr_lib_codes)
        logger.debug(f"Loaded {len(curr_lib_codes)} code blocks from {lib_name}")

    return lib_codes
