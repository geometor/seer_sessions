import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input, filled with 0s.
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Determine the rows where the colored lines will be placed.
    # The pattern is: azure, blue, green, red, with 0s padding top and bottom.

    # Find available rows for the fixed pattern
    colored_line_rows = []
    if rows >= 4:
        colored_line_rows = [rows // 2 - 2, rows // 2 -1, rows //2, rows//2 + 1] #try the center of the grid
        if colored_line_rows[0] < 0:
          colored_line_rows = [0,1,2,3] # if its very short, just start from top

    # Place the colored lines in the output grid.
    if len(colored_line_rows) >= 4 :
        output_grid[colored_line_rows[0], :] = 8  # Azure line
        output_grid[colored_line_rows[1], :] = 1  # Blue line
        output_grid[colored_line_rows[2], :] = 3  # Green line
        output_grid[colored_line_rows[3], :] = 2  # Red line
    elif rows > 0: #edge case, small grids
        if rows > 0:
            output_grid[0,:] = 8
        if rows > 1:
            output_grid[1,:] = 1
        if rows > 2:
            output_grid[2,:] = 3
        if rows > 3:
            output_grid[3,:] = 2
    return output_grid

def describe_grid(grid, name="Grid"):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    print(f"{name}:")
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique Colors: {unique_colors}")
    for color in unique_colors:
        count = np.sum(grid == color)
        print(f"    Color {color}: Count {count}")

#Example Usage (replace with your actual task data)
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8, 8, 8, 8, 8, 8, 8], [1, 1, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2, 2, 2, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [8, 8, 8, 8, 8, 8], [1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        },
        {
           "input": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            "output": [[8, 8, 8], [1, 1, 1], [3, 3, 3]]
        }
    ]
}

for i, example in enumerate(task["train"]):
    input_grid = np.array(example["input"])
    expected_output = np.array(example["output"])
    actual_output = transform(input_grid)

    print(f"Example {i+1}:")
    describe_grid(input_grid, "Input")
    describe_grid(expected_output, "Expected Output")
    describe_grid(actual_output, "Actual Output")
    print("-" * 30)