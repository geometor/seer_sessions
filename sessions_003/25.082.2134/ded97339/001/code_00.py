"""
1.  **Identify Azure Pixels:** Locate all pixels with the value 8 (azure) in the input grid.

2.  **Horizontal Expansion:** For each row, if there are multiple azure pixels, fill the space between the *leftmost* and *rightmost* azure pixels in that row with azure pixels.

3. **Fill Down within bounds**: fill with azure pixels, every black pixel found between the top-most and bottom-most azure pixel *within each column*.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds the coordinates of all azure pixels in the grid."""
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Horizontal Expansion
    for r in range(rows):
        azure_in_row = [c for c in range(cols) if input_grid[r, c] == 8]
        if len(azure_in_row) > 1:
            leftmost = min(azure_in_row)
            rightmost = max(azure_in_row)
            output_grid[r, leftmost:rightmost+1] = 8

    # Fill Down within bounds
    for c in range(cols):
        azure_in_col = [r for r in range(rows) if input_grid[r,c] == 8]
        if len(azure_in_col) > 1:
           topmost = min(azure_in_col)
           bottommost = max(azure_in_col)
           output_grid[topmost:bottommost+1, c] = 8

    return output_grid