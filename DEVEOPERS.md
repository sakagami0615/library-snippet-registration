# for developers

## create environment

```bash
# TODO: python3.10でない場合は、あらかしめ切り替える
pyenv global 3.10.x

poetry install
```

## run script

```bash
poetry run python snippet_tool.py [prepare|resist|delete]
```

## run test

```bash
poetry run tox

# NOTE: 単体で実施する場合は下記の通り
poetry run tox -e py310
poetry run tox -e ruff
poetry run tox -e mypy
```
