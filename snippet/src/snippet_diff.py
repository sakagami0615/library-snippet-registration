from logging import getLogger

from snippet.setting import SNIPPET_KEYS

logger = getLogger("snippet").getChild("snippet_diff")


class SnippetDiff:
    """スニペットの差分処理をまとめたクラス"""

    @staticmethod
    def logger_snippet_diff(src_snippet: dict, dst_snippet: dict) -> None:
        """スニペットの差分をロガーで表示

        Args:
            src_snippet (dict): スニペット情報(比較元)
            dst_snippet (dict): スニペット情報(比較先)
        """
        src_keys = set(src_snippet.keys())
        dst_keys = set(dst_snippet.keys())

        common_keys = src_keys & dst_keys
        new_keys = dst_keys - common_keys
        delete_keys = src_keys - common_keys

        for new_key in new_keys:
            logger.info(f"snippet_diff (new): {new_key}")
        for delete_key in delete_keys:
            logger.info(f"snippet_diff (delete): {delete_key}")

        for common_key in common_keys:
            src_item, dst_item = src_snippet[common_key], dst_snippet[common_key]
            change_contents = []
            for snippet_key in SNIPPET_KEYS:
                if src_item[snippet_key] != dst_item[snippet_key]:
                    change_contents.append(snippet_key)
            change_content = "/".join(change_contents)

            if src_item != dst_item:
                logger.info(f"snippet_diff (change - {change_content}): {common_key}")
