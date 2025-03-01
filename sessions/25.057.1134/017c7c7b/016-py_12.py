import numpy as np

def describe_grid(grid):
    shape = grid.shape
    colors = np.unique(grid)
    return f"Shape: {shape}, Colors: {colors}"

task_data = {
    "train": [
        {
            "input": [[3, 3, 3], [3, 8, 3], [3, 3, 3]],
            "output": [[3, 3, 3, 3, 3], [3, 8, 3, 8, 3], [3, 3, 3, 3, 3], [3, 8, 3, 8, 3], [3, 3, 3, 3, 3]],
        },
        {
            "input": [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
            "output": [[1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0], [1, 0, 1, 0, 1]],
        },
        {
            "input": [[8, 0, 0], [0, 1, 0], [5, 0, 6]],
            "output": [[8, 0, 0, 0, 8], [0, 1, 0, 1, 0], [5, 0, 6, 0, 5], [0, 1, 0, 1, 0], [8, 0, 0, 0, 8]],
        },
        {
             "input": [[7, 0, 7, 7], [7, 0, 8, 0], [7, 2, 7, 0], [7, 7, 7, 7]],
             "output": [[7, 0, 7, 7, 0, 7], [7, 0, 8, 0, 0, 7], [7, 2, 7, 0, 2, 7], [7, 7, 7, 7, 0, 7], [7, 0, 8, 0, 0, 7], [7, 2, 7, 0, 2, 7]]
        }
    ]
}

for i, example in enumerate(task_data['train']):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    print(f"Example {i+1}:")
    print(f"  Input: {describe_grid(input_grid)}")
    print(f"  Output: {describe_grid(output_grid)}")

    # Analyze column relationships
    for col_idx in range(input_grid.shape[1]):
        print(f"  Input Column {col_idx}: {input_grid[:, col_idx]}")

    print(f"Output columns 0 to {output_grid.shape[1]-1}:")
    for col_idx in range(output_grid.shape[1]):
        print(f"  Output Column {col_idx}: {output_grid[:, col_idx]}")