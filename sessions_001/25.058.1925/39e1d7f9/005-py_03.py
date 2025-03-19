import numpy as np

def find_object(grid, color):
    """Finds the bounding box of a contiguous object of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    output_grid = np.copy(input_grid)
    grid_height, grid_width = input_grid.shape

    # Find the magenta (6) object on the lower-right
    magenta_lower_right_top_left, magenta_lower_right_bottom_right = find_object(input_grid[grid_height//2:, grid_width//2:], 6)
    if magenta_lower_right_top_left:
       magenta_lower_right_top_left = (magenta_lower_right_top_left[0] +  grid_height//2, magenta_lower_right_top_left[1] + grid_width//2)
       magenta_lower_right_bottom_right = (magenta_lower_right_bottom_right[0] + grid_height//2, magenta_lower_right_bottom_right[1] + grid_width//2)

    #find the green (3) object second from the top.
    green_top_left, green_bottom_right = find_object(input_grid[:grid_height//2,grid_width//2:],3)

    # Perform the color swap within the identified region.
    if magenta_lower_right_top_left and green_top_left:
      # Swap magenta to green in lower right rectangle
        for r in range(magenta_lower_right_top_left[0], magenta_lower_right_bottom_right[0] + 1):
            for c in range(magenta_lower_right_top_left[1], magenta_lower_right_bottom_right[1] + 1):
                if output_grid[r,c] == 6:
                   output_grid[r, c] = 3

       #Swap the upper rectangle to all magenta
        for r in range(green_top_left[0], green_bottom_right[0] + 1):
            for c in range(green_top_left[1], green_bottom_right[1] + 1):
                if output_grid[r,c] == 3:
                   output_grid[r,c] = 6

    return output_grid

task_id = "3906de3d"

train_inputs = [
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 3, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 6, 5, 5]]),

np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 5, 5, 5]]),

np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 3, 3, 5],
       [5, 5, 5, 5, 5, 5, 3, 6, 3, 5],
       [5, 5, 5, 5, 5, 5, 3, 3, 3, 5]])
]

train_outputs = [
    np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 6, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 3, 5, 5]]),

np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 3, 5, 5, 5]]),

np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
       [5, 5, 5, 5, 5, 5, 6, 6, 6, 5],
       [5, 5, 5, 5, 5, 5, 6, 3, 6, 5],
       [5, 5, 5, 5, 5, 5, 6, 6, 6, 5]])
]

for i in range(len(train_inputs)):
    input_grid = train_inputs[i]
    expected_output = train_outputs[i]
    actual_output = transform(input_grid)
    
    print(f"Example {i+1}:")
    print(f"Input grid dimensions: {input_grid.shape}")

    # Find Green and Magenta Objects
    green_object = find_object(input_grid, 3)
    magenta_object = find_object(input_grid, 6)
    
    print(f"Green object bounding box: {green_object}")
    print(f"Magenta object bounding box: {magenta_object}")
    
    print("Input Grid:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)
    print("Correct:", np.array_equal(expected_output, actual_output))
    print("-" * 40)