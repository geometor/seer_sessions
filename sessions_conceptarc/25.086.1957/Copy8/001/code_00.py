import numpy as np
import math

def find_separator_columns(grid):
    """
    Finds columns in the grid that consist entirely of the background color (0).
    
    Args:
        grid (np.ndarray): The input grid.
        
    Returns:
        list: A list of indices of the separator columns. Returns empty list if none found.
    """
    num_rows, num_cols = grid.shape
    separator_cols = []
    for c in range(num_cols):
        is_separator = True
        for r in range(num_rows):
            if grid[r, c] != 0:
                is_separator = False
                break
        if is_separator:
            separator_cols.append(c)
    return separator_cols

def transform(input_grid):
    """
    Transforms the input grid based on a reflection rule across a vertical separator.

    1. Identify vertical columns composed entirely of the background color (0). 
       These columns define a central vertical axis of symmetry.
    2. Calculate the reflection axis coordinate as the average of the start and 
       end indices of these separator columns.
    3. Create the output grid by copying the input grid.
    4. For each pixel (r, c) to the left of the separator columns in the input grid, 
       calculate its reflected column position c_reflected based on the symmetry axis.
    5. Set the pixel at (r, c_reflected) in the output grid to the color of the 
       input pixel (r, c), overwriting the original value at that position.
    """
    # Convert input to numpy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_arr.shape
    
    # Initialize output grid as a copy of the input
    output_arr = np.copy(input_arr)

    # 1. Find separator columns
    separator_cols = find_separator_columns(input_arr)

    # Handle cases: no separator found (shouldn't happen based on examples)
    # or separator is at the edge (also unlikely for reflection)
    if not separator_cols:
        # If no separator, maybe return input? Or raise error?
        # Based on the task structure, a separator seems guaranteed.
        # For now, assume separator exists and is not just edge columns.
        return input_grid # Return unchanged if no separator logic works

    # 2. Calculate reflection axis
    s_start = separator_cols[0]
    s_end = separator_cols[-1]
    axis_col = (s_start + s_end) / 2.0

    # 3. Output grid is already initialized as a copy.

    # 4. & 5. Iterate through pixels left of the separator and reflect them
    # The left part includes columns from 0 up to (but not including) s_start
    for r in range(num_rows):
        for c in range(s_start):
            # Calculate the reflected column index
            # Use math.floor or int() for index. Rounding might be safer. Let's use round.
            c_reflected = round(2 * axis_col - c)
            
            # Ensure the reflected column is within bounds (should be if symmetric)
            if 0 <= c_reflected < num_cols:
                 # Get the color from the input grid's left side
                 color = input_arr[r, c]
                 # Set the pixel on the right side of the output grid
                 output_arr[r, c_reflected] = color

    # Convert output numpy array back to list of lists
    output_grid = output_arr.tolist()
    
    return output_grid
