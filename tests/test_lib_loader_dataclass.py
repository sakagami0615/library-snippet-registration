"""dataclassモジュールのユニットテスト."""

from snippet.src.lib_loader.dataclass import LanguageData
from snippet.src.lib_loader.dataclass import LibraryCode
from snippet.src.lib_loader.dataclass import LibraryRuleData
from snippet.src.lib_loader.dataclass import LibrarySettingData


def test_library_rule_data_from_setting() -> None:
    """LibraryRuleData.from_settingメソッドのテスト."""
    lib_setting = {
        "library_code_block": {"begin": "lib:begin", "end": "lib:end"},
        "library_description_prefix": {
            "snippet_key": "[snippet_key]",
            "snippet_prefix": "[snippet_prefix]",
            "description": "[description]",
        },
    }

    rule_data = LibraryRuleData.from_setting(lib_setting)

    assert rule_data.lib_code_block_begin == "lib:begin"
    assert rule_data.lib_code_block_end == "lib:end"
    assert rule_data.lib_desc_prefix_snippet_key == "[snippet_key]"
    assert rule_data.lib_desc_prefix_snippet_prefix == "[snippet_prefix]"
    assert rule_data.lib_desc_prefix_description == "[description]"


def test_language_data_from_setting_with_all_fields() -> None:
    """すべてのフィールドが存在する場合のLanguageData.from_settingテスト."""
    lib_setting = {
        "language": {
            "name": "python",
            "extensions": [".py"],
            "excludes": ["__pycache__", "test"],
        }
    }

    lang_data = LanguageData.from_setting(lib_setting)

    assert lang_data.name == "python"
    assert lang_data.extensions == [".py"]
    assert lang_data.excludes == ["__pycache__", "test"]


def test_language_data_from_setting_without_optional_fields() -> None:
    """オプショナルフィールドがない場合のLanguageData.from_settingテスト."""
    lib_setting = {"language": {"name": "cpp"}}

    lang_data = LanguageData.from_setting(lib_setting)

    assert lang_data.name == "cpp"
    assert lang_data.extensions == []
    assert lang_data.excludes == []


def test_library_setting_data_from_setting() -> None:
    """LibrarySettingData.from_settingメソッドのテスト."""
    lib_setting = {
        "enable": True,
        "description": "Test library",
        "relative_path": "./lib",
        "language": {"name": "python", "extensions": [".py"], "excludes": ["test"]},
        "library_code_block": {"begin": "lib:begin", "end": "lib:end"},
        "library_description_prefix": {
            "snippet_key": "[snippet_key]",
            "snippet_prefix": "[snippet_prefix]",
            "description": "[description]",
        },
    }

    setting_data = LibrarySettingData.from_setting("test_lib", lib_setting)

    assert setting_data.enable is True
    assert setting_data.library_name == "test_lib"
    assert setting_data.description == "Test library"
    assert setting_data.relative_path == "./lib"
    assert setting_data.language.name == "python"
    assert setting_data.rule.lib_code_block_begin == "lib:begin"


def test_library_code_from_lines_basic() -> None:
    """基本的なLibraryCode.from_linesメソッドのテスト."""
    lib_code_lines = [
        "# [snippet_key] my_function",
        "# [snippet_prefix] myfunc",
        "# [description] My function",
        "def my_function():",
        "    pass",
    ]

    lib_setting = {
        "enable": True,
        "description": "Test library",
        "relative_path": "./lib",
        "language": {"name": "python"},
        "library_code_block": {"begin": "lib:begin", "end": "lib:end"},
        "library_description_prefix": {
            "snippet_key": "[snippet_key]",
            "snippet_prefix": "[snippet_prefix]",
            "description": "[description]",
        },
    }
    setting_data = LibrarySettingData.from_setting("test_lib", lib_setting)

    lib_code = LibraryCode.from_lines(lib_code_lines, setting_data)

    assert lib_code.enable is True
    assert lib_code.library_name == "test_lib"
    assert lib_code.relative_path == "./lib"
    assert lib_code.language == "python"
    assert lib_code.snippet_key == "my_function"
    assert lib_code.snippet_prefix == "myfunc"
    assert lib_code.description == "My function"
    assert len(lib_code.code_lines) == 2
    assert lib_code.code_lines[0] == "def my_function():"
    assert lib_code.code_lines[1] == "    pass"


def test_library_code_from_lines_with_comment_markers() -> None:
    """コメントマーカーが含まれる場合のLibraryCode.from_linesテスト."""
    lib_code_lines = [
        "# # [snippet_key] my_function",
        "## [snippet_prefix] myfunc",
        "#[description] My function",
        "def my_function():",
        "    # This is a comment",
        "    pass",
    ]

    lib_setting = {
        "enable": True,
        "description": "Test library",
        "relative_path": "./lib",
        "language": {"name": "python"},
        "library_code_block": {"begin": "lib:begin", "end": "lib:end"},
        "library_description_prefix": {
            "snippet_key": "[snippet_key]",
            "snippet_prefix": "[snippet_prefix]",
            "description": "[description]",
        },
    }
    setting_data = LibrarySettingData.from_setting("test_lib", lib_setting)

    lib_code = LibraryCode.from_lines(lib_code_lines, setting_data)

    assert lib_code.snippet_key == "my_function"
    assert lib_code.snippet_prefix == "myfunc"
    assert lib_code.description == "My function"
    assert len(lib_code.code_lines) == 3


def test_library_code_from_lines_empty() -> None:
    """空の行リストのLibraryCode.from_linesテスト."""
    lib_code_lines: list[str] = []

    lib_setting = {
        "enable": True,
        "description": "Test library",
        "relative_path": "./lib",
        "language": {"name": "python"},
        "library_code_block": {"begin": "lib:begin", "end": "lib:end"},
        "library_description_prefix": {
            "snippet_key": "[snippet_key]",
            "snippet_prefix": "[snippet_prefix]",
            "description": "[description]",
        },
    }
    setting_data = LibrarySettingData.from_setting("test_lib", lib_setting)

    lib_code = LibraryCode.from_lines(lib_code_lines, setting_data)

    assert lib_code.snippet_key == ""
    assert lib_code.snippet_prefix == ""
    assert lib_code.description == ""
    assert len(lib_code.code_lines) == 0
