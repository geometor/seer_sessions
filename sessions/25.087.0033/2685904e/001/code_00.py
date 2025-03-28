"""
Transformation Rule:

1.  Identify the control row (row 0) and the key row (row 8).
2.  Count the number of azure (8) pixels in the control row. Let this count be N.
3.  Count the frequency of each non-white (0) color in the key row.
4.  Select colors 'C' from the key row whose frequency is exactly equal to N.
5.  For each selected color C:
    a. Find all columns 'j' where the key row has color C.
    b. In these columns 'j', draw a vertical line of color C.
    c. The line should span from row `6 - N` up to and including row 5.
6.  If N is 0 or no colors match the frequency N, the output grid is identical to the input grid except for the region where lines might be drawn (rows 1-5).
7.  All other parts of the grid remain unchanged.
"""

import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    
    # Define key row indices
    control_row_idx = 0
    key_row_idx = 8
    draw_end_row_idx = 5
    base_row_idx = 6 # The row below the drawing area (gray line)

    # Step 2: Count N (number of azure pixels in the control row)
    control_row = input_np[control_row_idx, :]
    N = np.count_nonzero(control_row == 8)

    # If N is 0, no lines can be drawn based on the rule (frequency must match N)
    if N == 0:
        return output_grid

    # Step 3: Count frequencies in the key row (excluding white)
    key_row = input_np[key_row_idx, :]
    color_counts = Counter(c for c in key_row if c != 0)

    # Step 4: Identify target colors C where count(C) == N
    target_colors = {color for color, count in color_counts.items() if count == N}

    # Step 5 & 6: Draw vertical lines for target colors
    if target_colors:
        start_row_idx = base_row_idx - N
        # Ensure start row is not less than 0 (though based on grid size and examples, unlikely)
        start_row_idx = max(0, start_row_idx) 
        
        num_cols = input_np.shape[1]
        
        for col_idx in range(num_cols):
            # Get the color in the key row for this column
            key_color = key_row[col_idx]
            
            # Check if this color is one of the target colors
            if key_color in target_colors:
                # Draw the vertical line segment
                for row_idx in range(start_row_idx, draw_end_row_idx + 1):
                    # Check bounds just in case, though draw_end_row_idx is fixed at 5
                    if 0 <= row_idx < input_np.shape[0]: 
                         output_grid[row_idx, col_idx] = key_color

    # Step 7: Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by testing framework
