# 6ecd11f4 • 020 • refine_coder

---
```python
"""
1.  **Identify the Target Region:** Find the region of pixels in the input grid that contains colors other than white (0) and azure (8). This area can be of any shape and size. If there is no such area, the output is a 4x4 grid of zeros.
2.  **Determine Top-Left:** Find the top-left-most pixel (minimum row and minimum column) within the target region.
3.  **Subsample:** Starting from the identified top-left pixel of the target region, create a 4x4 output grid. Select pixels from the input grid using a step of 2 in both rows and columns, starting from the top-left pixel.
    *   Input Grid Reference: `input_r = min_row + r * 2`, `input_c = min_col + c * 2`
    *   `r` and `c` are row, col index values for the output grid (range 0-3).
4.  **Apply Adjacency Rule:** Before subsampling, for each pixel within the target region, check for direct adjacency (up, down, left, or right) to an azure (8) pixel in the *original* input grid. If an azure pixel is directly adjacent, set the corresponding pixel in the output grid to white (0), *before* placing it into the output grid.
5.  **Handle Out-of-Bounds:** If the subsampling process goes beyond the boundaries of the target region, fill the corresponding cells in the 4x4 output grid with white (0). If there were no pixels in the target area, the output should be all zeros.
"""

import numpy as np

def find_target_region(grid):
    """
    Finds the top-left coordinate of the non-white, non-azure region.
    Returns None if no such region exists.
    """
    rows, cols = grid.shape
    min_row, min_col = rows, cols

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r, c] != 8:
                min_row = min(min_row, r)
                min_col = min(min_col, c)

    if min_row == rows: # No valid region found
        return None
    
    return (min_row, min_col)
    

def is_adjacent_to_azure(grid, r, c):
    """
    Checks if a cell is directly adjacent (up, down, left, right) to an azure (8) cell.
    """
    rows, cols = grid.shape
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 8:
            return True
    return False

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid = np.array(input_grid)
    top_left = find_target_region(input_grid)

    # initialize output grid to all white (0)
    output_grid = np.zeros((4, 4), dtype=int)

    if top_left is None:
        return output_grid.tolist() # return all 0's

    min_row, min_col = top_left
    
    # build list of target pixels and whether they are adjacent to azure
    target_pixels = []
    rows, cols = input_grid.shape
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] != 0 and input_grid[r,c] != 8:
          target_pixels.append( ((r,c), is_adjacent_to_azure(input_grid, r, c)) )
    

    for r in range(4):
        for c in range(4):
            input_r = min_row + r * 2
            input_c = min_col + c * 2
            
            # check if any of target pixels match the input coordinates
            pixel_value = 0  # Default to white (0)
            for (tr, tc), adjacent in target_pixels:
                if tr == input_r and tc == input_c:
                  if adjacent:
                    pixel_value = 0
                  else:
                    pixel_value = input_grid[tr, tc]
                  break # use the value of the first one found
            output_grid[r,c] = pixel_value

    return output_grid.tolist()
```
