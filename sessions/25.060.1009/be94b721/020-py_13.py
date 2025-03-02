"""
1.  **Identify the Azure Rectangle:** Locate the contiguous block of azure (8) pixels in the input grid. This forms a rectangle.
2.  **Determine Output Dimensions:** The output grid is always 4 rows high.  The width is determined by the width of the azure rectangle in the input grid plus one on either side, unless this exceeds the bounds of the input, in which case the largest possible slice is taken.

3.  **Create the Output Grid:** Create a new grid of 4 rows x N columns, where 'N' is calculated width, but never greater than the original.
4. Center the slice vertically.
5. Copy the identified azure rectangle into output. The top of the azure object will always be row 1 of the output and be horizontally centered. Fill any remaining cells in the output grid with black (0).
"""

import numpy as np

def get_object_bounds(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Identify the Azure Rectangle
    bounds = get_object_bounds(input_grid, 8)
    if bounds is None:
        return np.zeros((4, input_grid.shape[1]), dtype=int)  # Return empty grid if object not found
        
    min_row, max_row, min_col, max_col = bounds
    azure_width = max_col - min_col + 1

    # Determine Output Dimensions
    output_height = 4
    output_width = min(input_grid.shape[1], azure_width + 2)

    # initialize output_grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Calculate the horizontal offset for centering the azure rectangle in output
    offset = (output_width - azure_width) // 2

   
    # Copy the azure rectangle to output
    for r in range(min_row,max_row+1):
        for c in range(min_col, max_col + 1):
            output_row = 1 + (r - min_row)
            output_col = offset + (c - min_col)
            
            # Check bounds - should be always ok but just in case
            if 0 <= output_row < output_height and 0<= output_col < output_width:
              output_grid[output_row, output_col] = input_grid[r,c]

    return output_grid