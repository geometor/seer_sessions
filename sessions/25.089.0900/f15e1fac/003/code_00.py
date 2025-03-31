import numpy as np
import copy

"""
Transforms an input grid based on the positions of azure (8) and red (2) pixels, following one of two modes or a fallback:

1.  **Mode 1 (Vertical Shift):** Triggered if azure (8) pixels exist in the first row (row 0).
    *   An initial vertical pattern 'P' is defined by the columns of azure pixels in the first row.
    *   This pattern propagates downwards. For each row 'r':
        *   Check if the *input* row 'r' contains any red (2) pixels (triggers).
        *   If triggers exist, find the one with the smallest column index 'c_trig'.
        *   Compare 'c_trig' to the grid's horizontal midpoint 'M = width / 2'.
        *   If 'c_trig < M', shift the pattern 'P' right by 1 column for this row and subsequent rows (add 1 to each column index, discard indices >= width).
        *   If 'c_trig >= M', shift the pattern 'P' left by 1 column for this row and subsequent rows (subtract 1 from each column index, discard indices < 0).
        *   Apply the current (potentially shifted) pattern 'P' to the output grid's row 'r': For each column 'c' in 'P', if the corresponding *input* pixel `input[r, c]` is white (0), set the *output* pixel `output[r, c]` to azure (8). This preserves non-white input pixels (like the red triggers).

2.  **Mode 2 (Horizontal Blocks):** Triggered if Mode 1 is not met and azure (8) pixels exist in the first column (col 0).
    *   Each azure pixel in the first column at row `r` triggers the drawing of three horizontal, 4-pixel-wide azure blocks in the output grid:
        *   Block 1: Starts at `(r, 0)` (cols 0-3)
        *   Block 2: Starts at `(r-1, 4)` (cols 4-7), if `r-1 >= 0`
        *   Block 3: Starts at `(r-2, 8)` (cols 8-11), if `r-2 >= 0`
    *   These blocks overwrite any existing content in the output grid at their locations. All other input pixels are preserved.

3.  **Fallback:** If neither Mode 1 nor Mode 2 conditions are met, the output grid is identical to the input grid.
"""

import numpy as np
import copy # Although numpy copy is used, keeping it in case needed elsewhere.

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
        
        # Calculate grid midpoint (column index)
        midpoint = cols / 2.0
        
        # Find initial pattern columns from the first row
        current_pattern_cols = set(np.where(first_row == 8)[0])

        # Iterate through rows from top to bottom
        for r in range(rows):
            # Check if the *input* grid's current row `r` contains any red (2) pixels
            trigger_indices = np.where(input_np[r, :] == 2)[0]
            
            # If triggers are found in this row, update the pattern *before* applying it
            if len(trigger_indices) > 0:
                # Find the column index of the first (leftmost) trigger
                c_trig = np.min(trigger_indices)
                
                # Determine shift direction and update pattern
                next_pattern_cols = set()
                if c_trig < midpoint: # Shift right
                    for c in current_pattern_cols:
                        if c + 1 < cols: # Check upper bound
                            next_pattern_cols.add(c + 1)
                else: # c_trig >= midpoint: Shift left
                    for c in current_pattern_cols:
                        if c - 1 >= 0: # Check lower bound
                            next_pattern_cols.add(c - 1)
                            
                # Update the pattern for this row and subsequent rows
                current_pattern_cols = next_pattern_cols
                
            # Apply the current (potentially updated) pattern to this row in the output grid
            # Only change pixels that were originally white (0) in the input
            for c in current_pattern_cols:
                # Ensure column index is valid (although shift logic should handle this)
                if 0 <= c < cols:
                    if input_np[r, c] == 0:
                        output_np[r, c] = 8
                        
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
            # Draw Block 1: starts at (r, 0), length 4 (cols 0-3)
            # Overwrites existing pixels in output_np
            c_start, c_end = 0, min(4, cols)
            if c_start < c_end : # Ensure there's actually a range to draw
                output_np[r, c_start:c_end] = 8
                 
            # Draw Block 2: starts at (r-1, 4), length 4 (cols 4-7)
            if r - 1 >= 0: # Check row boundary
                 c_start, c_end = 4, min(8, cols)
                 if c_start < c_end :
                     output_np[r - 1, c_start:c_end] = 8

            # Draw Block 3: starts at (r-2, 8), length 4 (cols 8-11)
            if r - 2 >= 0: # Check row boundary
                 c_start, c_end = 8, min(12, cols)
                 if c_start < c_end :
                     output_np[r - 2, c_start:c_end] = 8

        # Return the result for Mode 2
        return output_np.tolist()

    # --- Fallback ---
    # If neither Mode 1 nor Mode 2 conditions were met,
    # return the initial copy of the input grid (which is already in output_np).
    return output_np.tolist()