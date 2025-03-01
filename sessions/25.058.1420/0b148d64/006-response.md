# 0b148d64 • 006 • refine_coder

---
```python
"""
1.  **Identify Target Object:** Find the contiguous rectangular object within the input grid that is not color 0 (white) and not color 8.
2.  **Define Bounding Box:** Determine the smallest rectangle (bounding box) that completely encloses the target object.
3.  **Crop:** Extract the target object from the input grid using the bounding box.
4. **Discard background**: remove all regions of the input grid with color 8
5.  **Resize:** Reduce both the height and width of the cropped object by half.
6.  **Output:** The resulting resized object is the output.
"""

import numpy as np

def find_target_object(grid):
    # Find the bounding box of the target object (non-0 and non-8 color)
    grid = np.array(grid)
    target_colors = [color for color in np.unique(grid) if color != 0 and color != 8]
    
    if not target_colors: # if there is no target color
        return None, None, None, None
        
    target_color = target_colors[0]  # There should only be one.
    coords = np.argwhere(grid == target_color)
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, min_col, max_row, max_col, target_color

def transform(input_grid):
    # Find the bounding box of target object
    min_row, min_col, max_row, max_col, target_color = find_target_object(input_grid)

    if min_row is None:  # Handle cases where no target object is found
      return []

    # Crop the target object
    cropped_grid = np.array(input_grid)[min_row:max_row+1, min_col:max_col+1]

    # Resize (halve dimensions)
    new_height = cropped_grid.shape[0] // 2
    new_width = cropped_grid.shape[1] // 2
    rows = np.linspace(0, cropped_grid.shape[0]-1, new_height, dtype=int)
    cols = np.linspace(0, cropped_grid.shape[1]-1, new_width, dtype=int)
    output_grid = cropped_grid[np.ix_(rows, cols)]

    return output_grid.tolist()
```
