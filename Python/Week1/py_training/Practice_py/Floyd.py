def floyds_triangle(rows):
    """
    Return Floyd's triangle as a list of lists for the given number of rows.
    Example for rows=3: [[1], [2, 3], [4, 5, 6]]
    """
    if rows <= 0:
        return []

    result = []
    current = 1
    for r in range(1, rows + 1):
        row = []
        for _ in range(r):
            row.append(current)
            current += 1
        result.append(row)

    return result


# Example
if __name__ == "__main__":
    print(floyds_triangle(5))
