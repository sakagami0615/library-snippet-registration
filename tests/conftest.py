import pytest

import os
import json
import yaml
import inspect

import io
from logging import getLogger
from logging import StreamHandler, DEBUG



def get_test_case_path():
    """実行したテストスクリプトからケースのパスを取得。
    NOTE:テストフォルダの階層が変わると想定しない動作になる可能性があるため注意。
    """
    test_script_path = inspect.stack()[2].filename
    return os.path.join(os.path.dirname(test_script_path), "test_case")


@pytest.fixture(scope="function")
def get_stream():
    """指定した名前のロガーを取得。
    アプリ内のロガー出力チェック用に使用。
    """
    def func(suffix):
        logger = getLogger("snippet").getChild(suffix)
        logger.setLevel(DEBUG)
        capture_stream = io.StringIO()
        stream_handler = StreamHandler(stream=capture_stream)
        stream_handler.setLevel(DEBUG)
        logger.addHandler(stream_handler)
        return capture_stream
    return func


@pytest.fixture(scope="function")
def get_path():
    """テストフォルダを起点とした相対パスを絶対パスにする。
    """
    def func(rel_path):
        return os.path.join(get_test_case_path(), rel_path)
    return func


@pytest.fixture(scope="function")
def read_yaml():
    def func(yaml_rel_path):
        yaml_path = os.path.join(get_test_case_path(), yaml_rel_path)
        with open(yaml_path, encoding="utf-8") as f:
            yaml_dict = yaml.safe_load(f)
        return yaml_dict
    return func


@pytest.fixture(scope="function")
def read_json():
    def func(json_rel_path):
        json_path = os.path.join(get_test_case_path(), json_rel_path)
        with open(json_path, encoding="utf-8") as f:
            json_dict = json.load(f)
        return json_dict
    return func


@pytest.fixture(scope="function")
def read_text():
    def func(text_rel_path):
        text_path = os.path.join(get_test_case_path(), text_rel_path)
        with open(text_path, encoding="utf-8") as f:
            lines = [s.rstrip("\n") for s in f.readlines()]
        return lines
    return func


@pytest.fixture(scope="function")
def read_snippet():
    def read_json(json_path):
        with open(json_path, encoding="utf-8") as f:
            json_dict = json.load(f)
        return json_dict

    def get_snippet_dict(read_dict):
        snippet_dict = {"script_path": "", "snippet_key": "", "snippet_prefix": "", "description": "", "code": []}
        for key in snippet_dict.keys():
            if key in read_dict:
                snippet_dict[key] = read_dict[key]
        return snippet_dict

    def func(json_rel_path):
        json_path = os.path.join(get_test_case_path(), json_rel_path)
        snippet_items = read_json(json_path)
        return [get_snippet_dict(snippet_item) for snippet_item in snippet_items]

    return func