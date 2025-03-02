def grid_report(grid, name="Grid"):
    report = f"{name}:\n"
    report += f"  Shape: {grid.shape}\n"
    report += f"  Unique Values: {np.unique(grid)}\n"

    # count of each value
    for value in np.unique(grid):
        count = np.count_nonzero(grid == value)
        report += f"  Count of {value}: {count}\n"

    return report

# Load the task examples
task_data = {
    "train": [
        {
            "input": np.array([[9, 9, 9, 9, 9],
                               [9, 9, 9, 9, 9],
                               [1, 1, 1, 1, 1],
                               [0, 0, 0, 0, 0]]),
            "output": np.array([[2, 2, 2, 2, 2],
                                [0, 0, 0, 0, 0]])
        },
        {
            "input": np.array([[9, 9, 9, 9, 9],
                               [1, 1, 1, 1, 1],
                               [9, 9, 9, 9, 9],
                               [0, 0, 0, 0, 0]]),
            "output": np.array([[2, 2, 2, 2, 2],
                                [2, 2, 2, 2, 2]])
        },
        {
            "input": np.array([[0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0],
                               [1, 1, 1, 1, 1],
                               [1, 1, 1, 1, 1]]),
            "output": np.array([[0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0]])
        }

    ],
    "test": [
        {
            "input": np.array([[9, 9, 9],
                               [9, 9, 9],
                               [1, 1, 1],
                               [0, 0, 0]]),
            "output": np.array([[2, 2, 2],
                                [0, 0, 0]])
        }
    ]
}

import numpy as np

reports = []
for i, example in enumerate(task_data["train"]):
    input_report = grid_report(example["input"], name=f"Train Input {i}")
    output_report = grid_report(example["output"], name=f"Train Output {i}")

    # calculate predicted
    predicted_output = transform(example["input"])
    predicted_report = grid_report(predicted_output, name=f"Predicted {i}")
    reports.append(f"{input_report}\n{output_report}\n{predicted_report}")

print("\n---\n".join(reports))
