# 開発者向けドキュメント

このドキュメントでは、本プロジェクトの開発環境のセットアップや開発時に必要な作業手順について説明します。

## 目次

- [開発環境](#開発環境)
- [開発環境の準備](#開発環境の準備)
- [テストデータを用いた動作確認](#テストデータを用いた動作確認)
- [toxによる単体テストと静的解析](#toxによる単体テストと静的解析)
- [カバレッジレポート作成](#カバレッジレポート作成)
- [pre-commitの設定](#pre-commitの設定)
- [GitHub Actionsの設定](#github-actionsの設定)

## 開発環境

本プロジェクトでは以下の環境を使用しています。

- **Pythonバージョン管理**: pyenv
- **パッケージ管理**: Poetry
- **対応Pythonバージョン**: 3.10, 3.11, 3.12

なお、各種設定に関しては. `pyproject.toml` に記載しています。

## 開発環境の準備

### 1. pyenvのインストール

pyenvがインストールされていない場合は、以下の手順でインストールしてください。

**macOS / Linux:**
```bash
curl https://pyenv.run | bash
```

**インストール後、シェルの設定ファイルに以下を追加:**
```bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

### 2. 必要なPythonバージョンのインストール

```bash
pyenv install 3.10
pyenv install 3.11
pyenv install 3.12
```

### 3. プロジェクトディレクトリでのPythonバージョン設定

プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
pyenv local 3.10 3.11 3.12
```

これにより、`.python-version`ファイルが作成され、プロジェクトで使用するPythonバージョンが指定されます。

### 4. Poetryのインストール

Poetryがインストールされていない場合は、以下のコマンドでインストールしてください。

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 5. 依存パッケージのインストール

プロジェクトのルートディレクトリで以下のコマンドを実行し、開発環境の依存パッケージをインストールします。

```bash
poetry install --with dev
```

これにより、仮想環境が自動的に作成され、必要なパッケージがインストールされます。

### 6. 仮想環境の有効化

```bash
poetry shell
```

または、`poetry run`を使用してコマンドを実行することもできます。

```bash
# usageが表示されます
poetry run python -m snippet
```

## テストデータを用いた動作確認

動作確認用として. `tests/sample_data` に簡易データ（ライブラリブロックを記載したコード等）を配しています。

> [tests/sample_data フォルダの中身の説明]  
> - .library-snippet-registration/setting.yml: 設定ファイル
> - sample_lib: ライブラリブロックを記載したコード
> - output: テスト用スニペットjson配置フォルダ

`tests/sample_data` フォルダに移動後、ツール実行コマンドによりこのテストデータに対してツールを実施することができます。

```bash
cd tests/sample_data

# ツール実行コマンド: Unix OS の場合
PYTHONPATH=../.. poetry run python -m snippet register

# ツール実行コマンド: Windows OS の場合
$env:PYTHONPATH = "../.."; poetry run python -m snippet register
```

## toxによる単体テストと静的解析

本プロジェクトでは、複数のPythonバージョンでのテストと静的解析を自動化するためにtoxを使用しています。

### 全てのテスト環境を実行

```bash
poetry run tox
```

これにより、以下の環境でテストと静的解析が実行されます。

- `py310`: Python 3.10でのテスト (テストコードはtestsに配置)
- `py311`: Python 3.11でのテスト (テストコードはtestsに配置)
- `py312`: Python 3.12でのテスト (テストコードはtestsに配置)
- `ruff`: Ruffによるコードフォーマットとリント (./snippetのコードのみ)
- `mypy`: 型チェック (./snippetのコードのみ)

### 特定の環境のみ実行

```bash
# Python 3.10のテストのみ (py311、py312でも実施可能)
poetry run tox -e py310

# Ruffによる静的解析のみ
poetry run tox -e ruff

# 型チェックのみ
poetry run tox -e mypy
```

## カバレッジレポート作成

テストのカバレッジレポートを生成するには、以下のコマンドを実行します。

### カバレッジ付きテストの実行

```bash
poetry run pytest --cov=snippet
```

### カバレッジレポートの詳細表示

```bash
poetry run pytest --cov=snippet --cov-report=term-missing
```

### HTMLカバレッジレポートの生成

```bash
poetry run pytest --cov=snippet --cov-report=html
```

HTMLレポートは `htmlcov/index.html` に生成されます。ブラウザで開いて確認してください。

## pre-commitの設定

本プロジェクトでは、コミット前に自動的にコード品質チェックを実行するためにpre-commitを使用しています。

### pre-commitのセットアップ

```bash
poetry run pre-commit install
```

これにより、Gitコミット時に自動的に以下のチェックが実行されます。

- 行末の空白削除
- ファイル末尾の改行チェック
- YAMLファイルの構文チェック
- 大容量ファイルの検出
- Ruffによるコードフォーマットとリント
- mypyによる型チェック

### pre-commitの手動実行

コミット前に全てのファイルに対してpre-commitを実行したい場合:

```bash
poetry run pre-commit run --all-files
```

### 特定のhookのみ実行

```bash
# Ruffのみ実行
poetry run pre-commit run ruff --all-files

# mypyのみ実行
poetry run pre-commit run mypy --all-files
```

### pre-commitの設定ファイル

設定は`.pre-commit-config.yaml`に記載されています。使用しているhookは以下の通りです。

- **pre-commit-hooks**: 基本的なコード品質チェック
- **ruff-pre-commit**: Ruffによるフォーマットとリント
- **mirrors-mypy**: 型チェック

## GitHub Actionsの設定

本プロジェクトでは、Pull Request時に自動的にテストと静的解析を実行するためにGitHub Actionsを使用しています。

### ワークフローの概要

GitHub Actionsの設定は`.github/workflows/ci.yml`に記載されています。

#### 1. テストジョブ (`test`)

- **対象ブランチ**: `main`, `develop`へのPull Request
- **実行環境**: Ubuntu latest
- **Pythonバージョン**: 3.10, 3.11, 3.12
- **実行内容**: 各Pythonバージョンで`poetry run pytest -v`を実行

#### 2. カバレッジレポートジョブ (`coverage`)

- **実行タイミング**: テストジョブ完了後
- **Pythonバージョン**: 3.10
- **実行内容**:
  - カバレッジ付きテストを実行
  - Pull Requestにカバレッジレポートをコメントとして投稿

#### 3. リントジョブ (`lint`)

- **Pythonバージョン**: 3.10
- **実行内容**:
  - Ruffによるフォーマットチェック
  - Ruffによるリントチェック
  - mypyによる型チェック
