def check_library_code_block(lines: list[str], code_block_begin: str, code_block_end: str) -> bool:
    """ライブラリコードブロックの開始・終了マークが正しく配置されているかチェックする

    コードブロックの開始マークと終了マークが適切にネストされているかを検証します。
    不正なネストや順序の誤りを検出します。

    Args:
        lines (list[str]): チェック対象のコード行のリスト
        code_block_begin (str): コードブロック開始マーク (ex: "lib:begin")
        code_block_end (str): コードブロック終了マーク (ex: "lib:end")

    Returns:
        bool: コードブロックが正しく配置されている場合True、それ以外はFalse

    Note:
        - カウンタが負の値になる場合: 終了マークが開始マークより先に出現
        - カウンタが1を超える場合: コードブロックが入れ子になっている
        - 最終的にカウンタが0でない場合: 開始と終了のペアが一致しない
    """
    counter = 0

    for line in lines:
        if code_block_begin in line:
            counter += 1
        elif code_block_end in line:
            counter -= 1

        if counter < 0 or counter > 1:
            return False

    return counter == 0


def check_library_code_prefix(lines: list[str], prefix_list: list[str]) -> bool:
    """ライブラリコードブロックに必須プレフィックスがすべて正確に1回ずつ含まれているかチェックする.

    スニペット登録に必要なメタデータ (snippet_key、snippet_prefix、description) の
    プレフィックスがコードブロック内にそれぞれ1回ずつ存在することを検証します。

    Args:
        lines (list[str]): チェック対象のコード行のリスト
        prefix_list (list[str]): 必須プレフィックスのリスト
            (ex: ["[snippet_key]", "[snippet_prefix]", "[description]"])

    Returns:
        bool: すべてのプレフィックスがちょうど1回ずつ含まれている場合True、
              それ以外 (欠けている、または重複している) の場合False

    Note:
        - すべてのプレフィックスが存在する必要があります (AND条件)
        - 各プレフィックスはちょうど1回出現する必要があります (0回や2回以上はNG)
        - プレフィックスが行内のどこに存在してもチェックは成功します
    """
    result = dict.fromkeys(prefix_list, 0)
    for line in lines:
        for prefix in prefix_list:
            if prefix in line:
                result[prefix] += 1
    return all(v == 1 for v in result.values())
