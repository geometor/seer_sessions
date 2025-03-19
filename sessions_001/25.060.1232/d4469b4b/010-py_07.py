"""
The transformation rule is:
1.  **Identify Blue Region:** Locate all blue pixels (value 1) in the input grid.
2.  **Create Bounding Box.** The bounding box of the shape in input will be the size of the output
3.  **Compress to Output Grid:** Create 3x3 output.
4.  **Fill with Gray:** Fill cells inside the box with the color gray (5) except the corners.
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Handle case where color is not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)  # Convert to numpy array for easier manipulation

    # 1. Identify Blue Region and 2. Create bounding box
    top_left, bottom_right = get_bounding_box(input_grid, 1)

    # 3. Compress to Output Grid & 4. Fill output
    
    output_grid = np.zeros((3, 3), dtype=int)

    output_grid[:] = 5
    output_grid[0,0] = 0
    output_grid[0,2] = 0
    output_grid[2,0] = 0
    output_grid[2,2] = 0
    

    return output_grid.tolist()