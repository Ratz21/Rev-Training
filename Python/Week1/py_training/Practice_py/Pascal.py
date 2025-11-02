def pascals_triangle(n):
    """
    Return 'n' rows of Pascal's triangle as a list of lists.
    Example for n=4: [[1], [1,1], [1,2,1], [1,3,3,1]]
    """
    if n <= 0:
        return []

    triangle = [[1]]  # row 0

    for row_index in range(1, n):
        prev = triangle[-1]
        # Start each row with 1
        row = [1]
        # Each inner element is sum of two above neighbors
        for j in range(1, len(prev)):
            row.append(prev[j-1] + prev[j])
        # End the row with 1
        row.append(1)
        triangle.append(row)

    return triangle


# Example
if __name__ == "__main__":
    print(pascals_triangle(5))


