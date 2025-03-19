import numpy as np

# The provided code (copied here for execution)
def find_cross_center(grid):
    # Find the center of the cross shape
    rows, cols = np.where(grid == 0)
    if len(rows) == 0:
        return None
    center_row = int(np.mean(rows))
    center_col = int(np.mean(cols))
    return center_row, center_col

def is_part_of_cross(grid, row, col, center_row, center_col):
    # Check if a cell is part of the cross
    if grid[row, col] != 0:
        return False

    #check if on same row or col as center
    if row == center_row or col == center_col:
        return True

    return False

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the center of the cross
    center = find_cross_center(input_grid)
    if center is None:
      return output_grid
    center_row, center_col = center

    # Iterate through the grid and remove the cross
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if is_part_of_cross(input_grid, row, col, center_row, center_col):
                #do nothing since output is already a copy of input
                pass
    return output_grid

# Example Data (Replace with actual data from the task)
examples = [
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 0, 8, 8, 8, 8],
                           [8, 8, 8, 8, 0, 8, 8, 8, 8],
                           [8, 8, 8, 8, 0, 8, 8, 8, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 8, 8, 0, 8, 8, 8, 8],
                           [8, 8, 8, 8, 0, 8, 8, 8, 8],
                           [8, 8, 8, 8, 0, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    },
    {
        "input": np.array([[8, 0, 8, 8, 8, 8, 8],
                           [8, 0, 8, 8, 8, 8, 8],
                           [8, 0, 8, 8, 8, 0, 8],
                           [8, 0, 8, 8, 8, 8, 8],
                           [8, 0, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 0, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8]]),
    },
    {
       "input": np.array([[6, 6, 6, 6, 6, 6, 6, 6],
                          [6, 6, 6, 6, 0, 6, 6, 6],
                          [6, 6, 0, 6, 0, 6, 0, 6],
                          [6, 6, 6, 6, 0, 6, 6, 6],
                          [6, 6, 6, 6, 0, 6, 6, 6],
                          [6, 6, 6, 6, 6, 6, 6, 6]]),
        "output": np.array([[6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 0, 6, 6, 6, 0, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6],
                           [6, 6, 6, 6, 6, 6, 6, 6]]),
    },

]

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    actual_output = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Matches Expected: {np.array_equal(actual_output, expected_output)}")
    center = find_cross_center(input_grid)
    print(f"  cross center {center}")
