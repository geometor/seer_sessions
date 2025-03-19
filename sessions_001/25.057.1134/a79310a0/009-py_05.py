import numpy as np

def find_non_zero_pixel(grid):
    # Iterate through the grid to find the non-zero pixel
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the non-zero pixel
    non_zero_pixel_coords = find_non_zero_pixel(input_grid)

    # If a non-zero pixel is found, change its value to 2 and move it to the center
    if non_zero_pixel_coords:
        # set original position to zero
        output_grid[non_zero_pixel_coords] = 0
        # move to the center and set to 2
        center_row = output_grid.shape[0] // 2
        center_col = output_grid.shape[1] // 2
        output_grid[center_row, center_col] = 2

    return output_grid

# Example data (replace with actual data from the task)
train_examples = [
    {
        "input": np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 0, 5, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 8, 0, 0, 0], [0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]),
    },
     {
        "input": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 9, 0, 0],[0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]]),
    },
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    expected_output = example["output"]
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input shape: {input_grid.shape}")
    print(f"  Output shape: {expected_output.shape}")
    print(f"  Input non-zero pixels: {np.count_nonzero(input_grid)}")
    print(f"  Output non-zero pixels: {np.count_nonzero(expected_output)}")
    print(f"  Correct Prediction: {np.array_equal(predicted_output, expected_output)}")
    print(f"  Predicted Output:\n{predicted_output}")
    print(f"  Expected Output:\n{expected_output}\n")