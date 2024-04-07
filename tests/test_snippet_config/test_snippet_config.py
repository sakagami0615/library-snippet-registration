import pytest
import os
import shutil
from freezegun import freeze_time

from snippet.src.snippet_updater import SnippetUpdater


@freeze_time("2024-10-10 01:02:03")
@pytest.mark.parametrize(
    "expected",
    [
        pytest.param("config_template_20241010_010203", id="check config folder"),
    ]
)
def test__generate_new_config_folder(expected):
    updater = SnippetUpdater()
    gen_config_path = updater.prepare_config_file()
    if gen_config_path.exists():
        shutil.rmtree(gen_config_path)

    assert gen_config_path.name == expected



@pytest.mark.parametrize(
    "expected",
    [
        pytest.param(["library_mark_template.yaml", "snippet_config_template.yaml"], id="check config file"),
    ]
)
def test__generate_new_config_folder(expected):
    updater = SnippetUpdater()
    gen_config_path = updater.prepare_config_file()
    config_filenames = os.listdir(gen_config_path).sort()
    if gen_config_path.exists():
        shutil.rmtree(gen_config_path)

    assert config_filenames == expected.sort()
