# for developers

## 環境構築

仮想環境構築には `pyenv` と `poetry` を使用します。

```bash
# サポートしているpytonパッケージに切り替える
pyenv local 3.xx.x

poetry install
```

## ツール実行

```bash
# Usage表示
poetry run python -m snippet register

# ツール設定ファイル生成
poetry run python snippet_tool.py prepare

# スニペット登録
poetry run python snippet_tool.py register
```

## テスト実行

```bash
poetry run tox

# NOTE: 単体で実施する場合は下記の通り
poetry run tox -e py310
poetry run tox -e py311
poetry run tox -e py312
poetry run tox -e ruff
poetry run tox -e mypy
```
