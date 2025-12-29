# for developers

## 環境構築

仮想環境構築には `pyenv` と `poetry` を使用します。

```bash
# サポートしているpytonパッケージに切り替える
pyenv local 3.xx.x

poetry install
```

## テストデータを用いたツールの実行

テスト用のデータを置いているフォルダに移動後、ツールコマンドを実行することでテストデータに対してツールを実施できます。

```bash
cd tests/sample_data

# [フォルダの中身の説明]
# sample_data/.library-snippet-registration/setting.yml: 設定ファイル
# sample_data/sample_lib: テスト用のライブラリコード
# sample_data/output: テスト用スニペットjson配置フォルダ
```

```bash
# ツール実行コマンド: Unix OS の場合
PYTHONPATH=../.. poetry run python -m snippet register

# ツール実行コマンド: Windows OS の場合
$env:PYTHONPATH = "../.."; poetry run python -m snippet register
```

## 実際のツール実行コマンド

[READMEの使用方法](../README.md) を参照してください。

## テスト実行

```bash
poetry run tox

# NOTE: 単体で実施する場合は下記の通り
poetry run tox -e py310
poetry run tox -e py311
poetry run tox -e py312

# NOTE: 静的解析のみ実施する場合は下記の通り
poetry run tox -e ruff
poetry run tox -e mypy
```

テストの設定は `pyproject.toml` に記載しています。

## カバレッジ取得

テストのカバレッジを確認する場合は以下のコマンドを実行します。  
コマンド実行後　`htmlcov/index.html` にレポートが生成されます。

```bash
# ターミナルにカバレッジレポートを表示
poetry run pytest --cov=snippet --cov-report=term-missing

# HTMLレポートも生成する場合
poetry run pytest --cov=snippet --cov-report=term-missing --cov-report=html
```

カバレッジの設定は `pyproject.toml` に記載しています。
なお、`__main__.py` と `version.py` はカバレッジ計測から除外されています。
