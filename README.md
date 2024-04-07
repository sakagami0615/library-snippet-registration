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

## generate config

以下のように実行することで2つのパラメータファイルが生成される。自身の環境に合わせて中身を記載する。

- library_mark_template.yaml
- snippet_config_template.yaml

```bash
python snippet_tool.py prepare
```

## run resist snippet

```bash
python snippet_tool.py resist -c ./library_mark_template.yaml
```
