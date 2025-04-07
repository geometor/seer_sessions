import numpy as np

"""
The transformation rule identifies the first trigger pattern consisting of a yellow (4) pixel adjacent to a red (2) pixel, scanning row by row, then column by column. 
There are two possible trigger configurations:
1. Vertical: Yellow (4) is directly above Red (2) in the same column 'c'.
2. Horizontal: Yellow (4) is directly to the left of Red (2) in the same row, involving columns 'c' and 'c+1'.

Based on the trigger type and location, specific columns are filled with an alternating pattern of yellow (4) and red (2) from the top edge (row 0) down to, but not including, the row containing the topmost blue (1) pixel in that column. If no blue pixel exists in a column, the pattern fills the entire column height.

The starting color of the alternating pattern in each affected column depends on the color of the trigger pixel located within that column:
- If the column contains the yellow (4) part of the trigger, the pattern starts with yellow (4) and alternates with red (2).
- If the column contains the red (2) part of the trigger, the pattern starts with red (2) and alternates with yellow (4).

All other pixels in the grid remain unchanged.
"""

def find_highest_blue(grid, col_index):
    """
    Finds the row index of the topmost blue (1) pixel in a given column.
    Returns the grid height if no blue pixel is found.
    """
    height = grid.shape[0]
    # Check if col_index is valid
    if col_index < 0 or col_index >= grid.shape[1]:
        return height # Treat invalid columns as having no blue boundary
        
    for r in range(height):
        if grid[r, col_index] == 1:
            return r
    return height # Return height if no blue pixel is found

def apply_pattern(output_grid, col_index, end_row, start_color, alternate_color):
    """
    Applies the alternating pattern (start_color, alternate_color, ...) 
    to a specific column up to the end_row (exclusive).
    """
    # Check if col_index is valid before applying pattern
    if col_index < 0 or col_index >= output_grid.shape[1]:
        return 
        
    for row in range(end_row):
        if row % 2 == 0:
            output_grid[row, col_index] = start_color
        else:
            output_grid[row, col_index] = alternate_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()
    height, width = grid.shape

    trigger_found = False
    trigger_type = None
    trigger_col_c = -1  # Column containing yellow (4) or the only column for vertical
    trigger_col_c1 = -1 # Column containing red (2) for horizontal trigger

    # Scan row-major to find the first trigger
    for r in range(height):
        for c in range(width):
            # Check for vertical trigger (4 above 2)
            if r + 1 < height and grid[r, c] == 4 and grid[r + 1, c] == 2:
                trigger_type = 'vertical'
                trigger_col_c = c # In vertical, both trigger parts are in the same column
                trigger_found = True
                break # Found the first trigger, stop searching columns
            # Check for horizontal trigger (4 left of 2)
            if c + 1 < width and grid[r, c] == 4 and grid[r, c + 1] == 2:
                trigger_type = 'horizontal'
                trigger_col_c = c   # Column with yellow (4)
                trigger_col_c1 = c + 1 # Column with red (2)
                trigger_found = True
                break # Found the first trigger, stop searching columns
        if trigger_found:
            break # Found the first trigger, stop searching rows
            
    # If no trigger was found, return the original grid copy
    if not trigger_found:
        return output_grid.tolist()

    # Apply transformation based on the identified trigger
    if trigger_type == 'vertical':
        # The column contains the red part of the trigger (at r+1, c)
        start_color = 2
        alternate_color = 4
        # Find the blue boundary for the affected column
        blue_row = find_highest_blue(grid, trigger_col_c)
        # Apply pattern starting with red (2)
        apply_pattern(output_grid, trigger_col_c, blue_row, start_color, alternate_color)
        
    elif trigger_type == 'horizontal':
        # Process column c (where yellow 4 was)
        start_color_c = 4
        alternate_color_c = 2
        blue_row_c = find_highest_blue(grid, trigger_col_c)
        # Apply pattern starting with yellow (4)
        apply_pattern(output_grid, trigger_col_c, blue_row_c, start_color_c, alternate_color_c)
        
        # Process column c+1 (where red 2 was)
        start_color_c1 = 2
        alternate_color_c1 = 4
        blue_row_c1 = find_highest_blue(grid, trigger_col_c1)
         # Apply pattern starting with red (2)
        apply_pattern(output_grid, trigger_col_c1, blue_row_c1, start_color_c1, alternate_color_c1)

    # Return the modified grid as a list of lists
    return output_grid.tolist()