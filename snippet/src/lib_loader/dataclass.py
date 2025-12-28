from dataclasses import dataclass
from dataclasses import field


@dataclass
class LibraryRuleData:
    """ライブラリコードの抽出ルールを管理するクラス.

    設定ファイルから読み込んだライブラリコードブロックのマークと
    説明プレフィックスの情報を保持します。

    Attributes:
        lib_code_block_begin (str): コードブロック開始マーク (ex: "lib:begin")
        lib_code_block_end (str): コードブロック終了マーク (ex: "lib:end")
        lib_desc_prefix_snippet_key (str): スニペットキーのプレフィックス (ex: "[snippet_key]")
        lib_desc_prefix_snippet_prefix (str): スニペットプレフィックスのプレフィックス (ex: "[snippet_prefix]")
        lib_desc_prefix_description (str): 説明のプレフィックス (ex: "[description]")
    """

    lib_code_block_begin: str
    lib_code_block_end: str
    lib_desc_prefix_snippet_key: str
    lib_desc_prefix_snippet_prefix: str
    lib_desc_prefix_description: str

    @classmethod
    def from_setting(cls, lib_setting: dict) -> "LibraryRuleData":
        """設定辞書からLibraryRuleDataオブジェクトを生成する

        Args:
            lib_setting (dict): ライブラリ設定辞書

        Returns:
            LibraryRuleData: 生成されたLibraryRuleDataオブジェクト
        """
        return cls(
            lib_code_block_begin=lib_setting["library_code_block"]["begin"],
            lib_code_block_end=lib_setting["library_code_block"]["end"],
            lib_desc_prefix_snippet_key=lib_setting["library_description_prefix"]["snippet_key"],
            lib_desc_prefix_snippet_prefix=lib_setting["library_description_prefix"]["snippet_prefix"],
            lib_desc_prefix_description=lib_setting["library_description_prefix"]["description"],
        )


@dataclass
class LanguageData:
    """プログラミング言語に関する設定を管理するクラス.

    Attributes:
        name (str): 言語名 (例: "python", "cpp")
        extensions (list[str]): 対象とするファイル拡張子のリスト (例: [".py"])
        excludes (list[str]): 除外するディレクトリやファイルパターンのリスト (例: ["__pycache__"])
    """

    name: str
    extensions: list[str] = field(default_factory=list)
    excludes: list[str] = field(default_factory=list)

    @classmethod
    def from_setting(cls, lib_setting: dict) -> "LanguageData":
        """設定辞書からLanguageDataオブジェクトを生成する

        Args:
            lib_setting (dict): ライブラリ設定辞書

        Returns:
            LanguageData: 生成されたLanguageDataオブジェクト
        """
        return cls(
            name=lib_setting["language"]["name"],
            extensions=lib_setting["language"].get("extensions", []),
            excludes=lib_setting["language"].get("excludes", []),
        )


@dataclass
class LibrarySettingData:
    """ライブラリ全体の設定を統合管理するクラス.

    Attributes:
        enable (bool): ライブラリの有効/無効フラグ
        library_name (str): ライブラリ名
        description (str): ライブラリの説明
        relative_path (str): ライブラリコードの相対パス
        language (LanguageData): 言語設定データ
        rule (LibraryRuleData): コード抽出ルール設定データ
    """

    enable: bool
    library_name: str
    description: str
    relative_path: str
    language: LanguageData
    rule: LibraryRuleData

    @classmethod
    def from_setting(cls, lib_name: str, lib_setting: dict) -> "LibrarySettingData":
        """設定辞書からLibrarySettingDataオブジェクトを生成する

        Args:
            lib_name (str): ライブラリ名
            lib_setting (dict): ライブラリ設定辞書

        Returns:
            LibrarySettingData: 生成されたLibrarySettingDataオブジェクト
        """
        language_data = LanguageData.from_setting(lib_setting)
        rule_data = LibraryRuleData.from_setting(lib_setting)

        return cls(
            enable=lib_setting["enable"],
            library_name=lib_name,
            description=lib_setting["description"],
            relative_path=lib_setting["relative_path"],
            language=language_data,
            rule=rule_data,
        )


@dataclass
class LibraryCode:
    """ライブラリコードのメタ情報を管理するクラス.

    Attributes:
        snippet_key (str): スニペットキー
        snippet_prefix (str): スニペットプレフィックス
        description (str): スニペット説明
        code_lines (list[str]): コード行のリスト
    """

    enable: bool
    library_name: str
    relative_path: str
    language: str
    snippet_key: str
    snippet_prefix: str
    description: str
    code_lines: list[str]

    @classmethod
    def from_lines(cls, lib_code_lines: list[str], setting_data: LibrarySettingData) -> "LibraryCode":
        """コード行のリストからLibraryCodeオブジェクトを生成する.

        コードブロック内の行を解析し、プレフィックスに基づいてメタデータと
        実際のコード行を分離してLibraryCodeオブジェクトを構築します。

        Args:
            lib_code_lines (list[str]): ライブラリコードの行リスト
            setting_data (LibrarySettingData): ライブラリ設定データ
                - rule: 抽出ルール（プレフィックス情報）
                - enable: ライブラリの有効/無効フラグ
                - relative_path: ライブラリの相対パス
                - language: 言語設定（name, extensions, excludes）

        Returns:
            LibraryCode: 生成されたLibraryCodeオブジェクト

        Note:
            - プレフィックス行からは、プレフィックスと"#"を除去して値を抽出します
            - プレフィックスが含まれない行は、code_linesに追加されます
            - 内部でextract_snippet_info()を呼び出して情報を抽出します
        """

        def replace(src: str, rep: str) -> str:
            return src.replace(rep, "").replace("#", "").strip()

        def extract_snippet_info() -> tuple[str, str, str, list[str]]:
            rule = setting_data.rule
            snippet_key, snippet_prefix, description = "", "", ""
            code_lines = []

            for line in lib_code_lines:
                if rule.lib_desc_prefix_snippet_key in line:
                    snippet_key = replace(line, rule.lib_desc_prefix_snippet_key)
                elif rule.lib_desc_prefix_snippet_prefix in line:
                    snippet_prefix = replace(line, rule.lib_desc_prefix_snippet_prefix)
                elif rule.lib_desc_prefix_description in line:
                    description = replace(line, rule.lib_desc_prefix_description)
                else:
                    code_lines.append(line)
            return snippet_key, snippet_prefix, description, code_lines

        snippet_key, snippet_prefix, description, code_lines = extract_snippet_info()

        return cls(
            enable=setting_data.enable,
            library_name=setting_data.library_name,
            relative_path=setting_data.relative_path,
            language=setting_data.language.name,
            snippet_key=snippet_key,
            snippet_prefix=snippet_prefix,
            description=description,
            code_lines=code_lines,
        )
