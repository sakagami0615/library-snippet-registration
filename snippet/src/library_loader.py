from dataclasses import dataclass
from dataclasses import field
from logging import getLogger
from pathlib import Path

from snippet.src.file_helper import BlockInfo
from snippet.src.file_helper import FileHelper
from snippet.src.string_helper import StringHelper

logger = getLogger("snippet").getChild("library_loader")


@dataclass
class CodeInfo:
    """ライブラリコードの情報格納データクラス

    Attributes:
        script_path (str): スクリプトパス
        snippet_key (str): スニペットに登録するキー情報
        snippet_prefix (str): スニペットに登録するスニペット情報
        description (str): スニペットに登録するDesc情報
        code (list): ライブラリコード
    """

    script_path: str
    snippet_key: str
    snippet_prefix: str
    description: str
    code: list = field(default_factory=list)

    def __eq__(self, other) -> bool:  # type: ignore
        return (
            (self.script_path in other.script_path)
            or (other.script_path in self.script_path)
            and self.snippet_key == other.snippet_key
            and self.snippet_prefix == other.snippet_prefix
            and self.description == other.description
            and self.code == other.code
        )


class LibraryLoader:
    """ライブラリ読み込みクラス

    Args:
        mark_path (Path): ライブラリコード関連のマークを記載した設定ファイル
        folder_path (Path): ライブラリフォルダパス
        extensions (list[str], optional): ライブラリスクリプトの拡張子。(Defaults to [])
        excludes (list[str], optional): ライブラリスクリプト探索時、無視する文字列。(Defaults to [])
    """

    def __init__(
        self,
        mark_path: Path,
        folder_path: Path,
        extensions: list[str] = [],
        excludes: list[str] = [],
    ):
        self._code_paths: list[Path] = []
        self._folder_path = folder_path
        self._extensions = extensions
        self._excludes = excludes
        self._lib_mark = FileHelper.read_yaml(mark_path)
        self._search_lib_codes()

    def _search_lib_codes(self) -> None:
        """対象となるライブラリスクリプトを取得する"""
        self._code_paths = []

        def recursion(cur_path: Path) -> None:
            for nxt_path in cur_path.iterdir():
                if nxt_path.is_dir():
                    if not StringHelper.is_include_targets(str(nxt_path), self._extensions):
                        recursion(nxt_path)
                else:
                    if (StringHelper.is_include_targets(str(nxt_path), self._extensions)) and (
                        not StringHelper.is_include_targets(str(nxt_path), self._excludes)
                    ):
                        self._code_paths.append(Path(nxt_path))

        recursion(self._folder_path)
        self._code_paths.sort()

    def _block_to_code_info(self, script_path: str, text_block: BlockInfo) -> CodeInfo:
        """ライブラリスクリプトから取得したブロック情報をライブラリ情報に変換する

        Args:
            script_path (str): スクリプトパス
            text_block (BlockInfo): ブロック情報

        Returns:
            CodeInfo: ライブラリ情報
        """
        snippet_key, snippet_prefix, description = "", "", ""
        code = []
        for line in text_block.lines:
            if snippet_key and snippet_prefix and description:
                code.append(line)
            else:
                key = self._lib_mark["snippet_key"]
                prefix = self._lib_mark["snippet_prefix"]
                desc = self._lib_mark["description"]

                if StringHelper.is_include_targets(line, [key]):
                    snippet_key = StringHelper.get_suffix(line, key)
                elif StringHelper.is_include_targets(line, [prefix]):
                    snippet_prefix = StringHelper.get_suffix(line, prefix)
                elif StringHelper.is_include_targets(line, [desc]):
                    description = StringHelper.get_suffix(line, desc)

        return CodeInfo(script_path, snippet_key, snippet_prefix, description, code)

    def _check_duplicate_code_info(
        self, store_code_infos: list[CodeInfo], src_code_info: CodeInfo, code_row: int
    ) -> bool:
        """ライブラリ情報に重複がないかをチェックする

        Args:
            store_code_infos (list[CodeInfo]): ストアしているライブラリ情報
            src_code_info (CodeInfo): チェック対象のライブラリ情報
            code_row (int): ライブラリの行番号

        Returns:
            bool: 重複があるかどうか(重複がある場合はTrue)
        """
        for store_code_info in store_code_infos:
            if src_code_info.snippet_key == store_code_info.snippet_key:
                logger.warning(
                    (
                        f"{src_code_info.script_path} L{code_row} のライブラリコードの"
                        f"snippet_key({src_code_info.snippet_key})が重複しているため、"
                        "スニペットの登録からは除外します (library syntax)"
                    )
                )
                return True
            if src_code_info.snippet_prefix == store_code_info.snippet_prefix:
                logger.warning(
                    (
                        f"{src_code_info.script_path} L{code_row} のライブラリコードの"
                        f"snippet_prefix({src_code_info.snippet_prefix})が重複しているため、"
                        "スニペットの登録からは除外します (library syntax)"
                    )
                )
                return True
        return False

    def _check_syntax_error_code_info(self, code_info: CodeInfo, code_row: int) -> bool:
        """ライブラリ情報の構文エラーをチェックする

        Args:
            code_info (CodeInfo): ライブラリ情報
            code_row (int): ライブラリの行番号

        Returns:
            bool: 構文エラーがあるかどうか(構文エラーがある場合はTrue)
        """
        result = False
        if not code_info.snippet_key:
            result = True
            logger.warning(
                (
                    f"{code_info.script_path} L{code_row} のライブラリコードには"
                    "snippet_keyが無いため、スニペットの登録からは除外します "
                    "(library syntax)"
                )
            )
        if not code_info.snippet_prefix:
            result = True
            logger.warning(
                (
                    f"{code_info.script_path} L{code_row} のライブラリコードには"
                    "snippet_prefixが無いため、スニペットの登録からは除外します "
                    "(library syntax)"
                )
            )
        return result

    def read_lib_codes(self) -> list[CodeInfo]:
        """ライブラリスクリプトからスニペットに登録するライブラリを読み込む

        Returns:
            list[CodeInfo]: 読み込んだライブラリ情報
        """
        code_infos: list[CodeInfo] = []

        for code_path in self._code_paths:
            text_blocks = FileHelper.read_text_blocks(code_path, self._lib_mark["lib_begin"], self._lib_mark["lib_end"])

            for text_block in text_blocks:
                code_info = self._block_to_code_info(str(code_path), text_block)

                is_syntax_error = self._check_syntax_error_code_info(code_info, text_block.row)
                is_duplicate = self._check_duplicate_code_info(code_infos, code_info, text_block.row)

                if (not is_syntax_error) and (not is_duplicate):
                    code_infos.append(code_info)

        return code_infos
