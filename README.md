# library-snippet-registration

作成したライブラリコードを VSCode や Cursor 等のコードエディタ用のスニペットに登録するためのツールです。

1. 設定ファイル:
  setting.yml という設定ファイルに `ライブラリの場所` `スニペットの保存先` 等記述します。
2. スニペットに登録したいコードのマーキング:
  ライブラリのソースコード内に、特別なコメント（[snippet_key]やlib:begin/lib:end等）を使って、スニペットとして登録したいコードブロックを指定します。
3. スニペット生成:
  ツールを実行すると、マーキングされたコードを読み取り、設定ファイルで指定されたエディタのスニペットファイル（JSON形式）を更新します。

## 対応しているPythonバージョン

- python 3.10.X
- python 3.11.X
- python 3.12.X

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
devices:
  {デバイス名}:  # 使用しているデバイスを識別する名前（例: "my-laptop", "desktop"など）
    snippet_path:
      vscode: {VSCodeのスニペットディレクトリパス}  # 例: C:\Users\username\AppData\Roaming\Code\User\snippets
      cursor: {Cursorのスニペットディレクトリパス}  # 例: C:\Users\username\AppData\Roaming\Cursor\User\snippets

tool_config:
  backup_snippet_dirpath: .backup_snippet  # スニペットファイルのバックアップ先ディレクトリ

libraries:
  {ライブラリ名}:  # 登録するライブラリの名前（例: "my-utils", "algorithms"など）
    enable: true  # ライブラリのスニペット登録を有効にするか
                  # > true: スニペットjsonに記載する
                  # > false: スニペットjsonから削除する
    description: "ライブラリの説明"  # ライブラリの説明文
    relative_path: {ライブラリパス}  # setting.ymlから見たライブラリフォルダの相対パス（例: "../my-library"）

    # 言語設定
    language:
      name: python  # プログラミング言語名(スニペットjsonの名前と一致する必要があります)
      extensions: [".py"]  # 対象とするファイル拡張子のリスト
      excludes: ["__pycache__", "test"]  # 除外するディレクトリやファイル名のパターン

    # ライブラリコードブロックの開始/終了マーカー
    library_code_block:
      begin: "lib:begin"  # ライブラリコードブロックの開始マーカー
      end: "lib:end"  # ライブラリコードブロックの終了マーカー

    # スニペット情報を記載するためのプレフィックス
    library_description_prefix:
      snippet_key: "[snippet_key]"  # スニペットキーを指定する接頭辞
      snippet_prefix: "[snippet_prefix]"  # スニペットプレフィックスを指定する接頭辞
      description: "[description]"  # スニペット説明を指定する接頭辞
```

**設定例:**

```yml
devices:
  my-laptop:
    snippet_path:
      vscode: C:\Users\username\AppData\Roaming\Code\User\snippets
      cursor: none

tool_config:
  backup_snippet_dirpath: .backup_snippet

libraries:
  my-algorithms:
    enable: true
    description: "競技プログラミング用アルゴリズムライブラリ"
    relative_path: ../algorithms
    language:
      name: python
      extensions: [".py"]
      excludes: ["__pycache__", "test", ".pytest_cache"]
    library_code_block:
      begin: "lib:begin"
      end: "lib:end"
    library_description_prefix:
      snippet_key: "[snippet_key]"
      snippet_prefix: "[snippet_prefix]"
      description: "[description]"
```

**ライブラリコードの記述例:**

ライブラリコードには、スニペット情報とコードブロックを以下のように記述します。

```python
# [snippet_key] binary_search
# [snippet_prefix] bsearch
# [description] Binary search implementation
# lib:begin
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
# lib:end
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

デバイス選択後、以下のようなログが表示され、スニペットjsonにライブラリコードが登録されます。。

```
[2025-12-29 03:59:43,951][snippet][INFO] chhose device: {デバイス名}
[2025-12-29 03:59:43,952][snippet.lib_loader][DEBUG] Loading library: {ライブラリ名}
[2025-12-29 03:59:43,953][snippet.lib_loader][DEBUG] Loaded X code blocks from {ライブラリ名}
[2025-12-29 03:59:43,958][snippet.update_snippet][INFO] [vscode] Snippet file updated: {スニペットjsonパス} 
[2025-12-29 03:59:43,958][snippet.update_snippet][INFO] [cursor] Snippet file updated: {スニペットjsonパス}
```
