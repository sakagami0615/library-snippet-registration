import pytest

import os
import tempfile
from pathlib import Path



@pytest.fixture(scope="function")
def dummy_backup_dirpath():
    backup_dirpath = Path(tempfile.TemporaryDirectory(delete=False).name)
    yield backup_dirpath


@pytest.fixture(scope="function")
def dummy_library_dirpath():
    library_dirpath = Path(tempfile.TemporaryDirectory(delete=False).name)
    yield library_dirpath


@pytest.fixture(scope="function")
def dummy_mark_filepath():
    mark_filepath = Path(tempfile.NamedTemporaryFile(suffix=".yaml", delete=False).name)
    yield mark_filepath


@pytest.fixture(scope="function")
def dummy_snippet_filepath():
    snippet_dirpath = Path(tempfile.TemporaryDirectory(delete=False).name)
    snippet_filepath = snippet_dirpath.joinpath("snippet.json")
    yield snippet_filepath


@pytest.fixture(scope="function")
def dummy_extensions():
    yield [".py"]


@pytest.fixture(scope="function")
def dummy_excludes():
    yield []


@pytest.fixture(scope="function")
def tmp_library_dirpath():
    library_dirpath = Path("./tmp_library")
    os.makedirs(library_dirpath, exist_ok=True)
    yield library_dirpath
    if library_dirpath.exists():
        os.removedirs(library_dirpath)


@pytest.fixture(scope="function")
def tmp_mark_filepath():
    mark_filepath = Path("./tmp_mark.yaml")
    with open(mark_filepath, 'w'): pass
    yield mark_filepath
    if mark_filepath.exists():
        mark_filepath.unlink()
