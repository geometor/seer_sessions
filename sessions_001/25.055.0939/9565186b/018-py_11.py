"""
1.  **Identify the Middle Row:** Find the row in the center of the input grid.
2.  **Examine Middle Row Colors:** Inspect the colors of all pixels within the middle row.
3. **Conditional Modification**:
      *   If the middle row consists *solely* of azure pixels, change all azure pixels in that row to gray.
      *   If the middle row contains azure and ANY color OTHER than azure, change all azure pixels in that row to gray.
      *   All other pixels in the grid (those not in the middle row) always remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the number of rows in the grid
    rows = output_grid.shape[0]
    middle_row_index = rows // 2
    middle_row = output_grid[middle_row_index]

    # Check if the middle row contains only azure pixels (8)
    if np.all(middle_row == 8):
        output_grid[middle_row_index] = 5  # Change all to gray (5)
    elif 8 in middle_row:
        # If azure is present, check for other colors.
        unique_colors = np.unique(middle_row)
        if len(unique_colors) > 1: #More than one color present
            #change azure to gray
            output_grid[middle_row_index][output_grid[middle_row_index] == 8] = 5
        
    
    # Return the modified grid
    return output_grid