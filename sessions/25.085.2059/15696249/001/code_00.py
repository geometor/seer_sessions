"""
Create a new 9x9 grid, filled entirely with the background color (white, 0).
Examine the input 3x3 grid.
Check if any row in the input_grid consists of only one color (is uniform):
  If the top row (row 0) is uniform: Tile the input_grid horizontally three times (3x9). Place this pattern into the top three rows (0-2) of the output_grid.
  If the middle row (row 1) is uniform: Tile the input_grid horizontally three times (3x9). Place this pattern into the middle three rows (3-5) of the output_grid.
  If the bottom row (row 2) is uniform: Tile the input_grid horizontally three times (3x9). Place this pattern into the bottom three rows (6-8) of the output_grid.
If no uniform row was found, check if any column in the input_grid consists of only one color (is uniform):
  If the left column (column 0) is uniform: Tile the input_grid vertically three times (9x3). Place this pattern into the left three columns (0-2) of the output_grid.
  If the middle column (column 1) is uniform: Tile the input_grid vertically three times (9x3). Place this pattern into the middle three columns (3-5) of the output_grid.
  If the right column (column 2) is uniform: Tile the input_grid vertically three times (9x3). Place this pattern into the right three columns (6-8) of the output_grid.
Return the resulting output_grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 9x9 output grid based on the presence
    and location of a uniform row or column in the input.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    input_rows, input_cols = input_np.shape

    # Initialize the 9x9 output grid with background color 0 (white)
    output_grid = np.zeros((9, 9), dtype=int)
    
    # Check for uniform rows
    for r in range(input_rows):
        row = input_np[r, :]
        # Check if all elements in the row are the same
        if len(set(row)) == 1:
            # Create a horizontally tiled pattern (3x9)
            tiled_pattern = np.tile(input_np, (1, 3))
            # Calculate the starting row index for placement
            start_row = r * 3
            # Place the tiled pattern in the output grid
            output_grid[start_row:start_row + input_rows, :] = tiled_pattern
            # Convert back to list of lists before returning
            return output_grid.tolist()

    # If no uniform row was found, check for uniform columns
    for c in range(input_cols):
        col = input_np[:, c]
        # Check if all elements in the column are the same
        if len(set(col)) == 1:
            # Create a vertically tiled pattern (9x3)
            tiled_pattern = np.tile(input_np, (3, 1))
            # Calculate the starting column index for placement
            start_col = c * 3
            # Place the tiled pattern in the output grid
            output_grid[:, start_col:start_col + input_cols] = tiled_pattern
            # Convert back to list of lists before returning
            return output_grid.tolist()

    # This part should theoretically not be reached based on the examples,
    # but return the empty grid just in case.
    return output_grid.tolist()