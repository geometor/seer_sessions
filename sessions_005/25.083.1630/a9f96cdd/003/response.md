```python
"""
1.  Find the Red Pixel: Locate the single red pixel (color code 2) within the input grid.
2.  Check for Existence: If no red pixel is found, the output grid is all zeros.
3.  Determine Output Pattern and Position:
    *   If the red pixel is in the first row (row index 0) of the input grid, insert the row [0, 8, 0, 7, 0] at row index 1 in the output grid.
    *   If the red pixel is in the second row (row index 1) of the input grid, insert the pattern [3, 0, 6] in the output grid at row index 0, and insert the pattern [8, 0, 7] in the output grid at row index 2. The columns where these patterns are inserted correspond to the column of the red pixel in the input grid, minus 1.
    *    If the red pixel is in the third row (row index 2) of the input grid, insert the row [0, 0, 0, 3, 0] at row index 1 in the output grid.
4. Output is same size as input.
"""

import numpy as np

def find_red_pixel(grid):
    # Find the coordinates of the red pixel (value 2).
    rows, cols = np.where(grid == 2)
    if len(rows) > 0:
        return rows[0], cols[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.zeros_like(input_grid)

    # Find the red pixel in the input.
    red_pixel_coords = find_red_pixel(input_grid)

    # If a red pixel is found, apply the transformation.
    if red_pixel_coords:
        row, col = red_pixel_coords
        height = input_grid.shape[0]
        width = input_grid.shape[1]

        if row == 0:
           output_grid[1,:] = [0, 8, 0, 7, 0] if width == 5 else [0, 8, 0, 7] #handle edge case where width < 5
        elif row == 1:
            if width >=3: # Pattern insertion requires at least 3 columns
                start_col = max(0, col - 1)
                end_col = min(width, col + 2)

                output_grid[0, start_col:end_col] = [3, 0, 6][:end_col-start_col]
                output_grid[2, start_col:end_col] = [8, 0, 7][:end_col-start_col]
        elif row == 2:
            output_grid[1,:] = [0, 0, 0, 3, 0] if width == 5 else [0,0,0,3]

    return output_grid
```