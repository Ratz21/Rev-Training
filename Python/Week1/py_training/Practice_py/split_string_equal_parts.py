def split_string_strict(s, k):
    """
    Split string s into k equal parts. If len(s) is not divisible by k, raises ValueError.
    Returns a list of k substrings, each of length len(s)//k.
    """
    if k <= 0:
        raise ValueError("k must be positive")
    n = len(s)
    if n % k != 0:
        raise ValueError(f"String length {n} not divisible by {k}")

    part_len = n // k
    return [s[i*part_len:(i+1)*part_len] for i in range(k)]


# Example
split_string_strict("abcdefghijkl", 3) ,['abcd', 'efgh', 'ijkl']
