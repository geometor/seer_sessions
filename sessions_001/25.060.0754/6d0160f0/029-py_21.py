import numpy as np

def compare_grids(expected, produced):
    """Compares two grids and returns a detailed report."""
    if expected.shape != produced.shape:
        return "Shapes are different"
    diff = expected != produced
    diff_indices = np.where(diff)
    num_diffs = len(diff_indices[0])
    report = {
        "total_differences": num_diffs,
        "different_pixels": [],
    }
    for i in range(num_diffs):
        row = diff_indices[0][i]
        col = diff_indices[1][i]
        report["different_pixels"].append(
            {
                "row": row,
                "col": col,
                "expected": int(expected[row, col]),
                "produced": int(produced[row, col]),
            }
        )
    return report

# Example grids (replace with actual data from the task)
example_pairs = [
    (
        np.array([
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 1, 0, 0, 3, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
        ]),
        np.array([
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 1, 0, 0, 3, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5],
        ]),
    ),
     (
        np.array([
            [5, 5, 5, 5, 5],
            [5, 1, 5, 3, 5],
            [5, 5, 5, 5, 5],
            [5, 0, 5, 0, 5],
            [5, 5, 5, 5, 5]
        ]),
        np.array([
            [5, 5, 5, 5, 5],
            [5, 0, 5, 0, 5],
            [5, 5, 5, 5, 5],
            [5, 1, 5, 3, 5],
            [5, 5, 5, 5, 5],
        ]),
    ),
    (
        np.array([
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 8, 0, 5, 0, 0, 2, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 0, 5, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 0, 5, 0, 4, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            ]),
        np.array([
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 0, 5, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 8, 0, 5, 0, 0, 2, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 0, 0, 0, 5, 0, 0, 0, 0, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
        ]),
    ),
        (
        np.array([
            [5, 5, 5, 5, 5, 5],
            [5, 1, 5, 0, 2, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 0, 5, 0, 0, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 0, 5, 4, 0, 5],
            [5, 5, 5, 5, 5, 5]
            ]),
        np.array([
            [5, 5, 5, 5, 5, 5],
            [5, 0, 5, 0, 0, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 1, 5, 0, 2, 5],
            [5, 5, 5, 5, 5, 5],
            [5, 0, 5, 0, 0, 5],
            [5, 5, 5, 5, 5, 5]
        ]),
    )

]

for i, (input_grid, expected_output) in enumerate(example_pairs):
    produced_output = transform(input_grid)
    comparison = compare_grids(expected_output, produced_output)
    print(f"Example {i+1} Comparison:")
    print(comparison)