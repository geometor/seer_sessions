# 3befdf3e • 020 • refine_coder

---
```python
"""
1.  **Identify the Inner Object:** Find the contiguous blue (color 1) rectangle within the input grid.
2.  **Expand Perimeter:** Expand the boundaries of the blue rectangle by one pixel in all directions (horizontally, vertically, and diagonally).
3.  **Determine Fill Color:** Identify the color of the *outer object*. The outer object will have the majority of the pixels surrounding the blue rectangle, but doesn't have to be a complete or perfect shape.
4.  **Apply Fill:** Color the expanded perimeter with the identified fill color.
5.  **Output:** The output grid consists of the original blue rectangle and its expanded perimeter, now filled with the outer object's color.
"""

import numpy as np
from collections import Counter

def find_rectangle(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def expand_perimeter(grid, rect):
    min_row, max_row, min_col, max_col = rect
    expanded_region = []
    for r in range(min_row - 1, max_row + 2):
        for c in range(min_col - 1, max_col + 2):
            if (min_row <= r <= max_row) and (min_col <= c <= max_col):
              continue #skip the original object
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]:
                expanded_region.append((r, c))
    return expanded_region

def get_adjacent_colors(grid, expanded_region):
    colors = []
    for r, c in expanded_region:
        colors.append(grid[r,c])
    color_counts = Counter(colors)
    # remove 0 if present, which are background
    if 0 in color_counts:
      del color_counts[0]

    if color_counts.most_common():
      return color_counts.most_common(1)[0][0]
    else:
       return None


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Identify Inner Object (blue rectangle)
    inner_rectangle = find_rectangle(input_grid, 1)  # Blue

    if inner_rectangle is None:
      return output_grid

    # Expand Perimeter
    expanded_region = expand_perimeter(input_grid, inner_rectangle)

    # Determine Fill Color (most common adjacent color)
    fill_color = get_adjacent_colors(input_grid, expanded_region)

    if fill_color is None:
      return output_grid

    # Apply Fill
    for r, c in expanded_region:
        output_grid[r, c] = fill_color

    #fill the inner rectangle
    if inner_rectangle:
      min_row, max_row, min_col, max_col = inner_rectangle
      output_grid[min_row:max_row+1, min_col:max_col+1] = 1

    return output_grid
```
