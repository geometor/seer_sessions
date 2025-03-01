import numpy as np

def analyze_transformation(input_grid, output_grid, predicted_output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_output_grid = np.array(predicted_output_grid)

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(output_grid)
    print("Predicted Output Grid:")
    print(predicted_output_grid)    

    correct = np.array_equal(output_grid, predicted_output_grid)
    print(f"Correct: {correct}")

    diff = output_grid - predicted_output_grid
    print("Difference (Expected - Predicted):")
    print(diff)    

    input_values = np.unique(input_grid)
    output_values = np.unique(output_grid)
    print(f"Unique Input Values: {input_values}")
    print(f"Unique Output Values: {output_values}")

examples = [
    {
        "input": [[2, 2, 8, 8, 2, 8, 6], [0, 0, 0, 0, 0, 0, 0], [6, 0, 8, 6, 0, 0, 0]],
        "output": [[2, 2, 8, 8, 2, 8, 6], [2, 2, 8, 8, 2, 8, 0], [0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 7, 7, 0, 7, 0, 0], [0, 0, 7, 7, 0, 7, 0], [7, 0, 7, 0, 0, 7, 0]],
        "output": [[0, 7, 7, 0, 7, 0, 0], [0, 7, 7, 0, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    },
        {
        "input": [[5, 0, 5, 5, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 5, 0, 5]],
        "output": [[5, 0, 5, 5, 0, 0, 5], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    },
]

def transform(input_grid):
    # Initialize output_grid with zeros
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Copy the first row from input to output
    output_grid[0, :] = input_grid[0, :]

    # Iterate through the first row to find source cells (2 and 8)
    for j in range(cols):
        if input_grid[0, j] == 2 or input_grid[0, j] == 8:
            source_value = input_grid[0, j]
            # Replicate the source value in the second row (index 1)
            if rows > 1: # Ensure there is a second row.
                output_grid[1, j] = source_value

    return output_grid

for i, example in enumerate(examples):
    print(f"----- Example {i + 1} -----")
    predicted_output = transform(example["input"])
    analyze_transformation(example["input"], example["output"], predicted_output)
