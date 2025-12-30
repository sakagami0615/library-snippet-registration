"""update_snippet.backupモジュールのユニットテスト."""

import tempfile
from pathlib import Path

from snippet.src.update_snippet.backup import backup_snippet_files


def test_backup_snippet_files_with_valid_paths() -> None:
    """有効なスニペットパスでバックアップが正しく作成されるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text('{"test": "data"}')

        cursor_snippet_dir = tmpdir_path / "cursor_snippets"
        cursor_snippet_dir.mkdir()
        (cursor_snippet_dir / "javascript.json").write_text('{"test": "data2"}')

        # ワークスペースディレクトリを作成
        workspace_dir = tmpdir_path / "workspace"
        workspace_dir.mkdir()

        # 設定を準備
        tool_setting = {"backup_snippet_dirpath": ".backup_snippet"}
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": str(cursor_snippet_dir),
            }
        }

        # バックアップディレクトリのパスを変更するため、一時的にモジュールの設定を変更
        import snippet.src.update_snippet.backup as backup_module

        original_workspace = backup_module.WORKSPACE_DIRPATH
        try:
            backup_module.WORKSPACE_DIRPATH = workspace_dir
            backup_snippet_files(tool_setting, device_setting)

            # バックアップが作成されたことを確認
            backup_dir = workspace_dir / ".backup_snippet"
            assert backup_dir.exists()
            assert (backup_dir / "vscode" / "python.json").exists()
            assert (backup_dir / "cursor" / "javascript.json").exists()

        finally:
            backup_module.WORKSPACE_DIRPATH = original_workspace


def test_backup_snippet_files_skip_none() -> None:
    """snippet_pathが"none"の場合にスキップされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成(vscodeのみ)
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text('{"test": "data"}')

        # ワークスペースディレクトリを作成
        workspace_dir = tmpdir_path / "workspace"
        workspace_dir.mkdir()

        # 設定を準備("cursor"は"none")
        tool_setting = {"backup_snippet_dirpath": ".backup_snippet"}
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": "none",  # これはスキップされるはず
            }
        }

        # バックアップディレクトリのパスを変更するため、一時的にモジュールの設定を変更
        import snippet.src.update_snippet.backup as backup_module

        original_workspace = backup_module.WORKSPACE_DIRPATH
        try:
            backup_module.WORKSPACE_DIRPATH = workspace_dir

            # FileNotFoundErrorが発生しないことを確認
            backup_snippet_files(tool_setting, device_setting)

            # バックアップが作成されたことを確認(vscodeのみ)
            backup_dir = workspace_dir / ".backup_snippet"
            assert backup_dir.exists()
            assert (backup_dir / "vscode" / "python.json").exists()
            # cursorのバックアップは作成されていないことを確認
            assert not (backup_dir / "cursor").exists()

        finally:
            backup_module.WORKSPACE_DIRPATH = original_workspace


def test_backup_snippet_files_skip_empty_string() -> None:
    """snippet_pathが空文字列の場合にスキップされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成(vscodeのみ)
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text('{"test": "data"}')

        # ワークスペースディレクトリを作成
        workspace_dir = tmpdir_path / "workspace"
        workspace_dir.mkdir()

        # 設定を準備("cursor"は空文字列)
        tool_setting = {"backup_snippet_dirpath": ".backup_snippet"}
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": "",  # これはスキップされるはず
            }
        }

        # バックアップディレクトリのパスを変更するため、一時的にモジュールの設定を変更
        import snippet.src.update_snippet.backup as backup_module

        original_workspace = backup_module.WORKSPACE_DIRPATH
        try:
            backup_module.WORKSPACE_DIRPATH = workspace_dir

            # FileNotFoundErrorが発生しないことを確認
            backup_snippet_files(tool_setting, device_setting)

            # バックアップが作成されたことを確認(vscodeのみ)
            backup_dir = workspace_dir / ".backup_snippet"
            assert backup_dir.exists()
            assert (backup_dir / "vscode" / "python.json").exists()
            # cursorのバックアップは作成されていないことを確認
            assert not (backup_dir / "cursor").exists()

        finally:
            backup_module.WORKSPACE_DIRPATH = original_workspace


def test_backup_snippet_files_skip_none_value() -> None:
    """snippet_pathがNoneの場合にスキップされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成(vscodeのみ)
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text('{"test": "data"}')

        # ワークスペースディレクトリを作成
        workspace_dir = tmpdir_path / "workspace"
        workspace_dir.mkdir()

        # 設定を準備("cursor"はNone)
        tool_setting = {"backup_snippet_dirpath": ".backup_snippet"}
        device_setting = {
            "snippet_path": {
                "vscode": str(vscode_snippet_dir),
                "cursor": None,  # これはスキップされるはず
            }
        }

        # バックアップディレクトリのパスを変更するため、一時的にモジュールの設定を変更
        import snippet.src.update_snippet.backup as backup_module

        original_workspace = backup_module.WORKSPACE_DIRPATH
        try:
            backup_module.WORKSPACE_DIRPATH = workspace_dir

            # FileNotFoundErrorが発生しないことを確認
            backup_snippet_files(tool_setting, device_setting)

            # バックアップが作成されたことを確認(vscodeのみ)
            backup_dir = workspace_dir / ".backup_snippet"
            assert backup_dir.exists()
            assert (backup_dir / "vscode" / "python.json").exists()
            # cursorのバックアップは作成されていないことを確認
            assert not (backup_dir / "cursor").exists()

        finally:
            backup_module.WORKSPACE_DIRPATH = original_workspace


def test_backup_snippet_files_all_none() -> None:
    """全てのsnippet_pathが"none"の場合でもエラーが発生しないテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # ワークスペースディレクトリを作成
        workspace_dir = tmpdir_path / "workspace"
        workspace_dir.mkdir()

        # 設定を準備(全て"none")
        tool_setting = {"backup_snippet_dirpath": ".backup_snippet"}
        device_setting = {
            "snippet_path": {
                "vscode": "none",
                "cursor": "none",
            }
        }

        # バックアップディレクトリのパスを変更するため、一時的にモジュールの設定を変更
        import snippet.src.update_snippet.backup as backup_module

        original_workspace = backup_module.WORKSPACE_DIRPATH
        try:
            backup_module.WORKSPACE_DIRPATH = workspace_dir

            # FileNotFoundErrorが発生しないことを確認
            backup_snippet_files(tool_setting, device_setting)

            # バックアップディレクトリは作成されるが、中身は空
            backup_dir = workspace_dir / ".backup_snippet"
            assert backup_dir.exists()
            # ディレクトリが空であることを確認
            assert len(list(backup_dir.iterdir())) == 0

        finally:
            backup_module.WORKSPACE_DIRPATH = original_workspace


def test_backup_snippet_files_overwrites_existing_backup() -> None:
    """既存のバックアップが上書きされるテスト."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # テスト用のスニペットディレクトリを作成
        vscode_snippet_dir = tmpdir_path / "vscode_snippets"
        vscode_snippet_dir.mkdir()
        (vscode_snippet_dir / "python.json").write_text('{"test": "new_data"}')

        # ワークスペースディレクトリを作成
        workspace_dir = tmpdir_path / "workspace"
        workspace_dir.mkdir()

        # 古いバックアップを作成
        old_backup_dir = workspace_dir / ".backup_snippet" / "vscode"
        old_backup_dir.mkdir(parents=True)
        (old_backup_dir / "python.json").write_text('{"test": "old_data"}')

        # 設定を準備
        tool_setting = {"backup_snippet_dirpath": ".backup_snippet"}
        device_setting = {"snippet_path": {"vscode": str(vscode_snippet_dir)}}

        # バックアップディレクトリのパスを変更するため、一時的にモジュールの設定を変更
        import snippet.src.update_snippet.backup as backup_module

        original_workspace = backup_module.WORKSPACE_DIRPATH
        try:
            backup_module.WORKSPACE_DIRPATH = workspace_dir
            backup_snippet_files(tool_setting, device_setting)

            # 新しいバックアップが作成されたことを確認
            backup_file = workspace_dir / ".backup_snippet" / "vscode" / "python.json"
            assert backup_file.exists()
            content = backup_file.read_text()
            assert "new_data" in content
            assert "old_data" not in content

        finally:
            backup_module.WORKSPACE_DIRPATH = original_workspace
