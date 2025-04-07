import numpy as np

"""
The transformation rule identifies the first occurrence (scanning row-major) of a trigger pattern involving an adjacent yellow (4) and red (2) pixel. 

There are two possible trigger configurations:
1. Vertical: Yellow (4) is directly above Red (2) in the same column 'c'.
2. Horizontal: Yellow (4) is directly to the left of Red (2) in the same row, involving columns 'c' and 'c+1'.

The type of trigger determines the transformation applied to the column(s) containing the trigger pixels:

- If the trigger is vertical (4 above 2) in column 'c':
    - The column 'c' is filled with an alternating pattern starting with red (2) and then yellow (4).
    - This fill extends from the top edge (row 0) down to, but not including, the row containing the topmost blue (1) pixel in that column. If no blue pixel exists, the pattern fills the entire column.

- If the trigger is horizontal (4 left of 2) involving columns 'c' (yellow) and 'c+1' (red):
    - Column 'c' is filled with solid yellow (4).
    - Column 'c+1' is filled with solid red (2).
    - Each fill extends from the top edge (row 0) down to, but not including, the row containing the topmost blue (1) pixel in that specific column. If no blue pixel exists in a column, the fill covers the entire column height.

All pixels outside the specifically filled regions remain unchanged from the input grid.
"""

def find_highest_blue(grid, col_index):
    """
    Finds the row index of the topmost blue (1) pixel in a given column.
    Returns the grid height if no blue pixel is found or if the column index is invalid.
    """
    height, width = grid.shape
    if col_index < 0 or col_index >= width:
        return height # Invalid column treated as having no boundary

    for r in range(height):
        if grid[r, col_index] == 1:
            return r
    return height # Return height if no blue pixel is found

def find_first_trigger(grid):
    """
    Scans the grid row-major to find the first trigger pattern.
    Returns:
        tuple: (trigger_type, col1, col2) where:
            trigger_type (str): 'vertical', 'horizontal', or None
            col1 (int): Index of the (first) column involved, or -1 if no trigger.
            col2 (int): Index of the second column (only for horizontal), or -1.
    """
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            # Check for vertical trigger (4 above 2)
            if r + 1 < height and grid[r, c] == 4 and grid[r + 1, c] == 2:
                return 'vertical', c, -1 # col2 is not used for vertical
            # Check for horizontal trigger (4 left of 2)
            if c + 1 < width and grid[r, c] == 4 and grid[r, c + 1] == 2:
                return 'horizontal', c, c + 1 # col1=yellow's col, col2=red's col
    return None, -1, -1 # No trigger found

def apply_alternating_pattern(output_grid, col_index, end_row, color1, color2):
    """
    Applies an alternating pattern (color1, color2, color1, ...)
    to a specific column up to the end_row (exclusive).
    """
    if col_index < 0 or col_index >= output_grid.shape[1]:
        return # Avoid accessing invalid columns

    for row in range(end_row):
        if row % 2 == 0:
            output_grid[row, col_index] = color1
        else:
            output_grid[row, col_index] = color2

def apply_solid_fill(output_grid, col_index, end_row, color):
    """
    Applies a solid color fill to a specific column up to the end_row (exclusive).
    """
    if col_index < 0 or col_index >= output_grid.shape[1]:
        return # Avoid accessing invalid columns
        
    for row in range(end_row):
        output_grid[row, col_index] = color

def transform(input_grid):
    """
    Applies the transformation rule based on the first found trigger pattern.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()
    
    # Find the first trigger pattern
    trigger_type, col1, col2 = find_first_trigger(grid)

    # If no trigger is found, return the unmodified grid copy
    if trigger_type is None:
        return output_grid.tolist()

    # Apply transformation based on the trigger type
    if trigger_type == 'vertical':
        # Find the blue boundary for the single affected column
        blue_row_boundary = find_highest_blue(grid, col1)
        # Apply alternating pattern: starts with red (2), alternates with yellow (4)
        apply_alternating_pattern(output_grid, col1, blue_row_boundary, 2, 4)
        
    elif trigger_type == 'horizontal':
        # Process column col1 (where yellow 4 was)
        blue_row_boundary_c1 = find_highest_blue(grid, col1)
        # Apply solid fill with yellow (4)
        apply_solid_fill(output_grid, col1, blue_row_boundary_c1, 4)
        
        # Process column col2 (where red 2 was)
        blue_row_boundary_c2 = find_highest_blue(grid, col2)
        # Apply solid fill with red (2)
        apply_solid_fill(output_grid, col2, blue_row_boundary_c2, 2)

    # Return the modified grid as a standard list of lists
    return output_grid.tolist()