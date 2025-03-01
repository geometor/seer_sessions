def grid_report(grid):
    """returns a report on the grid as a string"""
    import numpy as np
    grid_array = np.array(grid)
    rows, cols = grid_array.shape
    unique_values = np.unique(grid_array)
    report_str = (
        f"- Dimensions: {rows}x{cols}\n"
        f"- Unique values: {unique_values}"
    )
    return report_str

task = {
    "train": [
        {
            "input": [[1, 1, 1, 1, 8, 1], [1, 1, 1, 1, 8, 1], [1, 1, 1, 1, 8, 1], [1, 1, 1, 1, 8, 1]],
            "output": [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
        },
        {
            "input": [[1, 1, 1, 8, 1, 1, 1], [1, 1, 1, 8, 1, 1, 1], [1, 1, 1, 8, 1, 1, 1]],
            "output": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        },
        {
            "input": [[1, 1, 8, 1, 1, 1, 8, 1, 1], [1, 1, 8, 1, 1, 1, 8, 1, 1]],
            "output": [[1, 1], [1, 1]],
        },
        {
            "input": [[1, 8, 1, 1, 1, 1], [1, 8, 1, 1, 1, 1], [1, 8, 1, 1, 1, 1], [1, 8, 1, 1, 1, 1], [1, 8, 1, 1, 1, 1]],
            "output": [[1], [1], [1], [1], [1]],
        },
        {
            "input": [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [8, 8, 8, 8, 8, 8], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
            "output": [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
        },
    ]
}

for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    print("Input:")
    print(grid_report(example["input"]))
    print("Output:")
    print(grid_report(example["output"]))
    print("-" * 20)
