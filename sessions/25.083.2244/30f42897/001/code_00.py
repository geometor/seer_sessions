"""
The input grid is transformed by reflecting pixel values across a diagonal axis.
The diagonal axis is selected based on the position of non-8 color values in the
input. If non-8 values are along the bottom, reflection is across the
top-left to bottom-right diagonal. If along the right or top edge,
reflection is along top-right to bottom-left diagonal.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check for non-8 values along the bottom edge
    bottom_edge_has_non_8 = any(input_grid[-1, c] != 8 for c in range(cols))
    # Check for non-8 values along right and top edge
    right_edge_has_non_8 = any(input_grid[r,-1] !=8 for r in range(rows))
    top_edge_has_non_8 = any(input_grid[0,c] !=8 for c in range(cols))
    
    if bottom_edge_has_non_8:
        # Reflect along the top-left to bottom-right diagonal
        for r in range(rows):
            for c in range(cols):
                output_grid[r, c] = input_grid[c, r]
    elif right_edge_has_non_8 or top_edge_has_non_8:
      # Reflect along top-right to bottom left diagonal
        for r in range(rows):
            for c in range(cols):
              output_grid[r,c] = input_grid[rows - 1 - c, cols - 1 - r]
    else:
        #default case, identity transformation if neither of the edge cases exist
        pass #output grid already initialized.

    return output_grid