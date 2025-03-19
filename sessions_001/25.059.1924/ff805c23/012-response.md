# ff805c23 • 012 • refine_coder

---
```python
"""
1. **Identify the Region of Interest (ROI):** The ROI is the largest contiguous region *inside* the area bounded by color 6 (magenta). The ROI contains pixels of colors other than 6, including 0 (white), 1 (blue) and 8 (azure). The ROI is rectangular.

2. **Determine ROI Boundaries:**  Find the topmost, bottommost, leftmost, and rightmost rows and columns *within* the magenta boundary that still belong to the intended rectangular ROI. This requires looking *inward* from the outermost magenta pixels. The presence of non-magenta pixels inside the boundary helps define the ROI shape.

3. **Create Output Grid:**  Create a new grid filled with color 6 (magenta), with dimensions matching the ROI's width and height.

4. **Copy Exception Pixels:** Copy the color 0 (white) pixels from their corresponding locations within the ROI in the *input* grid to the *output* grid.

"""

import numpy as np

def find_inner_bounding_box(grid):
    """
    Finds the inner bounding box defined by the region of interest (ROI)
    within the area bounded by magenta (color 6).
    """
    rows, cols = grid.shape
    
    # Find outermost magenta pixels
    outer_min_row, outer_min_col, outer_max_row, outer_max_col = find_bounding_box(grid, 6)

    # Find top boundary of ROI (looking downwards from the outermost top magenta)
    top_row = outer_min_row
    while top_row <= outer_max_row:
        if all(grid[top_row, outer_min_col:outer_max_col+1] != 6):
            break
        top_row += 1
    top_row -=1 #adjust

    # Find bottom boundary of ROI (looking upwards from the outermost bottom magenta)
    bottom_row = outer_max_row
    while bottom_row >= outer_min_row:
        if all(grid[bottom_row, outer_min_col:outer_max_col+1] != 6):
            break
        bottom_row -= 1
    bottom_row += 1 #adjust

    # Find left boundary of ROI (looking rightwards from the outermost left magenta)
    left_col = outer_min_col
    while left_col <= outer_max_col:
        if all(grid[outer_min_row:outer_max_row+1, left_col] != 6):
            break
        left_col += 1
    left_col -=1 #adjust

    # Find right boundary of ROI (looking leftwards from the outermost right magenta)
    right_col = outer_max_col
    while right_col >= outer_min_col:
        if all(grid[outer_min_row:outer_max_row+1, right_col] != 6):
             break
        right_col -= 1
    right_col += 1
        
    return top_row, left_col, bottom_row, right_col

def find_bounding_box(grid, color):
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Find the inner bounding box (ROI).
    top_row, left_col, bottom_row, right_col = find_inner_bounding_box(input_grid)

    # Calculate height and width of the ROI.
    height = bottom_row - top_row + 1
    width = right_col - left_col + 1
    
    # Initialize output grid with the calculated dimensions, filled with 6s.
    output_grid = np.full((height, width), 6, dtype=int)

    # Copy color 0 pixels from the input ROI to the output grid.
    for r in range(height):
        for c in range(width):
            input_row = top_row + r
            input_col = left_col + c
            if input_grid[input_row, input_col] == 0:
                output_grid[r, c] = input_grid[input_row, input_col]

    return output_grid
```
