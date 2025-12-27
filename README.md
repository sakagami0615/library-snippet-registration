# library-snippet-registration

## 対応しているPythonバージョン

- python 3.10.X

## インストール方法

```bash
pip install git+https://github.com/sakagami0615/library-snippet-registration
```

## 使用方法

### 事前準備

ツールを使用する事前準備として、下記のコマンドを実行してライブラリに関する情報などを記載するためのsetting.ymlを生成します。  
コマンド実行後 `.library_snippet_registration/setting.yml` が生成されます。

```bash
python -m snippet setting  
```

> [注意]  
> すでに `.library_snippet_registration/setting.yml` が存在する場合、コマンドは失敗します。  
> 再生成したい場合は、元あるファイルを削除するかリネームしてください。

生成された `.library_snippet_registration/setting.yml` の設定値を記載します。

```yml
# TODO: 設定値の説明を記載する
```

### ツール実行

`.library_snippet_registration/setting.yml` の記載が完了している状態で、下記コマンドを実行します。

```bash
python -m snippet register  
```

複数のデバイスを記載している場合、対象のデバイスを選択します。

```bash
> python -m snippet register

choose device
1. {your setting device}
2. {your setting device}
>>> 
```
