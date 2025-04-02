"""
Perform a pixel-wise color transformation based on the input color.
- White (0) remains White (0).
- Red (2) or Green (3) becomes Yellow (4).
- Blue (1), Magenta (6), Orange (7), or Azure (8) becomes Gray (5).
The grid dimensions and the positions/shapes of the colored objects are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a specific color transformation rule to each pixel of the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Apply the color transformation rules using boolean indexing for efficiency

    # Rule 1: Red (2) or Green (3) -> Yellow (4)
    mask_rule1 = (input_grid == 2) | (input_grid == 3)
    output_grid[mask_rule1] = 4

    # Rule 2: Blue (1), Magenta (6), Orange (7), or Azure (8) -> Gray (5)
    mask_rule2 = (input_grid == 1) | (input_grid == 6) | (input_grid == 7) | (input_grid == 8)
    output_grid[mask_rule2] = 5
    
    # Rule 3: White (0) remains White (0) - this is implicitly handled by copying the input initially.

    return output_grid
