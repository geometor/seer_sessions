import numpy as np

def report_changes(input_grid, output_grid):
    changes = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != output_grid[i, j]:
                changes.append(
                    {
                        "row": i,
                        "col": j,
                        "old_color": int(input_grid[i, j]),
                        "new_color": int(output_grid[i, j]),
                    }
                )
    return changes

task = {
    "train": [
        {
            "input": [[5, 0, 5], [0, 0, 5], [0, 5, 5]],
            "output": [[5, 0, 5], [0, 0, 5], [0, 5, 5]],
        },
        {
            "input": [[1, 0, 8], [0, 0, 1], [8, 1, 1]],
            "output": [[1, 0, 8], [0, 0, 8], [8, 8, 8]],
        },
        {
            "input": [[0, 7, 0], [0, 7, 7], [7, 7, 0]],
            "output": [[0, 7, 0], [0, 7, 7], [7, 7, 7]],
        },
        {
            "input": [[6, 6, 0], [0, 0, 0], [6, 0, 6]],
            "output": [[6, 6, 0], [0, 0, 0], [6, 0, 6]],
        },
        {
            "input": [[0, 9, 4], [9, 8, 7], [9, 4, 9]],
            "output": [[0, 9, 4], [9, 8, 4], [9, 4, 4]],
        },
    ],
    "test": [{"input": [[5, 0, 9], [3, 8, 9], [9, 9, 0]], "output": []}],
}

for i, example in enumerate(task["train"]):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted_output = transform(input_grid)  # Using the provided transform function
    changes = report_changes(input_grid, output_grid)
    predicted_changes = report_changes(input_grid, predicted_output)

    print(f"Example {i+1}:")
    print(f"  Expected Changes: {changes}")
    print(f"  Predicted Changes: {predicted_changes}")
    print("-" * 30)
