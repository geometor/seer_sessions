import numpy as np

# Mock functions - for demonstration purposes.
def find_object(grid, color):
    coords = np.argwhere(grid == color)
    return coords

def shift_object_up(grid, coords, shift_amount):
    new_grid = np.copy(grid)
    for r, c in coords:
        new_grid[r, c] = 0
    for r, c in coords:
        new_r = r - shift_amount
        if 0 <= new_r < new_grid.shape[0]:
            new_grid[new_r, c] = grid[r,c]
    return new_grid

def transform(input_grid):
    output_grid = np.copy(input_grid)
    blue_coords = find_object(output_grid, 1)
    if len(blue_coords)>0:
      output_grid = shift_object_up(output_grid, blue_coords, 4)
    yellow_coords = find_object(output_grid, 4)
    if len(yellow_coords) > 0:
        output_grid = shift_object_up(output_grid, yellow_coords, 2)
    red_coords = find_object(output_grid,2)
    if len(red_coords) > 0:
      output_grid = shift_object_up(output_grid, red_coords, 1)
    return output_grid
    

# Example Input Grids (from the training set - represented as strings for brevity)
example_inputs = [
    """
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 4, 4, 0, 0, 2, 2],
     [0, 0, 0, 0, 4, 4, 0, 0, 2, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """,
        """
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4]]
    """,
    """
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4, 0]]
    """
]

example_outputs = [
    """
    [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 4, 4, 0, 0, 0, 0],
     [0, 0, 0, 0, 4, 4, 0, 0, 2, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """,
    """
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4],
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """,
    """
   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 4, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """
]

def check_transform(input_str, expected_output_str):
    input_grid = np.array(eval(input_str))
    expected_output_grid = np.array(eval(expected_output_str))
    transformed_grid = transform(input_grid)
    print(f"Transformed:\n{transformed_grid}")
    print(f"Expected:\n{expected_output_grid}")
    return np.array_equal(transformed_grid, expected_output_grid)
    

for i, (input_str, output_str) in enumerate(zip(example_inputs, example_outputs)):
    print(f"--- Example {i + 1} ---")
    result = check_transform(input_str, output_str)
    print(f"Result: {'Success' if result else 'Failure'}")