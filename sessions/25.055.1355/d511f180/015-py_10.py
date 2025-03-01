import numpy as np

def report_grid_diff(input_grid, output_grid, predicted_grid):
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{output_grid}")
    print(f"Predicted Output:\n{predicted_grid}")    
    diff_expected = np.where(input_grid != output_grid)
    diff_predicted = np.where(input_grid != predicted_grid)
    print(f"Expected Changes at (row, col):\n{list(zip(diff_expected[0], diff_expected[1]))}")
    print(f"Predicted Changes at (row, col):\n{list(zip(diff_predicted[0], diff_predicted[1]))}")
    match = np.array_equal(output_grid,predicted_grid)
    print(f"match: {match}")

#Provided Code
def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Swap top-middle and left-middle pixels.
    output_grid[0, 1], output_grid[1, 0] = output_grid[1, 0], output_grid[0, 1]

    # Swap bottom-middle and bottom-left pixels.
    output_grid[2, 1], output_grid[2, 0] = output_grid[2, 0], output_grid[2, 1]

    return output_grid

# Example Data
examples = [
    {
        "input": np.array([[8, 5, 1], [5, 5, 5], [5, 5, 5]]),
        "output": np.array([[8, 5, 1], [1, 5, 5], [5, 5, 5]])
    },
    {
        "input": np.array([[8, 5, 8], [5, 5, 5], [1, 5, 1]]),
        "output": np.array([[8, 5, 8], [8, 5, 5], [5, 5, 1]])
    },
    {
        "input": np.array([[8, 5, 5], [5, 5, 5], [5, 1, 5]]),
        "output": np.array([[8, 5, 5], [5, 5, 5], [1, 5, 5]])
    },
    {
        "input": np.array([[8, 1, 8], [8, 1, 5], [1, 1, 1]]),
        "output": np.array([[8, 1, 8], [1, 8, 5], [5, 1, 1]])
    }
]
for i, example in enumerate(examples):
    print(f"--- Example {i} ---")
    predicted_grid = transform(example["input"])    
    report_grid_diff(example["input"], example["output"], predicted_grid)
