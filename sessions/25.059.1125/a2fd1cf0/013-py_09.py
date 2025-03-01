import numpy as np

def find_pixel(grid, color):
    """Finds the location of the first pixel of a given color."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    input_grid_array = np.array(input_grid)

    # 1. Locate red and green pixels
    red_loc = find_pixel(input_grid_array, 2)
    green_loc = find_pixel(input_grid_array, 3)

    if red_loc is None or green_loc is None:
        return output_grid  # Return original if either pixel is missing

    # 2. Horizontal Segment
    if red_loc[1] < green_loc[1]:  # Green is to the right of red
        for c in range(red_loc[1], green_loc[1]):
            output_grid[red_loc[0], c] = 8
        last_horizontal_x = green_loc[1] -1
    else:  # Green is to the left of red
        for c in range(green_loc[1] + 1, red_loc[1] + 1):
            output_grid[red_loc[0], c] = 8
        last_horizontal_x = green_loc[1] + 1
        
    intermediate_grid = np.copy(output_grid) #for debugging

    # 3. Vertical Segment
    if red_loc[0] < green_loc[0]: #green is below red
      for r in range(red_loc[0], green_loc[0]):
        output_grid[r, last_horizontal_x] = 8
    else: #green is above red
      for r in range(green_loc[0], red_loc[0]):
          output_grid[r, last_horizontal_x] = 8


    return output_grid

def show_results(input_grid, expected_output, transformed_grid, intermediate_grid):
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)
    transformed_np = np.array(transformed_grid)
    intermediate_np = np.array(intermediate_grid)

    print("Input:\n", input_np)
    print("Intermediate:\n", intermediate_np)
    print("Expected:\n", expected_np)
    print("Transformed:\n", transformed_np)
    print("Correct:", np.array_equal(expected_np,transformed_np))
    print("-" * 20)
#Example grids
grids = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 2, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 3, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 2, 8, 8, 8, 8, 0],[0, 0, 0, 0, 0, 0, 0, 0, 3, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 2, 0, 0, 0, 3, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 2, 8, 8, 8, 3, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 2, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 3, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 2, 0, 0, 0, 0, 0, 0],[0, 0, 0, 8, 0, 0, 0, 0, 0, 0],[0, 0, 0, 3, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[2, 0, 0, 0, 0, 0, 0, 3, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[2, 8, 8, 8, 8, 8, 8, 3, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }

]

for grid in grids:
    transformed_grid = transform(grid["input"])
    show_results(grid["input"], grid["output"], transformed_grid, intermediate_grid)
