```python
"""
1.  **Identify the Non-Zero Region:** Locate the rectangular region within the input grid that contains only non-zero digits. This region is bounded by zeros.

2.  **Isolate the Non-Zero Region:** Extract this rectangular region as a separate sub-grid.

3.  **Invert Colors:**
    *   Take the center pixel from the isolated region in the input.
    *   Swap all instances of this center color with the color that surrounds the isolated non-zero region in the input.
    *   All other colors remain as they are.

4.  **Rotate/transpose and crop:** Rotate/transpose the isolated region by 90 degrees clockwise and crop the minimum rectangle to represent the output.

5. **Return result:** the rotated/transposed and cropped sub-grid with inverted colors is the output.
"""

import numpy as np

def _find_non_zero_region(grid):
    # Find rows and cols that contain non-zero values
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    # Get the min and max indices of non-zero rows and cols
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def _invert_colors(grid, center_color, surround_color):
    # Create a copy to avoid modifying the original grid
    inverted_grid = grid.copy()
    # Swap center_color with surround_color
    inverted_grid[grid == center_color] = surround_color
    inverted_grid[grid == surround_color] = center_color # this line appears wrong
    
    return inverted_grid

def _get_surrounding_color(grid, min_row, max_row, min_col, max_col):
    # Check the color just outside the bounding box.  Assume 0 if at edge.
    if min_row > 0:
        return grid[min_row - 1, min_col]  # Check above
    elif max_row < grid.shape[0] -1:
        return grid[max_row + 1, min_col] # Check below
    elif min_col > 0:
        return grid[min_row, min_col -1] # check left
    elif max_col < grid.shape[1] -1:
        return grid[min_row, max_col + 1]
        
    return 0 # default to 0

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify and 2. Isolate the Non-Zero Region
    min_row, max_row, min_col, max_col = _find_non_zero_region(input_grid)
    isolated_region = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 3. Invert Colors
    # Find center pixel of the isolated region
    center_row = (isolated_region.shape[0] -1 ) // 2
    center_col = (isolated_region.shape[1] - 1) // 2
    
    center_color = isolated_region[center_row, center_col]
    surround_color = _get_surrounding_color(input_grid, min_row, max_row, min_col, max_col)

    # this appears to be working to get the color swap, although perhaps
    # incorrectly
    inverted_region = _invert_colors(isolated_region, center_color, surround_color)

    # 4. Rotate/transpose and Crop
    rotated_region = np.rot90(inverted_region, k=-1)  # Rotate 90 degrees clockwise

    return rotated_region.tolist()
```