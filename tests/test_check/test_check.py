import pytest


from pathlib import Path
from snippet.src.snippet_diff import SnippetDiff

from snippet.src.library_loader import LibraryLoader, CodeInfo



@pytest.mark.parametrize(
    "path_a, path_b, path_expected",
    [
        pytest.param("diff_snippets/case1/snippet_a.json", "diff_snippets/case1/snippet_b.json", "diff_snippets/case1/expected.txt", id="same single"),
        pytest.param("diff_snippets/case2/snippet_a.json", "diff_snippets/case2/snippet_b.json", "diff_snippets/case2/expected.txt", id="diff body"),
        pytest.param("diff_snippets/case3/snippet_a.json", "diff_snippets/case3/snippet_b.json", "diff_snippets/case3/expected.txt", id="diff all"),
        pytest.param("diff_snippets/case4/snippet_a.json", "diff_snippets/case4/snippet_b.json", "diff_snippets/case4/expected.txt", id="new and delete"),
        pytest.param("diff_snippets/case5/snippet_a.json", "diff_snippets/case5/snippet_b.json", "diff_snippets/case5/expected.txt", id="same multiple"),
    ],
)
def test__diff_snippets(get_stream, read_json, read_text, path_a, path_b, path_expected):
    capture_stream = get_stream("snippet_diff")
    snippet_a, snippet_b = read_json(path_a), read_json(path_b)
    expected = read_text(path_expected)

    SnippetDiff.logger_snippet_diff(snippet_a, snippet_b)
    assert capture_stream.getvalue().splitlines() == expected



@pytest.mark.parametrize(
    "code_path, mark_path, extensions, excludes, path_expected",
    [
        pytest.param("get_library/case1", "get_library/case1/mark.yaml", [".py"], [], "get_library/case1/expected.json", id="code single"),
        pytest.param("get_library/case2", "get_library/case2/mark.yaml", [".py"], [], "get_library/case2/expected.json", id="code multiple"),
        pytest.param("get_library/case3", "get_library/case3/mark.yaml", [".py"], [], "get_library/case3/expected.json", id="not description"),
        pytest.param("get_library/case4", "get_library/case4/mark.yaml", [".py"], [], "get_library/case4/expected.json", id="diff mark"),
        pytest.param("get_library/case5", "get_library/case5/mark.yaml", [".py"], [], "get_library/case5/expected.json", id="file multiple"),
        pytest.param("get_library/case6", "get_library/case6/mark.yaml", [".py"], ["exclude"], "get_library/case6/expected.json", id="file exclude"),
        pytest.param("get_library/case7", "get_library/case7/mark.yaml", [".py"], [], "get_library/case7/expected.json", id="library syntax error"),
        pytest.param("get_library/case8", "get_library/case8/mark.yaml", [".py"], [], "get_library/case8/expected.json", id="library duplicate key"),
        pytest.param("get_library/case9", "get_library/case9/mark.yaml", [".py"], [], "get_library/case9/expected.json", id="library duplicate prefix"),
    ],
)
def test__get_library(get_path, read_snippet, code_path, mark_path, extensions, excludes, path_expected):
    expected = [CodeInfo(**data) for data in read_snippet(path_expected)]
    lib_loader = LibraryLoader(Path(get_path(mark_path)), Path(get_path(code_path)), extensions, excludes)
    result = lib_loader.read_lib_codes()
    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert e == r



@pytest.mark.parametrize(
    "code_path, mark_path, extensions, path_expected",
    [
        pytest.param("syntax_error_library/case1", "syntax_error_library/case1/mark.yaml", [".py"], "syntax_error_library/case1/expected.txt", id="error nothing"),
        pytest.param("syntax_error_library/case2", "syntax_error_library/case2/mark.yaml", [".py"], "syntax_error_library/case2/expected.txt", id="lib_end syntax error"),
        pytest.param("syntax_error_library/case3", "syntax_error_library/case3/mark.yaml", [".py"], "syntax_error_library/case3/expected.txt", id="lib_begin syntax error"),
        pytest.param("syntax_error_library/case4", "syntax_error_library/case4/mark.yaml", [".py"], "syntax_error_library/case4/expected.txt", id="lib_begin only"),
    ],
)
def test__syntax_error_library(get_stream, get_path, read_text, code_path, mark_path, extensions, path_expected):
    capture_stream = get_stream("file_helper")
    expected = read_text(path_expected)

    lib_loader = LibraryLoader(Path(get_path(mark_path)), Path(get_path(code_path)), extensions)
    lib_loader.read_lib_codes()
    result = capture_stream.getvalue().splitlines()

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert e in r



@pytest.mark.parametrize(
    "code_path, mark_path, extensions, path_expected",
    [
        pytest.param("syntax_shortage_library/case1", "syntax_shortage_library/case1/mark.yaml", [".py"], "syntax_shortage_library/case1/expected.txt", id="key not exist"),
        pytest.param("syntax_shortage_library/case2", "syntax_shortage_library/case2/mark.yaml", [".py"], "syntax_shortage_library/case2/expected.txt", id="prefix not exist"),
        pytest.param("syntax_shortage_library/case3", "syntax_shortage_library/case3/mark.yaml", [".py"], "syntax_shortage_library/case3/expected.txt", id="key blank"),
        pytest.param("syntax_shortage_library/case4", "syntax_shortage_library/case4/mark.yaml", [".py"], "syntax_shortage_library/case4/expected.txt", id="prefix blank"),
    ],
)
def test__syntax_shortage_library(get_stream, get_path, read_text, code_path, mark_path, extensions, path_expected):
    capture_stream = get_stream("library_loader")
    expected = read_text(path_expected)

    lib_loader = LibraryLoader(Path(get_path(mark_path)), Path(get_path(code_path)), extensions)
    a = lib_loader.read_lib_codes()
    result = capture_stream.getvalue().splitlines()
    print((a, 1))
    print((result, 1))

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert e in r



@pytest.mark.parametrize(
    "code_path, mark_path, extensions, path_expected",
    [
        pytest.param("duplicate_library/case1", "duplicate_library/case1/mark.yaml", [".py"], "duplicate_library/case1/expected.txt", id="duplicate key"),
        pytest.param("duplicate_library/case2", "duplicate_library/case2/mark.yaml", [".py"], "duplicate_library/case2/expected.txt", id="duplicate prefix"),
    ],
)
def test__duplicate_library(get_stream, get_path, read_text, code_path, mark_path, extensions, path_expected):
    capture_stream = get_stream("library_loader")
    expected = read_text(path_expected)

    lib_loader = LibraryLoader(Path(get_path(mark_path)), Path(get_path(code_path)), extensions)
    lib_loader.read_lib_codes()
    result = capture_stream.getvalue().splitlines()

    assert len(result) == len(expected)
    for r, e in zip(result, expected):
        assert e in r
