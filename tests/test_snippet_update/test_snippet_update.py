import pytest
from freezegun import freeze_time

import shutil
from pathlib import Path

from snippet.src.snippet_updater import SnippetUpdater



@pytest.mark.parametrize(
    "snippet_path, code_info_path, path_expected",
    [
        pytest.param(Path("test_snippet.json"), Path("new_snippet/case1/code_info.json"), Path("new_snippet/case1/expected.json"), id="create new snippet"),
    ]
)
def test__generate_new_snippet(get_path, read_json, read_code_infos,
                               snippet_path, code_info_path, path_expected):
    code_infos = read_code_infos(get_path(code_info_path))

    updater = SnippetUpdater(False)
    result = updater.resist_snippet(snippet_path, code_infos)
    if snippet_path.exists():
        snippet_path.unlink()

    assert result == read_json(path_expected)


def test__delete_enable_snippet(tmp_snippet_filepath):
    updater = SnippetUpdater()
    updater.delete_snippet(tmp_snippet_filepath)
    assert not tmp_snippet_filepath.exists()


@pytest.mark.parametrize(
    "snippet_path, expected",
    [
        pytest.param(Path("tmp_snippet.json"), ["delete snippet (tmp_snippet.json)"], id="exist"),
        pytest.param(Path("not_exist_snippet.json"), ["failed to delete snippet (not_exist_snippet.json is not exist)"], id="not_exist"),
    ]
)
def test__delete_disable_snippet(tmp_snippet_filepath,
                                 get_stream, snippet_path, expected):
    capture_stream = get_stream("snippet_updater")
    updater = SnippetUpdater()

    updater.delete_snippet(snippet_path)
    assert capture_stream.getvalue().splitlines() == expected


@freeze_time("2024-10-10 01:02:03")
@pytest.mark.parametrize(
    "backup_path, snippet_path, expected",
    [
        pytest.param(Path("test_backup"), "backup_snippet/case1/snippet.json", ["create backup snippet (test_backup/snippet_20241010_010203.json)"], id="backup"),
        pytest.param(Path(), "backup_snippet/case1/snippet.json", [], id="not_backup"),
    ]
)
def test__backup_snippet(get_stream, get_path, backup_path, snippet_path, expected):
    capture_stream = get_stream("snippet_updater")
    updater = SnippetUpdater(backup_folder_path=backup_path)

    snippet_path = Path(get_path(snippet_path))

    backup_snippet_path = updater._backup_snippet(snippet_path)
    if backup_snippet_path and backup_snippet_path.exists():
        shutil.rmtree(backup_path)

    assert capture_stream.getvalue().splitlines() == expected
