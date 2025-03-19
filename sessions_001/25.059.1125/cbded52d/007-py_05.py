import numpy as np

def analyze_changes(input_grid, output_grid):
    """Analyzes the differences between input and output grids."""
    changes = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != output_grid[r, c]:
                changes.append({
                    "row": r,
                    "col": c,
                    "original_color": int(input_grid[r, c]),
                    "new_color": int(output_grid[r, c]),
                })
    return changes

# Example Usage (assuming train_in, train_out are defined for each example)
task_data = [
    {
        "train_in": np.array([
            [5, 0, 5, 1, 3, 5, 0, 5],
            [0, 0, 0, 1, 0, 0, 5, 5],
            [5, 5, 0, 1, 0, 5, 5, 0],
            [0, 0, 5, 1, 5, 5, 0, 0],
            [5, 0, 0, 1, 0, 0, 0, 5],
            [5, 5, 5, 1, 3, 0, 5, 5],
            [0, 5, 5, 1, 0, 5, 5, 0],
            [0, 0, 0, 1, 0, 0, 0, 0]
        ]),
        "train_out": np.array([
            [5, 0, 5, 3, 3, 5, 0, 5],
            [0, 0, 0, 0, 0, 0, 5, 5],
            [5, 5, 0, 0, 0, 5, 5, 0],
            [0, 0, 5, 5, 5, 5, 0, 0],
            [5, 0, 0, 0, 0, 0, 0, 5],
            [5, 5, 5, 3, 3, 0, 5, 5],
            [0, 5, 5, 0, 0, 5, 5, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
    },
        {
        "train_in": np.array([
            [0, 7, 7, 7, 7, 7, 0, 7],
            [7, 0, 7, 0, 0, 0, 7, 0],
            [7, 7, 0, 7, 7, 7, 0, 0],
            [7, 0, 7, 0, 7, 0, 7, 7],
            [7, 0, 0, 7, 0, 0, 0, 7],
            [0, 7, 7, 0, 7, 7, 7, 0],
            [0, 0, 0, 0, 0, 7, 0, 7],
            [7, 7, 0, 0, 7, 7, 7, 7]
        ]),
        "train_out": np.array([
            [0, 7, 7, 7, 7, 7, 0, 7],
            [7, 0, 7, 0, 0, 0, 7, 0],
            [7, 7, 0, 7, 7, 7, 0, 0],
            [7, 0, 7, 0, 7, 0, 7, 7],
            [7, 0, 0, 7, 0, 0, 0, 7],
            [0, 7, 7, 7, 7, 7, 7, 0],
            [0, 0, 0, 0, 0, 7, 0, 7],
            [7, 7, 0, 0, 7, 7, 7, 7]
        ])
    },
    {
        "train_in": np.array([
            [0, 0, 0, 2, 0, 0, 0, 2],
            [0, 0, 0, 5, 0, 0, 2, 0],
            [0, 0, 0, 2, 0, 2, 0, 0],
            [0, 0, 0, 5, 2, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0, 0]
        ]),
        "train_out": np.array([
            [0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
    }
]

for i, example in enumerate(task_data):
    changes = analyze_changes(example["train_in"], example["train_out"])
    print(f"Example {i+1} Changes:")
    for change in changes:
        print(change)
    print("-" * 20)