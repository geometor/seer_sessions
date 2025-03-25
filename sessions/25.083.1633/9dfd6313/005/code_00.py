"""
The transformation extracts all non-zero elements from the input grid, preserving their original order of appearance, and then repacks them into an output grid of the same size, starting from the top-left corner and filling each row completely before moving to the next.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by repacking non-zero elements.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # 1. Identify and Extract non-zero elements
    non_zero_elements = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != 0:
                non_zero_elements.append(input_grid[r, c])

    # 2. Repack into Output Grid
    output_row = 0
    output_col = 0
    for value in non_zero_elements:
        # Place the value in the next available position
        output_grid[output_row, output_col] = value
        
        # Update to the next position (row-major order)
        output_col += 1
        if output_col >= output_grid.shape[1]:
            output_col = 0
            output_row += 1

    return output_grid.tolist()