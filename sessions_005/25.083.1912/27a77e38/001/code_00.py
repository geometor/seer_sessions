"""
Copies the input grid to the output, then changes the centermost pixel on the 
bottom row to match a pixel color from a non-bottom row, if one exists. 
If the bottom row center pixel is zero, or no matching color is found, the output bottom row center remains zero.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = input_grid.copy()

    # Locate Center Column
    center_col = width // 2

    # Find Target Value on bottom row
    target_value = input_grid[height - 1, center_col]

    # Find other instance of target value in upper rows
    found_match = False
    for r in range(height - 1):
        for c in range(width):
            if input_grid[r, c] == target_value and target_value !=0:
                found_match = True
                break
        if found_match:
            break
    
    # only change value in output if match was found and not zero
    if found_match:
      output_grid[height - 1, center_col] = target_value

    return output_grid.tolist()