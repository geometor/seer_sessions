# 995c5fa3 • 023 • refine_coder

---
```python
"""
1. **Identify the Center:** Find the row, col coordinates of a pixel that is not color 5 in the input grid.
2. **Extract Subgrid:** Extract the 3x3 subgrid centered at the coordinates from step 1.
3. **Map to Output:** Map the extracted subgrid to the output grid based on these rules:
    *  If the subgrid contains anything other than colors 0 and 5, do not apply these transformation rules.
    * If the subgrid contains only colors 5 and 0:
        - If the center pixel of the subgrid is color 0, the center of the output is one of [2, 4].
        - Map the color 0 pixels in the input subgrid that are not color 5 to color 2 in the output.
        - If there is only one row or column containing a color 0 in the subgrid, the output color is 4.
        - Otherwise, all other pixels in the output grid are 0.
"""

import numpy as np

def _get_center(grid):
    # Find the row, col coordinates of the first pixel that is not color 5.
    h, w = grid.shape
    center_r = -1
    center_c = -1
    for r in range(h):
        for c in range(w):
            if grid[r, c] != 5:
                center_r = r
                center_c = c
                break
        if center_r != -1:
            break
    return center_r, center_c

def _extract_subgrid(grid, center_r, center_c):
    # Extract the 3x3 subgrid centered at (center_r, center_c).
    h, w = grid.shape
    start_row = max(0, center_r - 1)
    end_row = min(h, center_r + 2)
    start_col = max(0, center_c - 1)
    end_col = min(w, center_c + 2)
    return grid[start_row:end_row, start_col:end_col]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the center of the non-background region.
    center_r, center_c = _get_center(input_grid)

    # Handle edge case: input grid is all 5
    if center_r == -1:
        return output_grid

    # Extract the 3x3 subgrid.
    subgrid = _extract_subgrid(input_grid, center_r, center_c)
    
    # Pad subgrid with 5s if smaller than 3x3
    sub_h, sub_w = subgrid.shape
    if sub_h < 3 or sub_w < 3:
      temp_grid = np.full((3,3), 5)
      temp_grid[:sub_h, :sub_w] = subgrid
      subgrid = temp_grid

    # Check if the subgrid contains only colors 0 and 5.
    unique_colors = np.unique(subgrid)
    if not all(color in [0, 5] for color in unique_colors):
        return output_grid  # Return all zeros if other colors are present
    
    # Map to output based on subgrid content.
    if subgrid[1, 1] == 0:
        # Count non-5s rows and columns
        rows_with_0 = np.sum(np.any(subgrid == 0, axis=1))
        cols_with_0 = np.sum(np.any(subgrid == 0, axis=0))

        if rows_with_0 == 1 or cols_with_0 == 1:
          output_grid[1,1] = 4
        else:
          output_grid[1,1] = 2
          
        for i in range(3):
          for j in range(3):
            if subgrid[i,j] == 0 and (i != 1 or j != 1):
              output_grid[i,j] = 2

    return output_grid
```
