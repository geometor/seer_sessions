import numpy as np

def get_subgrid(grid, row_start, col_start):
    """Extracts a 3x3 subgrid from the input grid."""
    return grid[row_start:row_start+3, col_start:col_start+3]

def find_first_nonzero(subgrid):
    """Finds the first non-zero element in a subgrid and returns its value."""
    rows, cols = subgrid.shape
    for i in range(rows):
        for j in range(cols):
            if subgrid[i,j] != 0:
                return subgrid[i,j]
    return 0

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize output_grid as a 3x3 array filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Get the top-center 3x3 subgrid.
    top_center_subgrid = get_subgrid(input_grid, 0, 3)
    # Find the first non-zero value in the top-center subgrid.
    top_center_value = find_first_nonzero(top_center_subgrid)
    # Place the value in the output grid.
    output_grid[0, 1] = top_center_value

    # Get the bottom-center 3x3 subgrid.
    bottom_center_subgrid = get_subgrid(input_grid, 6, 3)
    # Find the first non-zero value in the bottom-center subgrid.
    bottom_center_value = find_first_nonzero(bottom_center_subgrid)
    # Place the value in the output grid.
    output_grid[2, 1] = bottom_center_value
    
    return output_grid

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    diff_grid = np.zeros_like(grid1)
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i,j] != grid2[i,j]:
                diff_grid[i,j] = 1  # Mark differences with 1
    return diff_grid

# input_output_pairs is expected to be initialized
for example_idx, (input_grid, output_grid) in enumerate(input_output_pairs):
    transformed_grid = transform(np.array(input_grid))
    result = 'pass' if np.array_equal(transformed_grid, np.array(output_grid)) else 'fail'
    print (f"example_idx: {example_idx}, result: {result}")
    if result == 'fail':
      diff = compare_grids(np.array(output_grid),transformed_grid )
      print(f"expected:\n{np.array(output_grid)}")
      print(f"actual:\n{transformed_grid}")
      print(f"diff:\n{diff}")