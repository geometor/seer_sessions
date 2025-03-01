import numpy as np

# Define the transform function (as provided)
def find_blue_pixel(grid):
    # Find the coordinates of the blue pixel (value 1).
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                return (i, j)
    return None  # Should not happen in the intended cases

def transform(input_grid):
    """
    Crops the input grid to a 3x3 area centered on the blue pixel.
    """
    # Find the blue pixel.
    blue_pixel_coords = find_blue_pixel(input_grid)

    if blue_pixel_coords is None:
        return input_grid # defaults to returning input if not found

    # Determine the cropping region.
    row, col = blue_pixel_coords
    start_row = row - 1
    end_row = row + 2
    start_col = col - 1
    end_col = col + 2

    # Create the output grid by extracting the 3x3 region.
    output_grid = input_grid[max(0, start_row):min(input_grid.shape[0], end_row),
                            max(0, start_col):min(input_grid.shape[1], end_col)]

    return output_grid

# Example Inputs and Outputs (from the task)
train_inputs = [
    np.array([[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 1]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

train_outputs = [
    np.array([[0, 0, 0],
              [0, 1, 0],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [0, 0, 1],
              [0, 0, 0]]),
    np.array([[0, 0, 0],
              [0, 0, 0],
              [0, 0, 1]]),
    np.array([[0, 0, 0],
             [0, 1, 0],
             [0, 0, 0]])
]

# Analyze each example
for i, (input_grid, expected_output) in enumerate(zip(train_inputs, train_outputs)):
    blue_pixel_loc = find_blue_pixel(input_grid)
    output_grid = transform(input_grid)
    padding_needed = not output_grid.shape == (3, 3)
    print(f"Example {i+1}:")
    print(f"  Input Dims: {input_grid.shape}")
    print(f"  Blue Pixel Loc: {blue_pixel_loc}")
    print(f"  Output Dims: {output_grid.shape}")
    print(f"  Padding Needed: {padding_needed}")
    print(f"  Expected Output Dims: {expected_output.shape}")
    print(f"Transformed:\n{output_grid}\nExpected:\n{expected_output}\n")
