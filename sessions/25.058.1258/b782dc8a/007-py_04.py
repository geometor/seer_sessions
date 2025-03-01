import numpy as np

def analyze_results(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    changed_pixels = np.sum(expected_output != input_grid)
    actual_changed_pixels = np.sum(actual_output != input_grid)

    print(f"Changed Pixels (Expected): {changed_pixels}")
    print(f"Changed Pixels (Actual):   {actual_changed_pixels}")

    diff = expected_output - actual_output
    rows, cols = np.where(diff != 0)

    for r, c in zip(rows, cols):
        print(f"Discrepancy at ({r}, {c}): Expected {expected_output[r, c]}, Actual {actual_output[r, c]}, Input {input_grid[r,c]}")
        print(f"  - Surrounding pixels in input :")
        if r > 0: print(f"      Up   : {input_grid[r-1, c]}")
        if r < input_grid.shape[0] - 1: print(f"      Down : {input_grid[r+1, c]}")
        if c > 0: print(f"      Left : {input_grid[r, c-1]}")
        if c < input_grid.shape[1] - 1: print(f"      Right: {input_grid[r, c+1]}")
        print(f"  - Surrounding pixels in output:")
        if r > 0: print(f"      Up   : {expected_output[r-1, c]}")
        if r < input_grid.shape[0] - 1: print(f"      Down : {expected_output[r+1, c]}")
        if c > 0: print(f"      Left : {expected_output[r, c-1]}")
        if c < input_grid.shape[1] - 1: print(f"      Right: {expected_output[r, c+1]}")


# example usage with the provided data structure:

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 0, 0, 0, 0], [0, 8, 8, 0, 0, 8, 8, 8, 0, 0], [0, 8, 8, 0, 0, 8, 0, 8, 0, 0], [0, 8, 8, 0, 0, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 3, 0, 0, 0, 0], [0, 3, 3, 0, 0, 3, 3, 3, 0, 0], [0, 3, 3, 0, 0, 3, 0, 3, 0, 0], [0, 3, 3, 0, 0, 3, 3, 3, 0, 0], [0, 3, 3, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 0, 0, 0, 0], [0, 8, 8, 1, 1, 8, 8, 8, 0, 0], [0, 8, 8, 1, 1, 8, 0, 8, 0, 0], [0, 8, 8, 1, 1, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2, 0, 0, 0, 0], [0, 2, 2, 1, 1, 2, 2, 2, 0, 0], [0, 2, 2, 1, 1, 2, 0, 2, 0, 0], [0, 2, 2, 1, 1, 2, 2, 2, 0, 0], [0, 2, 2, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 8, 0, 0], [0, 8, 8, 8, 8, 8, 0, 8, 0, 0], [0, 8, 8, 4, 4, 8, 8, 8, 0, 0], [0, 8, 8, 4, 4, 8, 0, 8, 0, 0], [0, 8, 8, 4, 4, 8, 8, 8, 0, 0], [0, 8, 8, 8, 8, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 3, 3, 3, 3, 3, 0, 3, 0, 0], [0, 3, 3, 4, 4, 3, 3, 3, 0, 0], [0, 3, 3, 4, 4, 3, 0, 3, 0, 0], [0, 3, 3, 4, 4, 3, 3, 3, 0, 0], [0, 3, 3, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
    ]
}

for i, example in enumerate(task["train"]):
    print(f"----- Example {i + 1} -----")
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(np.array(input_grid))
    analyze_results(input_grid, expected_output, actual_output)