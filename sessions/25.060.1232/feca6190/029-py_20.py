def get_grid_info(grid):
    """Gets information about non-zero elements in a grid."""
    non_zero_elements = []
    for value in np.unique(grid):
        if value != 0:
            count = np.sum(grid == value)
            non_zero_elements.append((value, count))
    return {
        "shape": grid.shape,
        "non_zero_elements": non_zero_elements,
    }

import numpy as np
task_data = {  # replace with actual training examples
    "train": [
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 1, 0]]),
            "output": np.array([[1]]),
        },
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 8, 0, 0]]),
            "output": np.array([[8, 0], [0, 8]]),
        },
        {
            "input": np.array([[0, 0, 0, 0, 0, 3, 0, 0, 0, 0]]),
            "output": np.array([[3, 0, 0, 0, 0], [0, 3, 0, 0, 0], [0, 0, 3, 0, 0], [0, 0, 0, 3, 0], [0, 0, 0, 0, 3]]),
        },
        {
            "input": np.array([[0, 0, 0, 7, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[7, 0, 0, 0], [0, 7, 0, 0], [0, 0, 7, 0], [0, 0, 0, 7]]),
        },
        {
            "input": np.array([[0, 0, 5, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[5, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 5]]),
        },
    ]
}
results = {}
for i, example in enumerate(task_data["train"]):
    results[f"example_{i}"] = {
        "input": get_grid_info(example["input"]),
        "output": get_grid_info(example["output"]),
    }
print(results)
