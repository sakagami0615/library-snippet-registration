import pytest

import json
from pathlib import Path

from snippet.src.library_loader import CodeInfo



@pytest.fixture(scope="function")
def read_code_infos():
    def func(code_info_json):
        with open(code_info_json, encoding="utf-8") as f:
            json_dict = json.load(f)
        return [CodeInfo(**data) for data in json_dict]
    return func


@pytest.fixture(scope="function")
def tmp_snippet_filepath():
    snippet_filepath = Path("./tmp_snippet.json")
    with open(snippet_filepath, 'w'): pass
    yield snippet_filepath
    if snippet_filepath.exists():
        snippet_filepath.unlink()