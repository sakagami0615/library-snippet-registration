import pytest

from pathlib import Path

from snippet.src.snippet_argument import Argument



@pytest.mark.parametrize(
    "snippet_path, expected",
    [
        pytest.param(Path("snippet.json"), [], id="valid"),
        pytest.param(Path(""), ["snippet_path が設定されていません"], id="invalid"),
    ]
)
def test__set_argument_snippet_path(dummy_backup_dirpath, dummy_library_dirpath, dummy_mark_filepath, dummy_extensions, dummy_excludes,
                                    get_stream, snippet_path, expected):
    capture_stream = get_stream("snippet_updater")
    arg = Argument("delete", True, dummy_backup_dirpath, dummy_library_dirpath,
                   dummy_mark_filepath, snippet_path, dummy_extensions, dummy_excludes)
    arg.is_invalid()

    assert capture_stream.getvalue().splitlines() == expected



@pytest.mark.parametrize(
    "extensions, expected",
    [
        pytest.param([".py"], [], id="valid"),
        pytest.param([], ["extensions が設定されていません"], id="invalid"),
    ]
)
def test__set_argument_extensions(dummy_backup_dirpath, dummy_library_dirpath, dummy_mark_filepath, dummy_snippet_filepath, dummy_excludes,
                                  get_stream, extensions, expected):
    capture_stream = get_stream("snippet_updater")
    arg = Argument("delete", True, dummy_backup_dirpath, dummy_library_dirpath,
                   dummy_mark_filepath, dummy_snippet_filepath, extensions, dummy_excludes)
    arg.is_invalid()

    assert capture_stream.getvalue().splitlines() == expected



@pytest.mark.parametrize(
    "library_path, expected",
    [
        pytest.param(Path("tmp_library"), [], id="valid"),
        pytest.param(Path("not_exist_library"), ["library_path が存在しません (設定値: not_exist_library)"], id="invalid"),
    ]
)
def test__valid_argument_library_path(tmp_library_dirpath,
                                      dummy_backup_dirpath, dummy_mark_filepath, dummy_snippet_filepath, dummy_extensions, dummy_excludes,
                                      get_stream, library_path, expected):
    capture_stream = get_stream("snippet_updater")
    arg = Argument("delete", True, dummy_backup_dirpath, library_path,
                   dummy_mark_filepath, dummy_snippet_filepath, dummy_extensions, dummy_excludes)
    arg.is_invalid()

    assert capture_stream.getvalue().splitlines() == expected



@pytest.mark.parametrize(
    "mark_path, expected",
    [
        pytest.param(Path("tmp_mark.yaml"), [], id="valid"),
        pytest.param(Path("not_exist_mark.yaml"), ["mark_path が存在しません (設定値: not_exist_mark.yaml)"], id="invalid"),
    ]
)
def test__valid_argument_mark_path(tmp_mark_filepath,
                                   dummy_backup_dirpath, dummy_library_dirpath, dummy_snippet_filepath, dummy_extensions, dummy_excludes,
                                   get_stream, mark_path, expected):
    capture_stream = get_stream("snippet_updater")
    arg = Argument("delete", True, dummy_backup_dirpath, dummy_library_dirpath,
                   mark_path, dummy_snippet_filepath, dummy_extensions, dummy_excludes)
    arg.is_invalid()

    assert capture_stream.getvalue().splitlines() == expected
