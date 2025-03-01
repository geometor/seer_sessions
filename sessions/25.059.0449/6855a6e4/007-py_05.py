import numpy as np

# Helper functions (from the provided code)
def find_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []  # Return empty list if no objects found
    return coords

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def move_object(grid, coords, row_shift, col_shift, color):
    """Moves an object to a new location in the grid, overwriting values"""
    new_coords = []

    # remove old
    for r, c in coords:
        grid[r,c] = 0

    # add new
    for r, c in coords:
      new_coords.append( (r + row_shift, c + col_shift) )
      grid[r + row_shift, c + col_shift] = color

    return new_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects
    red_coords = find_objects(input_grid, 2)
    grey_coords = find_objects(input_grid, 5)

    # Copy red object
    for r, c in red_coords:
        output_grid[r, c] = 2

    # Red Bounding Box
    if red_coords:
        red_min_row, red_max_row, red_min_col, red_max_col = bounding_box(red_coords)

        # Grey Object Placement
        if grey_coords:
            grey_height = bounding_box(grey_coords)[1] - bounding_box(grey_coords)[0] + 1
            grey_width = bounding_box(grey_coords)[3] - bounding_box(grey_coords)[2] + 1
            
            # calculate shifts
            row_shift = red_max_row - (bounding_box(grey_coords)[0] + grey_height -1) 
            col_shift = red_max_col - (bounding_box(grey_coords)[2] + grey_width - 1)
            
            # apply shift
            move_object(output_grid, grey_coords, row_shift, col_shift, 5)

    return output_grid

# Example Data (replace with actual data from the problem)
example_inputs = [
    np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 0, 0, 0, 0],
        [0, 5, 5, 0, 0, 0, 0],
    ]),
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 5, 0, 0, 0, 0],
        [0, 0, 5, 5, 0, 0, 0, 0],
    ]),
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 2, 0, 0, 0],
        [0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 5],
        [0, 0, 0, 0, 0, 0, 5, 5],
    ])
]

example_outputs = [
     np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 5, 0],
        [0, 0, 0, 0, 5, 5, 0],
    ]),
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 5, 0, 0],
        [0, 0, 0, 0, 5, 5, 0, 0],
    ]),
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 2, 2, 0, 0, 0],
        [0, 2, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 5],
        [0, 0, 0, 0, 0, 0, 5, 5],
    ]),
]

def compare_grids(grid1, grid2):
    """Checks if two grids are identical."""
    return np.array_equal(grid1, grid2)

# Analyze each example
for i, (input_grid, expected_output) in enumerate(zip(example_inputs, example_outputs)):
    predicted_output = transform(input_grid.copy())  # Use a copy to avoid modifying the original
    is_correct = compare_grids(predicted_output, expected_output)
    print(f"Example {i+1}: Correct = {is_correct}")
    if not is_correct:
      print(f"predicted:\n{predicted_output}\nexpected:\n{expected_output}")
