import numpy as np
import copy

"""
Transforms an input grid based on the positions of azure (8) and red (2) pixels, following one of two modes or a fallback:

1.  **Mode 1 (Vertical Shift):** Triggered if azure (8) pixels exist in the first row (row 0).
    *   An initial vertical pattern is defined by the columns of azure pixels in the first row.
    *   This pattern propagates downwards. For each row, white (0) pixels in the input grid at the pattern's columns are changed to azure (8) in the output grid.
    *   If a row in the *input* grid contains a red (2) pixel, the pattern for subsequent rows shifts one column to the left (negative indices are discarded).
    *   Non-white pixels from the input (like the red triggers) are preserved unless overwritten by the propagated pattern (which only happens if they were white initially).

2.  **Mode 2 (Horizontal Blocks):** Triggered if Mode 1 is not met and azure (8) pixels exist in the first column (col 0).
    *   Each azure pixel in the first column at row `r` triggers the drawing of three horizontal, 4-pixel-wide azure blocks in the output grid:
        *   Block 1: Starts at `(r, 0)`
        *   Block 2: Starts at `(r-1, 4)` (if `r-1 >= 0`)
        *   Block 3: Starts at `(r-2, 8)` (if `r-2 >= 0`)
    *   These blocks overwrite any existing content in the output grid at their locations. All other input pixels are preserved.

3.  **Fallback:** If neither Mode 1 nor Mode 2 conditions are met, the output grid is identical to the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list[list[int]]): The input grid as a 2D list of integers.

    Returns:
        list[list[int]]: The transformed grid as a 2D list of integers.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)

    # --- Check conditions and apply transformations ---

    # Condition for Mode 1: Azure (8) in the first row (row 0)
    first_row = input_np[0, :]
    if 8 in first_row:
        # --- Mode 1: Vertical Shift ---
        
        # Find initial pattern columns from the first row
        current_pattern_cols = set(np.where(first_row == 8)[0])

        # Iterate through rows from top to bottom
        for r in range(rows):
            # Apply the current pattern to this row in the output grid
            # Only change pixels that were originally white (0)
            for c in current_pattern_cols:
                # Ensure column index is valid before accessing
                if 0 <= c < cols:
                    if input_np[r, c] == 0:
                        output_np[r, c] = 8
            
            # Check if the *input* grid's current row `r` contains any red (2) pixels
            # This determines the pattern for the *next* row
            if 2 in input_np[r, :]:
                # Update pattern for the next row by shifting all columns left by 1
                next_pattern_cols = set()
                for c in current_pattern_cols:
                    if c - 1 >= 0: # Discard resulting negative indices
                        next_pattern_cols.add(c - 1)
                # Update the pattern for the next iteration
                current_pattern_cols = next_pattern_cols 
                
        # Return the result for Mode 1
        return output_np.tolist() 

    # Condition for Mode 2: No azure in row 0, BUT azure (8) in the first column (col 0)
    # This check only happens if Mode 1 condition was false
    first_col = input_np[:, 0]
    if 8 in first_col:
        # --- Mode 2: Horizontal Blocks ---
        
        # Find all trigger row indices `r` where input[r, 0] is azure (8)
        trigger_rows = np.where(first_col == 8)[0]

        # For each trigger row, draw the three horizontal blocks
        for r in trigger_rows:
            # Draw Block 1: starts at (r, 0), length 4
            # Overwrites existing pixels in output_np
            for c_offset in range(4):
                 c = 0 + c_offset
                 if c < cols: # Check column boundary
                     output_np[r, c] = 8
                 
            # Draw Block 2: starts at (r-1, 4), length 4
            if r - 1 >= 0: # Check row boundary
                 for c_offset in range(4):
                     c = 4 + c_offset
                     if c < cols: # Check column boundary
                         output_np[r - 1, c] = 8

            # Draw Block 3: starts at (r-2, 8), length 4
            if r - 2 >= 0: # Check row boundary
                 for c_offset in range(4):
                     c = 8 + c_offset
                     if c < cols: # Check column boundary
                         output_np[r - 2, c] = 8

        # Return the result for Mode 2
        return output_np.tolist()

    # --- Fallback ---
    # If neither Mode 1 nor Mode 2 conditions were met,
    # return the initial copy of the input grid.
    return output_np.tolist()