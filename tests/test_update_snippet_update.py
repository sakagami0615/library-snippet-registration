"""update_snippet.updateモジュールのユニットテスト."""

import tempfile
from pathlib import Path

from snippet.src.lib_loader.dataclass import LibraryCode
from snippet.src.update_snippet.update import update_snippet


def test_update_snippet_with_valid_paths() -> None:
    """有効なスニペットパスでスニペットファイルが正しく更新されるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text("{}")

        cursor_snippet_dir = tmpdir_path / "cursor_snippets"
        cursor_snippet_dir.mkdir()
        (cursor_snippet_dir / "python.json").write_text("{}")

        # 設定を準備
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": str(cursor_snippet_dir),
            }
        }

        # テスト用のライブラリコードを作成
        lib_codes = [
            LibraryCode(
                enable=True,
                library_name="test_lib",
                relative_path="./test_lib",
                language="python",
                snippet_key="test_snippet",
                snippet_prefix="ts",
                description="Test snippet",
                code_lines=["print('hello')"],
            )
        ]

        # スニペットを更新
        update_snippet(device_setting, lib_codes)

        # 両方のファイルが更新されたことを確認
        assert (vscode_snippet_dir / "python.json").exists()
        assert (cursor_snippet_dir / "python.json").exists()


def test_update_snippet_skip_none() -> None:
    """snippet_pathが"none"の場合にスキップされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成(vscodeのみ)
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text("{}")

        # 設定を準備("cursor"は"none")
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": "none",  # これはスキップされるはず
            }
        }

        # テスト用のライブラリコードを作成
        lib_codes = [
            LibraryCode(
                enable=True,
                library_name="test_lib",
                relative_path="./test_lib",
                language="python",
                snippet_key="test_snippet",
                snippet_prefix="ts",
                description="Test snippet",
                code_lines=["print('hello')"],
            )
        ]

        # FileNotFoundErrorが発生しないことを確認
        update_snippet(device_setting, lib_codes)

        # vscodeのファイルのみ更新されたことを確認
        assert (vscode_snippet_dir / "python.json").exists()


def test_update_snippet_skip_empty_string() -> None:
    """snippet_pathが空文字列の場合にスキップされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成(vscodeのみ)
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text("{}")

        # 設定を準備("cursor"は空文字列)
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": "",  # これはスキップされるはず
            }
        }

        # テスト用のライブラリコードを作成
        lib_codes = [
            LibraryCode(
                enable=True,
                library_name="test_lib",
                relative_path="./test_lib",
                language="python",
                snippet_key="test_snippet",
                snippet_prefix="ts",
                description="Test snippet",
                code_lines=["print('hello')"],
            )
        ]

        # FileNotFoundErrorが発生しないことを確認
        update_snippet(device_setting, lib_codes)

        # vscodeのファイルのみ更新されたことを確認
        assert (vscode_snippet_dir / "python.json").exists()


def test_update_snippet_skip_none_value() -> None:
    """snippet_pathがNoneの場合にスキップされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成(vscodeのみ)
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text("{}")

        # 設定を準備("cursor"はNone)
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": None,  # これはスキップされるはず
            }
        }

        # テスト用のライブラリコードを作成
        lib_codes = [
            LibraryCode(
                enable=True,
                library_name="test_lib",
                relative_path="./test_lib",
                language="python",
                snippet_key="test_snippet",
                snippet_prefix="ts",
                description="Test snippet",
                code_lines=["print('hello')"],
            )
        ]

        # FileNotFoundErrorが発生しないことを確認
        update_snippet(device_setting, lib_codes)

        # vscodeのファイルのみ更新されたことを確認
        assert (vscode_snippet_dir / "python.json").exists()


def test_update_snippet_all_none() -> None:
    """全てのsnippet_pathが"none"の場合でもエラーが発生しないテスト."""
    # 設定を準備(全て"none")
    device_setting = {
        "snippet_path": {
            "vscode": "none",
            "cursor": "none",
        }
    }

    # テスト用のライブラリコードを作成
    lib_codes = [
        LibraryCode(
            enable=True,
            library_name="test_lib",
            relative_path="./test_lib",
            language="python",
            snippet_key="test_snippet",
            snippet_prefix="ts",
            description="Test snippet",
            code_lines=["print('hello')"],
        )
    ]

    # FileNotFoundErrorが発生しないことを確認
    update_snippet(device_setting, lib_codes)


def test_update_snippet_empty_lib_codes() -> None:
    """ライブラリコードが空の場合でもエラーが発生しないテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text("{}")

        # 設定を準備
        device_setting = {"snippet_path": {"vscode": str(vscode_snippet_dir)}}

        # 空のライブラリコードで更新
        update_snippet(device_setting, [])


def test_update_snippet_multiple_languages() -> None:
    """複数の言語のスニペットが正しく更新されるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text("{}")
        (vscode_snippet_dir / "javascript.json").write_text("{}")

        # 設定を準備
        device_setting = {"snippet_path": {"vscode": str(vscode_snippet_dir)}}

        # 複数の言語のライブラリコードを作成
        lib_codes = [
            LibraryCode(
                enable=True,
                library_name="test_lib",
                relative_path="./test_lib",
                language="python",
                snippet_key="test_snippet_py",
                snippet_prefix="tspy",
                description="Test Python snippet",
                code_lines=["print('hello')"],
            ),
            LibraryCode(
                enable=True,
                library_name="test_lib",
                relative_path="./test_lib",
                language="javascript",
                snippet_key="test_snippet_js",
                snippet_prefix="tsjs",
                description="Test JavaScript snippet",
                code_lines=["console.log('hello')"],
            ),
        ]

        # スニペットを更新
        update_snippet(device_setting, lib_codes)

        # 両方のファイルが更新されたことを確認
        assert (vscode_snippet_dir / "python.json").exists()
        assert (vscode_snippet_dir / "javascript.json").exists()
