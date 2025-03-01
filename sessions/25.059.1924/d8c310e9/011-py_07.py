import numpy as np

def report_diff(expected, actual):
    if expected.shape != actual.shape:
        return f"Shape mismatch: Expected {expected.shape}, Actual {actual.shape}"

    diff = expected != actual
    if not np.any(diff):
        return "No differences found."

    diff_indices = np.where(diff)
    report = "Differences found at:\n"
    for i in range(len(diff_indices[0])):
        row, col = diff_indices[0][i], diff_indices[1][i]
        expected_val = expected[row, col]
        actual_val = actual[row, col]
        report += f"  ({row}, {col}): Expected {expected_val}, Actual {actual_val}\n"
    return report

# Example usage with dummy data (replace with actual results):
task_examples = [
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 2, 0, 0, 2, 0, 0],
                           [0, 0, 2, 0, 0, 2, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 0, 0, 2, 0, 0],
                            [0, 0, 2, 0, 0, 2, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1]])
    },
        {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 0, 2, 0, 0],
                           [0, 2, 0, 0, 0, 2, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [1, 1, 1, 1, 1, 1, 1, 1]])
    },
        {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 2, 2, 0, 0, 0],
                           [0, 0, 0, 2, 2, 0, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 2, 2, 0, 0, 0],
                            [0, 0, 0, 2, 2, 0, 0, 0],
                            [1, 1, 1, 1, 1, 1, 1, 1]])
    },
]

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Copy the last row (already done during initialization)

    # Iterate through the grid to find and extend red blocks
    for r in range(rows -1):
        for c in range(cols):
            if input_grid[r][c] == 2:
                # Copy existing red blocks (already in place due to copy)

                # Extend red blocks to the right
                if c + 2 < cols :
                    output_grid[r, c + 2*4] = 2
                    if input_grid[r+1,c] == 2: # make sure to copy it if and only if it is two long.
                        output_grid[r+1,c+2*4] = 2


    return output_grid

for i, ex in enumerate(task_examples):
    input_grid = ex['input']
    expected_output = ex['output']
    actual_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(report_diff(expected_output, actual_output))
