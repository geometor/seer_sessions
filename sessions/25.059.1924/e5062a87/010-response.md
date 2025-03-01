# e5062a87 • 010 • example_2 • investigate_coder

---
```python
"""
Finds a horizontal line segment of red (2) pixels and extends it horizontally until it hits a non-white (0) pixel or the edge of the grid.
"""

import numpy as np

def find_red_line_segment(grid):
    # iterate over rows
    for r_idx, row in enumerate(grid):
        # iterate over pixel values
        for c_idx, pixel in enumerate(row):
            # looking for red
            if pixel == 2:
                # start building segment from here
                segment = []
                c = c_idx
                while c < len(row) and row[c] == 2:
                    segment.append((r_idx, c))
                    c += 1
                if len(segment) > 0:
                  return segment
    return None

def extend_segment(grid, segment):
    """Extends a line segment horizontally."""
    if not segment:
      return grid

    output_grid = np.copy(grid)
    row_index = segment[0][0]
    row = grid[row_index]

    # Extend to the left
    c_left = segment[0][1] -1
    while c_left >= 0 and grid[row_index][c_left] == 0 :
      output_grid[row_index][c_left] = 2
      c_left -= 1


    # Extend to the right
    c_right = segment[-1][1] + 1
    while c_right < len(row) and grid[row_index][c_right] == 0:
        output_grid[row_index][c_right] = 2
        c_right += 1

    return output_grid

def transform(input_grid):
    """
    Finds a horizontal line segment of red pixels and extends it.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid)

    # Find the red line segment
    red_segment = find_red_line_segment(grid)

    # Extend the red line segment
    output_grid = extend_segment(grid, red_segment)
    
    # change output pixels to be the same as input, extended if red

    return output_grid.tolist()
```
