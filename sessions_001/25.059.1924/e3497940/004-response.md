# e3497940 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** the central, vertical column of gray (5) pixels.
2.  **Identify** the colored shapes (yellow/4 and green/3) that are directly adjacent to the gray column.
3.  **Remove** the entire gray column.
4.  **Remove** any empty columns that are created by removing the gray column.
5.  **Retain** the identified colored shapes (yellow and green) in their original rows.
6. The output is new grid with colored shapes.
"""

import numpy as np

def find_gray_column(grid):
    # Find the column index of the gray (5) pixels.
    for j in range(grid.shape[1]):
        if np.any(grid[:, j] == 5):
            return j
    return -1  # Should not happen in valid inputs.

def get_colored_shapes(grid, gray_column_index):
  # extracts colored shapes adjacent to gray column
    colored_pixels = []
    for i in range(grid.shape[0]):
        if grid[i, gray_column_index] == 5:
            # Check left neighbor
            if gray_column_index > 0 and grid[i, gray_column_index - 1] != 0 and grid[i, gray_column_index - 1] != 5:
                colored_pixels.append((i, gray_column_index - 1, grid[i, gray_column_index - 1]))
            # Check right neighbor
            if gray_column_index < grid.shape[1] - 1 and grid[i, gray_column_index + 1] != 0 and grid[i, gray_column_index+1] != 5:
                colored_pixels.append((i, gray_column_index + 1, grid[i, gray_column_index + 1]))
    return colored_pixels

def transform(input_grid):
    # Find central gray column index
    gray_column_index = find_gray_column(input_grid)

    # Get colored shape pixels
    colored_pixels = get_colored_shapes(input_grid, gray_column_index)

    # determine columns to keep, based on location of the colored shapes
    columns_to_keep = sorted(list(set([pixel[1] for pixel in colored_pixels])))
    # shift column numbers
    
    # initialize output_grid by copying
    output_grid = np.zeros((input_grid.shape[0], len(columns_to_keep)), dtype=int)
    
    # map old column index to new column index
    col_mapping = {old_col: new_col for new_col, old_col in enumerate(columns_to_keep)}

    # copy just those pixels to output grid using the mapping
    for x, y, color in colored_pixels:
      output_grid[x, col_mapping[y]] = color

    return output_grid
```
