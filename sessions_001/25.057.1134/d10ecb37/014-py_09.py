"""
The transformation identifies and extracts the fundamental repeating 2x2 unit from the top-left of the input grid to create the output grid.
"""

import numpy as np

def get_block(grid, row_start, col_start, height, width):
    """Extracts a subgrid (block) from the given grid."""
    return grid[row_start:row_start + height, col_start:col_start + width]

def transform(input_grid):
    """Transforms the input grid by extracting the top-left 2x2 block."""
    
    # Convert input to a NumPy array
    input_np = np.array(input_grid)

    # Extract the 2x2 block from the top-left corner
    output_np = get_block(input_np, 0, 0, 2, 2)

    # Convert the result back to a list
    output_grid = output_np.tolist()

    return output_grid