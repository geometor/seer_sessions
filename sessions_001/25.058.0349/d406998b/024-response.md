# d406998b • 024 • refine_coder

---
```python
"""
Iterate through the input grid, identifying gray (5) pixels. For each gray pixel,
determine if it's part of a continuous, unbroken horizontal or vertical line of
gray pixels.  If it is, change the color of all pixels in that line to green (3).
All other pixels remain unchanged.
"""

import numpy as np

def is_part_of_line(grid, row, col, visited):
    """
    Checks if a gray pixel is part of a horizontal or vertical line.

    Args:
        grid: The input grid.
        row: Row index of the pixel.
        col: Column index of the pixel.
        visited: set of visited pixels

    Returns:
        A tuple: (is_part_of_line, line_pixels) where is_part_of_line is a boolean
        indicating if the pixel is part of a line, and line_pixels is a set
        containing the coordinates of all pixels in the line (or an empty set
        if it's not part of a line).
    """
    rows, cols = grid.shape
    if grid[row, col] != 5:
        return False, set()

    # Check horizontal line
    horizontal_line = set()
    c = col
    while c >= 0 and grid[row, c] == 5:
        horizontal_line.add((row, c))
        c -= 1
    c = col + 1
    while c < cols and grid[row, c] == 5:
        horizontal_line.add((row, c))
        c += 1

    # Check if the horizontal line pixels have only two neighbors,
    # except end points
    if len(horizontal_line) > 1:
        valid_horizontal = True
        h_list = sorted(list(horizontal_line), key=lambda x:x[1]) # sort by col
        for r,c in h_list:
          neighbors = 0
          if (r,c-1) in horizontal_line:
            neighbors += 1
          if (r,c+1) in horizontal_line:
            neighbors += 1
          if neighbors > 2 or (neighbors == 1 and c != h_list[0][1] and c != h_list[-1][1]):
            valid_horizontal = False
            break
        if valid_horizontal:
            # Check if pixels already in a vertical line
            for r, c in horizontal_line:
                if (r,c) in visited:
                  return False, set()
            return True, horizontal_line

    # Check vertical line
    vertical_line = set()
    r = row
    while r >= 0 and grid[r, col] == 5:
        vertical_line.add((r, col))
        r -= 1
    r = row + 1
    while r < rows and grid[r, col] == 5:
        vertical_line.add((r, col))
        r += 1

    # Check if the horizontal line pixels have only two neighbors,
    # except end points
    if len(vertical_line) > 1:
        valid_vertical = True
        v_list = sorted(list(vertical_line),key=lambda x: x[0]) # sort by row
        for r,c in v_list:
            neighbors = 0
            if (r-1,c) in vertical_line:
                neighbors+=1
            if (r+1,c) in vertical_line:
                neighbors+=1
            if neighbors > 2 or (neighbors == 1 and r != v_list[0][0] and r != v_list[-1][0]):
                valid_vertical = False
                break
        if valid_vertical:
          # Check if pixels are already in a horizontal line
          for r, c in vertical_line:
            if (r,c) in visited:
              return False, set()
          return True, vertical_line

    return False, set()

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    visited = set()

    # Iterate and change output pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5:
                is_line, line_pixels = is_part_of_line(output_grid, r, c, visited)
                if is_line:
                    for line_row, line_col in line_pixels:
                        output_grid[line_row, line_col] = 3  # Change to green
                        visited.add((line_row, line_col))

    return output_grid
```
