import numpy as np

def show_grid(grid, title="Grid"):
    print(f"\n--- {title} ---")
    print(grid)

def count_differences(grid1, grid2):
    if grid1.shape != grid2.shape:
        return -1 # Indicate shape mismatch

    diff = grid1 != grid2
    return np.sum(diff)

# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0],
        ]),
        "test_output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0],
        ]),

    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
        ]),
        "test_output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
        ]),
    },
    {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 2],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 2],
        ]),
        "test_output": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 2, 2],
        ]),
    },
        {
        "input": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2],
        ]),
         "test_output": np.array([
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2],
        ]),
    },
        {
        "input": np.array([
            [0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
        ]),
        "output": np.array([
            [0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
        ]),
        "test_output": np.array([
            [0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
        ]),
    },
]

for i, example in enumerate(examples):
    input_grid = example["input"]
    output_grid = example["output"]
    test_output_grid = example["test_output"]

    show_grid(input_grid, f"Example {i+1} - Input")
    show_grid(output_grid, f"Example {i+1} - Expected Output")
    show_grid(test_output_grid, f"Example {i+1} - Test Output")

    diff_count = count_differences(output_grid, test_output_grid)
    print(f"Differences between Expected and Test Output: {diff_count}")