import copy
import math

def find_gray_row(grid):
    """
    Finds the row index of the solid horizontal gray line (color 5).

    Args:
        grid (list[list[int]]): The input grid.

    Returns:
        int: The row index of the gray line, or -1 if not found.
    """
    height = len(grid)
    if height == 0:
        return -1
    width = len(grid[0])
    if width == 0:
        return -1
        
    for r in range(height):
        if all(grid[r][c] == 5 for c in range(width)):
            # Check if it's a solid line of gray
            if len(grid[r]) == width: # ensure row has expected width
                 return r
    return -1 # Gray line not found

def transform(input_grid):
    """
    Transforms the input grid by modifying a single pixel in the last row.
    The color of the modified pixel is determined by a rule based on the color
    of the pixel located in the middle column, one row above a solid horizontal
    gray line.

    Rule:
    1. Find the solid horizontal gray line (color 5).
    2. Identify the pixel above it in the middle column (P_above).
    3. Determine the source color based on P_above's color (C_above):
       - If C_above is red (2), use red (2).
       - If C_above is green (3), use the color from the pixel 2 rows above the gray line in the middle column.
       - If C_above is yellow (4), use blue (1).
       - Otherwise, use C_above itself.
    4. Set the pixel in the last row, middle column to this source color.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return [] # Handle empty grid case
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)] # Handle grid with empty rows

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Calculate the middle column index
    mid_col = width // 2

    # Find the row index of the solid gray line
    gray_row = find_gray_row(input_grid)

    # If no gray line is found, or if it's the top row (no pixel above), return the original grid
    if gray_row <= 0: 
        return output_grid 

    # Get the color of the pixel immediately above the gray line in the middle column
    # (gray_row - 1 is guaranteed to be >= 0 because gray_row > 0)
    c_above = input_grid[gray_row - 1][mid_col]

    # Determine the source color based on the conditional logic
    source_color = -1 # Initialize with an invalid color

    if c_above == 2: # Red
        source_color = 2
    elif c_above == 3: # Green
        # Need to look 2 rows above the gray line. Check if that row exists.
        if gray_row >= 2:
            source_color = input_grid[gray_row - 2][mid_col]
        else:
            # This case (green above gray line, but gray line is at row 1) 
            # was not in examples. Default to c_above for robustness.
            source_color = c_above 
    elif c_above == 4: # Yellow
        source_color = 1 # Blue
    else:
        # Default case for any other color not specified in the rules (including 0, 1, 5, 6, 7, 8, 9)
        source_color = c_above

    # Identify the target pixel coordinates (last row, middle column)
    target_row = height - 1

    # Modify the target pixel in the output grid
    # Ensure source_color was determined (should always be unless grid structure is unexpected)
    if source_color != -1:
        output_grid[target_row][mid_col] = source_color
    # else: leave the pixel as it was in the copy (or potentially handle as error)

    return output_grid