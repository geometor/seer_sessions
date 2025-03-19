"""
The transformation rule involves dividing the input grid into four quadrants and checking for the presence of non-white pixels. The output is a 2x2 grid where each cell represents a quadrant of the input. If a quadrant contains any non-white pixels, the corresponding cell in the output grid is red (2); otherwise, it's white (0).
"""

import numpy as np

def get_quadrant(input_grid, quadrant_index):
    """
    Divides the input grid into four quadrants and returns one.
    quadrant_index: 0 (top-left), 1 (top-right), 2 (bottom-left), 3 (bottom-right)
    """
    rows, cols = input_grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant_index == 0:  # Top-left
        return input_grid[:mid_row, :mid_col]
    elif quadrant_index == 1:  # Top-right
        return input_grid[:mid_row, mid_col:]
    elif quadrant_index == 2:  # Bottom-left
        return input_grid[mid_row:, :mid_col]
    elif quadrant_index == 3:  # Bottom-right
        return input_grid[mid_row:, mid_col:]
    else:
        raise ValueError("Invalid quadrant index. Must be 0, 1, 2, or 3.")

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((2, 2), dtype=int) # Initialize 2x2 output grid

    # Iterate through the four quadrants of the input grid
    for i in range(4):
        quadrant = get_quadrant(input_grid, i)

        # Check for any non-zero (non-white) pixels in the quadrant
        if np.any(quadrant != 0):
            # Map quadrant index to output grid positions
            if i == 0:  # Top-left
                output_grid[0, 0] = 2
            elif i == 1:  # Top-right
                output_grid[0, 1] = 2
            elif i == 2:  # Bottom-left
                output_grid[1, 0] = 2
            elif i == 3:  # Bottom-right
                output_grid[1, 1] = 2

    return output_grid