def compare_grids(expected, actual):
    """Compares two grids and returns a report of discrepancies."""
    expected = np.array(expected)
    actual = np.array(actual)
    if expected.shape != actual.shape:
        return "Shapes differ: Expected {}, Actual {}".format(expected.shape, actual.shape)

    diff = expected != actual
    num_diff = np.sum(diff)
    diff_indices = np.where(diff)
    diff_report = []
    for i in range(num_diff):
        row = diff_indices[0][i]
        col = diff_indices[1][i]
        diff_report.append(
            "({}, {}): Expected {}, Actual {}".format(
                row, col, expected[row, col], actual[row, col]
            )
        )

    return {
        "num_diff": num_diff,
        "diff_report": diff_report,
    }