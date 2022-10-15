def split_list(input_list, n) -> list:
    """
    Takes a list and splits it into smaller lists of n elements each.
    :param input_list: any list of items
    :param n: max elements each list should have
    :return:
    """
    n = max(1, n)
    return [input_list[i:i + n] for i in range(0, len(input_list), n)]
