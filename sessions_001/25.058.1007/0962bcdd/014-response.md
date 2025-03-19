# 0962bcdd • 014 • refine_coder

---
```python
"""
1.  **Identify Crosses:** Locate all "cross" shapes in the input grid. A cross is defined as a central magenta (6) pixel surrounded by four azure (8) pixels, one in each orthogonal direction (up, down, left, right).

2.  **Expand to Squares:** For each identified cross:
    *   Replace the entire 3x3 area centered on the cross's original magenta pixel with azure (8) pixels. This creates a 3x3 azure square.

3. **Replicate Magenta Pixels (Simplified Rule):**
     - Find the bounding box that contains the initial "cross."
     - Identify all the magenta pixels that constitute the border.
     - Do not consider internal pixels.
     - Replicate the border one level out from the expanded azure square.

"""

import numpy as np

def find_crosses(grid):
    """Finds the coordinates of the center of each cross in the grid."""
    crosses = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r, c] == 6:  # Magenta center
                if (grid[r-1, c] == 8 and grid[r+1, c] == 8 and
                    grid[r, c-1] == 8 and grid[r, c+1] == 8):
                    crosses.append((r, c))
    return crosses

def get_border(grid, cross_center):
    """Identifies the magenta pixels forming the border around the cross, excluding internal pixels."""
    r, c = cross_center
    border_pixels = []
   
    # Get initial bounding box around the cross
    min_r, max_r = r,r
    min_c, max_c = c,c
    
    # Expand the bounding box to find the extent of magenta pixels
    for i in range(r-1, r + 2):
      for j in range(c-1, c+2):
        if grid[i,j] == 6:
           min_r = min(min_r, i)
           max_r = max(max_r, i)
           min_c = min(min_c, j)
           max_c = max(max_c, j)
        
    # Iterate through the bounding box to find the border pixels
    for i in range(min_r-1, max_r+2):
      for j in range(min_c-1, max_c+2):
        if grid[i,j] == 6 and (i < min_r or i > max_r or j < min_c or j > max_c) :
            border_pixels.append((i,j))
    return border_pixels, min_r, max_r, min_c, max_c
    
def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    crosses = find_crosses(input_grid)

    for cross_center in crosses:
        r, c = cross_center

        # Expand to 3x3 azure square
        for i in range(r - 1, r + 2):
            for j in range(c - 1, c + 2):
                output_grid[i, j] = 8

        # Replicate magenta border
        border_pixels, min_r, max_r, min_c, max_c = get_border(input_grid, cross_center)

        # Calculate offset
        offset_r = r-min_r
        offset_c = c-min_c
        
        # Iterate through border and place one level out.
        for pixel_r, pixel_c in border_pixels:
            new_r = pixel_r + (pixel_r - r) // abs(pixel_r - r) if pixel_r !=r else pixel_r
            new_c = pixel_c + (pixel_c - c) // abs(pixel_c - c) if pixel_c != c else pixel_c          
            output_grid[new_r,new_c] = 6


    return output_grid
```
