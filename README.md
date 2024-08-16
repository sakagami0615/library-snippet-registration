# library-snippet-registration

## requirements

- python 3.12.X

## installation

```bash
pip install git+https://github.com/sakagami0615/library-snippet-registration
```

## prepare run script

### snippet_tool.py

```python
from snippet.snippet import main

if __name__ == "__main__":
    main()
```

## how to use

### generate config

以下のように実行することで2つのパラメータファイルが生成される。自身の環境に合わせて中身を記載する。

- snippet_config_template.yaml
- library_mark_template.yaml

```bash
python snippet_tool.py prepare
```

### run resist snippet

```bash
python snippet_tool.py resist -c ./snippet_config_template.yaml
```

## for developers

### create environment

```bash
# TODO: python3.10でない場合は、あらかしめ切り替える
pyenv global 3.10.x

poetry install
```

### run script

```bash
poetry run python snippet_tool.py [prepare|resist|delete]
```

### run test

```bash
poetry run tox

# NOTE: 単体で実施する場合は下記の通り
poetry run tox -e py312
poetry run tox -e ruff
poetry run tox -e mypy
```
