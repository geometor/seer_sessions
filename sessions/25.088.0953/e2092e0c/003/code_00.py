import numpy as np
import math

"""
Identifies a unique horizontal bar of exactly four gray pixels ('5 5 5 5'). 
Based on the value 'V' of the pixel immediately to the right of this bar, 
it calculates the placement (top-left corner: row1, start_col) for a 5x5 modification area.
The output grid is a copy of the input grid, modified within this 5x5 area:
1. A gray (5) border of 1-pixel thickness is drawn.
2. The 3x3 interior region within the border is filled by copying the corresponding 
   3x3 region from the original input grid.

Detailed Steps:
1. Find the unique horizontal sequence '5 5 5 5'. Let its start be (R, C).
2. Get the value 'V' of the pixel at (R, C+4).
3. Calculate the start column for the 5x5 area: start_col = (C + 4) + floor(V / 2) - 2.
4. Determine the top row 'row1' for the 5x5 area based on V:
   - If V=4, row1 = R + 1.
   - If V=6, row1 = R + 5.
   - If V=8, row1 = R + 4.
5. Calculate the bottom row 'row2' = row1 + 4 and the right column 'end_col' = start_col + 4.
6. Initialize the output grid as a copy of the input grid.
7. Copy the 3x3 block of pixels from input[row1+1:row2, start_col+1:end_col] to 
   output[row1+1:row2, start_col+1:end_col].
8. Draw the gray (5) border in the output grid:
   - Top: output[row1, start_col : end_col+1] = 5
   - Bottom: output[row2, start_col : end_col+1] = 5
   - Left: output[row1+1 : row2, start_col] = 5
   - Right: output[row1+1 : row2, end_col] = 5
"""

def find_source_bar(grid_np):
    """
    Finds the unique horizontal bar '5 5 5 5' in the grid.

    Args:
        grid_np: A numpy array representing the input grid.

    Returns:
        A tuple (row, col) of the starting coordinates of the bar,
        or None if the bar is not found or is not unique/exactly 4 long.
    """
    rows, cols = grid_np.shape
    target_pattern = np.array([5, 5, 5, 5], dtype=int)
    found_coords = None
    
    for r in range(rows):
        for c in range(cols - 3): # Iterate potential start columns
            # Check if the 4-pixel segment matches the pattern
            if np.array_equal(grid_np[r, c:c+4], target_pattern):
                # Ensure it's exactly 4 pixels long (not part of a longer bar)
                # Check pixel before (if not at column 0)
                starts_at_c = (c == 0 or grid_np[r, c-1] != 5)
                # Check pixel after (if not at last possible position)
                ends_at_c3 = (c + 4 >= cols or grid_np[r, c+4] != 5)
                
                if starts_at_c and ends_at_c3:
                    # Ensure uniqueness - if already found, it's ambiguous
                    if found_coords is not None:
                        return None # Not unique
                    found_coords = (r, c) 
                    
    return found_coords # Return the unique coordinates or None


def transform(input_grid):
    """
    Transforms the input grid by creating a 5x5 framed area based on 
    the position and right-neighbor value of a specific four-pixel gray bar.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape
    
    # --- Step 1: Find the source bar '5 5 5 5' and its coordinates (R, C) ---
    source_coords = find_source_bar(input_np)
    
    if source_coords is None:
        # If the specific source bar isn't found or isn't unique/exact length, 
        # return the original grid unchanged.
        return input_grid 
        
    R, C = source_coords
    
    # --- Step 2: Identify the trigger pixel and its value V ---
    trigger_col_idx = C + 4
    if trigger_col_idx >= cols:
        # Trigger pixel position is outside the grid bounds, return unchanged.
        # This is unexpected based on examples.
        return output_grid.tolist() 
        
    V = input_np[R, trigger_col_idx]
    
    # --- Step 3: Calculate the starting column for the new 5x5 area ---
    # Formula derived from analyzing example transformations:
    # start_col = trigger_col_idx + floor(V / 2) - 2
    try:
        start_col = trigger_col_idx + math.floor(V / 2) - 2
    except TypeError:
         # V might not be a number if something unexpected happens
         return output_grid.tolist() # Return unchanged if V is not valid for calculation

    # --- Step 4: Determine the row index (row1) for the top of the 5x5 area ---
    row1 = -1 # Initialize with an invalid value
    if V == 4:
        row1 = R + 1
    elif V == 6:
        row1 = R + 5
    elif V == 8:
        row1 = R + 4
    else:
        # The value V is not one of the expected values (4, 6, 8).
        # Based on training data, this shouldn't happen. Return unchanged.
        return output_grid.tolist()

    # --- Step 5: Calculate the bounds for the 5x5 area ---
    row2 = row1 + 4
    end_col = start_col + 4
    
    # --- Boundary Check: Ensure the 5x5 area is within grid bounds ---
    if not (0 <= row1 < rows and 0 <= row2 < rows and 
            0 <= start_col < cols and 0 <= end_col < cols):
        # The calculated 5x5 area goes out of bounds. Return unchanged.
        # This is unexpected based on examples.
        return output_grid.tolist()
        
    # --- Step 6: Define the interior 3x3 area bounds ---
    interior_row_start = row1 + 1
    interior_row_end = row2 # Slicing is exclusive at the end
    interior_col_start = start_col + 1
    interior_col_end = end_col # Slicing is exclusive at the end

    # --- Step 7: Copy the 3x3 interior from the input grid to the output grid ---
    # Ensure the source region for copy is also valid (redundant given Step 5 check, but safe)
    if (interior_row_start >= 0 and interior_row_end <= rows and
        interior_col_start >= 0 and interior_col_end <= cols):
          output_grid[interior_row_start:interior_row_end, interior_col_start:interior_col_end] = \
              input_np[interior_row_start:interior_row_end, interior_col_start:interior_col_end]

    # --- Step 8: Draw the gray border in the output grid ---
    border_color = 5
    
    # Top border
    output_grid[row1, start_col : end_col + 1] = border_color
    # Bottom border
    output_grid[row2, start_col : end_col + 1] = border_color
    # Left border (excluding corners)
    output_grid[interior_row_start : interior_row_end, start_col] = border_color
    # Right border (excluding corners)
    output_grid[interior_row_start : interior_row_end, end_col] = border_color

    # Convert the final NumPy array back to a list of lists for the expected output format
    return output_grid.tolist()