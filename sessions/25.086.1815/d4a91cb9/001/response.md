```python
"""
Draws a rectilinear path (L-shape) between a red pixel (2) and an azure pixel (8) using yellow pixels (4). 
The path consists of a vertical segment along the azure pixel's column and a horizontal segment along the red pixel's row. 
The path only overwrites white pixels (0).
"""

import numpy as np

def find_pixel(grid, color):
    """
    Finds the coordinates (row, col) of the first pixel with the specified color.
    Returns None if the color is not found.
    """
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return r, c
    return None # Should not happen based on task description

def transform(input_grid):
    """
    Transforms the input grid by drawing a yellow L-shaped path between 
    the red and azure pixels.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = grid_np.copy()

    # Locate the coordinates of the red pixel (color 2)
    red_pos = find_pixel(grid_np, 2)
    if red_pos is None:
        # Handle error or return input if red pixel not found (though description implies it exists)
        return input_grid 
    R_row, R_col = red_pos

    # Locate the coordinates of the azure pixel (color 8)
    azure_pos = find_pixel(grid_np, 8)
    if azure_pos is None:
        # Handle error or return input if azure pixel not found (though description implies it exists)
        return input_grid
    A_row, A_col = azure_pos

    # Determine the coordinates of the corner point: Corner = (R_row, A_col)
    # This point defines where the horizontal and vertical segments meet.

    # Draw the vertical segment of the path
    # Iterate through rows from min(R_row, A_row) to max(R_row, A_row) at column A_col
    row_start = min(R_row, A_row)
    row_end = max(R_row, A_row)
    for r in range(row_start, row_end + 1):
        # Only change white pixels (0) to yellow (4)
        if output_grid[r, A_col] == 0:
            output_grid[r, A_col] = 4

    # Draw the horizontal segment of the path
    # Iterate through columns from min(R_col, A_col) to max(R_col, A_col) at row R_row
    col_start = min(R_col, A_col)
    col_end = max(R_col, A_col)
    for c in range(col_start, col_end + 1):
        # Only change white pixels (0) to yellow (4)
        if output_grid[R_row, c] == 0:
            output_grid[R_row, c] = 4

    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
```