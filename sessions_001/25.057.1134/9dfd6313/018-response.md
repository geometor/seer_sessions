# 9dfd6313 • 018 • refine_coder

---
```python
"""
1.  **Anchor Identification:** Identify all grey (5) pixels. These pixels act as anchors and do not change their positions in the output grid. They define "zones" above and below them.
2. **Copy Anchors:** Grey pixels are placed on the output grid
3.  **Non-Anchor Pixel Movement:** Iterate through each non-grey and non-white pixel in the input grid (in reading order: left to right, top to bottom).
    *   **Vertical Check:** For the current pixel, examine its column:
        *   If a grey pixel exists *above* the current pixel in the same column, find the nearest grey. Then, move the current pixel's color value to the  empty cell directly *above* that nearest grey pixel.
        *   If a grey pixel exists *below* the current pixel in the same column, find the nearest grey. Then, move the current pixel's color value to the  empty cell directly *below* that nearest grey pixel.
        *  If the pixel was moved based on the adjacent rule, check if there is a non-white pixel to it's immediate right.  If there is, and it has a grey above, move it to the space directly above its neighbor.
4. Copy the pixels to the output that haven't moved.
"""

import numpy as np

def find_nearest_grey_above(grid, row, col):
    """Finds the nearest grey (5) cell above the given cell in the same column."""
    for r in range(row - 1, -1, -1):
        if grid[r][col] == 5:
            return r
    return -1

def find_nearest_grey_below(grid, row, col):
    """Finds the nearest grey (5) cell below the given cell in the same column."""
    for r in range(row + 1, len(grid)):
        if grid[r][col] == 5:
            return r
    return -1

def find_empty_above(grid, row, col):
    """Finds the first empty (0) cell directly above the given row in the same column."""
    for r in range(row -1, -1, -1):
       if grid[r][col] == 0:
          return r
    return -1 # no empty cell

def find_empty_below(grid, row, col):
   """Find the first empty (0) cell directly below the given row in the same column"""
   for r in range(row + 1, len(grid)):
      if grid[r][col] == 0:
         return r
   return -1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    moved = np.zeros_like(input_grid, dtype=bool) # track if pixel has moved
    
    # Copy Anchors
    for r in range(rows):
      for c in range(cols):
        if input_grid[r][c] == 5:
            output_grid[r][c] = 5
            moved[r,c] = True

    # Non-Anchor Pixel Movement
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] not in (0, 5) and not moved[r,c]:
                val = input_grid[r][c]
                
                # Check for grey above
                grey_above = find_nearest_grey_above(input_grid, r, c)
                if grey_above != -1:
                    empty_above = find_empty_above(output_grid, grey_above + 1, c)
                    if empty_above != -1:
                        output_grid[empty_above][c] = val
                        moved[r,c] = True
                        # check right neighbor
                        if c+1 < cols and input_grid[r, c+1] != 0:
                           grey_neighbor = find_nearest_grey_above(input_grid, r, c+1)
                           if grey_neighbor != -1:
                              empty_neighbor = find_empty_above(output_grid, grey_neighbor + 1, c + 1)
                              if empty_neighbor != -1:
                                output_grid[empty_neighbor][c+1] = input_grid[r][c+1]
                                moved[r,c+1] = True
                        continue

                # Check for grey below
                grey_below = find_nearest_grey_below(input_grid, r, c)
                if grey_below != -1:

                    empty_below = find_empty_below(output_grid, grey_below , c)
                    if empty_below != -1 :
                        output_grid[empty_below][c] = val
                        moved[r,c] = True
                        continue

    # copy unmoved
    for r in range(rows):
        for c in range(cols):
           if not moved[r,c]:
              output_grid[r][c] = input_grid[r][c]

    return output_grid
```
