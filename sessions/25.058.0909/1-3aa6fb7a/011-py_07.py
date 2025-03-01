import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns the coordinates where they differ.
    """
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    diff_coords = []
    for row in range(grid1.shape[0]):
        for col in range(grid1.shape[1]):
            if grid1[row, col] != grid2[row, col]:
                diff_coords.append((row, col))
    return diff_coords

# Example data (replace with actual data from the task)
# These are placeholders.  I'll use the REAL data in the execution.
examples = [
    {
        "input": np.array([[8, 8, 8, 8, 8], [8, 0, 0, 0, 8], [8, 0, 0, 0, 8], [8, 8, 8, 8, 8]]),
        "output": np.array([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 8], [1, 1, 1, 1, 8]]),
        "test_output": np.array([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 8], [1, 1, 1, 1, 8]]),
    },
    {
        "input": np.array([[8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 8], [8, 8, 8, 0]]),
        "output": np.array([[1, 1, 1, 1], [1, 1, 1, 8], [1, 1, 1, 8], [1, 1, 8, 0]]),
        "test_output": np.array([[1, 1, 1, 1], [1, 8, 8, 8], [1, 8, 8, 8], [1, 8, 8, 0]]),

    },
    {
        "input": np.array([[0, 0, 8, 8, 8, 8], [0, 0, 8, 0, 0, 8], [8, 8, 8, 0, 0, 8], [8, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 8], [8, 8, 8, 8, 8, 8]]),
        "output": np.array([[0, 0, 1, 1, 1, 1], [0, 0, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1], [1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1]]),
        "test_output": np.array([[0, 0, 1, 1, 1, 1], [0, 0, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1], [1, 0, 0, 0, 0, 8], [1, 0, 0, 0, 0, 8], [1, 1, 1, 1, 8, 8]]),
    },
     {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 8, 0, 0, 8, 0], [8, 0, 8, 8, 8, 8, 8, 0],[8, 8, 8, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0],[1, 1, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1]]),
        "test_output": np.array([[1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 1, 1, 0],[1, 1, 1, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8]]),
    }
]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    diffs = compare_grids(example["output"], example["test_output"])
    print(f"  Differences between expected and actual: {diffs}")