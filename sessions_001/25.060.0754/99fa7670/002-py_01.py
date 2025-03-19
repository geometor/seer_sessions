"""
1.  **Identify** all non-zero colored cells within the input grid.
2.  For each identified colored cell:
    *   **Extend** the cell's color horizontally to the right edge of the grid.
    *   **Extend** the color of all cells in this extended row, downwards to fill the input grid shape.

Essentially, each non-zero cell's color is propagated rightward and then downward, overwriting any existing colors. The key is the order: right, then fill down from the extended row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending non-zero colored cells to the right and down.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy to avoid modifying the original
    rows, cols = input_grid.shape

    # Iterate through each cell in the input grid
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                # Extend the cell's color horizontally to the right
                output_grid[r, c:] = input_grid[r, c]
                
    # second loop - fill down            
    for r in range(rows):
        for c in range(cols):        
            if output_grid[r,c] != 0:
               output_grid[r:, c] = output_grid[r,c]
    
    return output_grid