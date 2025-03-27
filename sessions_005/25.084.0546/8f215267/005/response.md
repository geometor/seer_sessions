```python
"""
Transforms an input grid by eroding shapes to their vertically and horizontally connected cores, removing isolated pixels and stray lines.
The background color is assumed to be the most frequent color in the grid.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, assumed to be the background.
    """
    flat_grid = grid.flatten()
    color_counts = Counter(flat_grid)
    return color_counts.most_common(1)[0][0]

def is_connected(grid, r, c, color):
    """
    Checks if a pixel at (r, c) is connected (horizontally or vertically) to another pixel of the same color.
    """
    rows, cols = grid.shape
    # Check above
    if r > 0 and grid[r-1, c] == color:
        return True
    # Check below
    if r < rows - 1 and grid[r+1, c] == color:
        return True
    # Check left
    if c > 0 and grid[r, c-1] == color:
        return True
    # Check right
    if c < cols - 1 and grid[r, c+1] == color:
        return True
    return False

def transform(input_grid):
    """
    Transforms the input grid by eroding non-background shapes.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    background_color = find_background_color(input_grid)

    rows, cols = input_grid.shape

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != background_color:
                # Check if the pixel is connected to any neighbors of the same color
                if not is_connected(input_grid, r, c, color):
                    output_grid[r, c] = background_color #remove isolated pixels
                else: #check for horizontal lines
                    line_start = c
                    while c < cols and input_grid[r,c] == color:
                      c += 1
                    line_end = c
                    if line_end - line_start > 1:
                      #if any in line is not vertically connected, then set entire line to background
                      remove = False
                      for i in range(line_start, line_end):
                        if not (r > 0 and input_grid[r-1,i] == color) and not (r < rows-1 and input_grid[r+1, i] == color):
                          remove = True
                          break
                      if remove:
                        output_grid[r,line_start:line_end] = background_color

    return output_grid.tolist()
```