import numpy as np

def report(input_grid, output_grid, expected_output_grid):
    """Generates a report comparing the output grid to the expected output grid."""

    print("Input Grid:")
    print(input_grid)
    print("Output Grid (from transform function):")
    print(output_grid)
    print("Expected Output Grid:")
    print(expected_output_grid)

    correct = np.array_equal(output_grid, expected_output_grid)
    print(f"Correct: {correct}")
    if not correct:
        differences = output_grid != expected_output_grid
        print("Indices where differences occur:")
        print(np.where(differences))
        print("Values at differing indices (Output, Expected):")
        diff_indices = np.where(differences)
        for i in range(len(diff_indices[0])):
            row, col = diff_indices[0][i], diff_indices[1][i]
            print(
                f"  ({row}, {col}): {output_grid[row, col]}, {expected_output_grid[row, col]}"
            )
    print("-" * 20)
    return correct

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # define the color mapping
    color_map = {
        9: 8,
        4: 3,
        2: 6
    }

    # iterate through each pixel in the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # apply color mapping
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid

# Example Data (replace with actual data from the task)
train_pairs = [
    {
        "input": np.array([[9, 4, 2], [9, 9, 2], [4, 9, 4]]),
        "output": np.array([[8, 3, 6], [8, 8, 6], [3, 8, 3]]),
    },
    {
        "input": np.array([[2, 9, 9], [4, 9, 2], [9, 4, 2]]),
        "output": np.array([[6, 8, 8], [3, 8, 6], [8, 3, 6]]),
    },
    {
        "input": np.array([[4, 9, 4], [4, 2, 9], [9, 4, 2]]),
        "output": np.array([[3, 8, 3], [3, 6, 8], [8, 3, 6]]),
    },
    {
        "input": np.array([[4, 4, 9], [9, 2, 4], [2, 9, 4]]),
        "output": np.array([[3, 3, 8], [8, 6, 3], [6, 8, 3]]),
    },
]

results = []
for i, pair in enumerate(train_pairs):
    output_grid = transform(pair["input"])
    correct = report(pair["input"], output_grid, pair["output"])
    results.append(correct)
    
print(f"overall correct: {all(results)}")
