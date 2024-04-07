import json
from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from logging import getLogger
from pathlib import Path

import yaml

from snippet.setting import CODE_ENCODING
from snippet.src.string_helper import StringHelper

logger = getLogger("snippet").getChild("file_helper")


@dataclass
class BlockInfo:
    """ライブラリスクリプトから取得したコードブロック情報。

    Attributes:
        row (int): ブロックの先頭業番号
        lines (list[str]): ブロックコード
        enable (bool): 有効なブロックかどうか
    """

    row: int
    lines: list[str] = field(default_factory=list)
    enable: bool = False


class FileHelper:
    """ファイル読み書き処理をまとめたクラス"""

    @staticmethod
    def read_text(file_path: Path) -> list[str]:
        """テキストを読み込む。

        Args:
            file_path (Path): テキストファイルパス

        Returns:
            list[str]: 読み込んだテキスト
        """
        with open(file_path, encoding=CODE_ENCODING) as f:
            lines = [s.rstrip("\n") for s in f.readlines()]
        return lines

    @staticmethod
    def read_json(json_path: Path) -> dict:
        """jsonファイルを読み込む

        Args:
            json_path (Path): jsonファイルパス

        Returns:
            dict: 読み込んだjsonデータ
        """
        if not json_path.exists():
            return defaultdict(str)
        with open(json_path, encoding=CODE_ENCODING) as f:
            json_dict = json.load(f)
        return defaultdict(str, json_dict)

    @staticmethod
    def write_json(json_path: Path, json_dict: dict) -> None:
        """jsonファイルを書き込む

        Args:
            json_path (Path): 書き込み先のjsonファイル
            json_dict (dict): 書き込む辞書データ
        """
        with open(json_path, "w", encoding=CODE_ENCODING) as f:
            json.dump(json_dict, f, indent=2)

    @staticmethod
    def read_yaml(yaml_path: Path) -> dict:
        """yamlデータを読み込む

        Args:
            yaml_path (Path): yamlデータファイル

        Returns:
            dict: 読み込んだyamlデータ
        """
        if not yaml_path.exists():
            return defaultdict(str)
        with open(yaml_path, encoding=CODE_ENCODING) as f:
            yaml_dict = yaml.safe_load(f)
        return defaultdict(str, yaml_dict)

    @staticmethod
    def read_text_blocks(file_path: Path, begin_label: str, end_label: str) -> list[BlockInfo]:
        """ライブラリスクリプトからライブラリコードブロックを取得する

        開始ラベルと終了ラベルの間のコードをライブラリコードブロックとして抽出する。

        Args:
            file_path (Path): ライブラリスクリプトパス
            begin_label (str): ブロック開始ラベル
            end_label (str): ブロック開始ラベル

        Returns:
            list[BlockInfo]: 取得したライブラリコードブロック
        """
        lines = FileHelper.read_text(file_path)

        block_infos: list[BlockInfo] = []
        is_block = False

        for idx, line in enumerate(lines):
            row_number = idx + 1

            if StringHelper.is_include_targets(line, [begin_label]):
                if not is_block:
                    block_infos.append(BlockInfo(row_number))
                    is_block = True
                else:
                    curr_block_row = block_infos[-1].row
                    block_infos[-1] = BlockInfo(row_number)
                    logger.warning(
                        f"{file_path} L{curr_block_row} に対応するブロック終了のマークがありません (library syntax)"
                    )

            elif StringHelper.is_include_targets(line, [end_label]):
                if is_block:
                    is_block = False
                    block_infos[-1].enable = True
                else:
                    logger.warning(
                        f"{file_path} L{row_number} に対応するブロック開始のマークがありません (library syntax)"
                    )

            elif is_block:
                block_infos[-1].lines.append(line)

        # check last block enable
        if block_infos and (not block_infos[-1].enable):
            logger.warning(
                f"{file_path} L{block_infos[-1].row} に対応するブロック終了のマークがありません (library syntax)"
            )

        return block_infos
