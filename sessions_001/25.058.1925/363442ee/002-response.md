# 363442ee • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Separator:** Locate the vertical column of gray (5) pixels. This divides the grid into a left and right region.
2.  **Clear Blue Pixels**: scan the grid and locate any blue (1) pixels, set the value of those locations as 0 (white).
3.  **Copy Left Region:** Copy the shape present to the left of the separator column.
4.  **Paste to the Right Region:** Paste the copied shape to the right region, with separator as the left border.
5.  **Check for Second Shape:** If the original shape is not square and touches the lower border, copy the shape, rotate clockwise by 90 degrees, then paste it so it is located where the top border of the shape is the last row of the grid, and the left border is the separator.
"""

import numpy as np

def find_separator_column(grid):
    """Finds the index of the vertical gray (5) separator column."""
    for j in range(grid.shape[1]):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Should not happen, based on problem description

def copy_left_region(grid, separator_index):
    """Copies the region to the left of the separator."""
    return grid[:, :separator_index].copy()

def paste_region(grid, region, start_col):
    """Pastes a region into the grid starting at a specified column."""
    rows = min(grid.shape[0], region.shape[0])
    cols = min(grid.shape[1] - start_col, region.shape[1])
    grid[:rows, start_col:start_col + cols] = region[:rows, :cols]

def rotate_clockwise(region):
    """Rotates a 2D numpy array 90 degrees clockwise."""
    return np.rot90(region, k=-1)
    

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    
    # 1. Identify Separator
    separator_index = find_separator_column(output_grid)

    # 2. Clear Blue Pixels
    output_grid[output_grid == 1] = 0

    # 3. Copy Left Region
    left_region = copy_left_region(input_grid, separator_index)

    # 4. Paste to Right Region
    paste_region(output_grid, left_region, separator_index + 1)
    
    # 5. check for second shape
    if left_region.shape[0] != left_region.shape[1] and input_grid.shape[0] - left_region.shape[0] == 0 :
        rotated_left_region = rotate_clockwise(left_region)
        paste_region(output_grid, rotated_left_region, separator_index + 1 )
        output_grid = output_grid[:input_grid.shape[0],:]
    
    
    return output_grid.tolist()
```
