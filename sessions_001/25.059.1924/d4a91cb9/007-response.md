# d4a91cb9 • 007 • refine_coder

---
```python
"""
1. Find Azure Pixel: Locate the first occurrence of an azure (8) pixel in the input grid. If none is found, the transformation is complete.
2. Find Red Pixel: Locate the first occurrence of a red (2) pixel in the input grid. If none is found, the transformation is complete.
3. Draw Yellow Line: Draw a yellow (4) line connecting the azure pixel to the red pixel. The line should only use horizontal and vertical segments (no diagonals). Change existing pixel values to yellow (4) along the path.
4. No other changes: The output grid is otherwise identical to the input grid.
"""

import numpy as np

def find_first_pixel(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def draw_line(grid, start, end, color):
    """Draws a line from start to end using only horizontal and vertical moves."""
    if start is None or end is None:
        return

    r1, c1 = start
    r2, c2 = end

    if r1 == r2:  # Horizontal line
        for c in range(min(c1, c2) + 1, max(c1, c2)):
            grid[r1, c] = color
    elif c1 == c2:  # Vertical line
        for r in range(min(r1, r2) + 1, max(r1, r2)):
            grid[r, c1] = color
    else: # draw 2-part L-shaped line
        # first vertical part:
        for r in range(min(r1,r2), max(r1,r2)+1):
            grid[r,c1] = color
        # then horizontal part:
        for c in range(min(c1,c2) + 1, max(c1,c2)):
            grid[r2,c] = color       

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the first azure and red pixels
    azure_pos = find_first_pixel(output_grid, 8)
    red_pos = find_first_pixel(output_grid, 2)

    # Draw the yellow line if both pixels are found
    if azure_pos is not None and red_pos is not None:
        draw_line(output_grid, azure_pos, red_pos, 4)

    return output_grid
```
