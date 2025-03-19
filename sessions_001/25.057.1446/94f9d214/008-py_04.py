"""
The transformation rule involves detecting the presence of non-white (non-zero) colored regions within four quadrants of the input grid and representing their presence with a red (value 2) pixel in the corresponding quadrant of a smaller output grid. If a quadrant contains no non-white pixels, the corresponding output pixel is white (value 0).
"""

import numpy as np

def get_quadrant(input_grid, quadrant_index):
    """
    Divides 8x4 input into four 4x2 quadrants and returns one.
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
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the four quadrants of the input grid
    for i in range(4):
        quadrant = get_quadrant(input_grid, i)

        # Check for any non-zero (non-white) pixels in the quadrant
        if np.any(quadrant != 0):
            # Map quadrant index to output grid positions
            if i == 0:  # Top-left
                output_grid[0:2, 0] = 2
            elif i == 1:  # Top-right
                output_grid[0:2, 1] = 2
            elif i == 2:  # Bottom-left
                output_grid[2:4, 0] = 2
            elif i == 3: # Bottom Right
                output_grid[2:4, 1] = 2

    return output_grid