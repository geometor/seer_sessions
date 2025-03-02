# ea32f347 • 012 • refine_coder

---
```python
"""
Transforms an input grid by identifying grey (5) pixels. If a vertical line of grey pixels exists, those pixels are changed to blue (1).  Grey pixels to the left of the vertical line are changed to yellow (4), and those to the right are changed to red (2). If no vertical line of grey pixels is found, no changes are made.
"""

import numpy as np

def find_vertical_line(grid):
    """
    Finds the longest vertical line of grey pixels in the grid.
    Returns a list of (row, col) tuples for the line, or an empty list if none found.
    """
    rows, cols = grid.shape
    grey_pixels = np.argwhere(grid == 5)
    if len(grey_pixels) == 0:
        return []

    col_counts = {}  # Count grey pixels in each column
    for r, c in grey_pixels:
        if c not in col_counts:
            col_counts[c] = []
        col_counts[c].append(r)

    longest_col = -1
    longest_col_len = 0

    for col, row_list in col_counts.items():
        row_list.sort()
        local_max_len = 0
        max_len = 0
        for i in range(len(row_list)):
            if i == 0:
                local_max_len = 1
            elif row_list[i] == row_list[i - 1] + 1:
                local_max_len += 1
            else:
                local_max_len = 1
            max_len = max(max_len, local_max_len)
            
        if max_len > longest_col_len:
            longest_col_len = max_len
            longest_col = col

    if longest_col_len == 0:
        return []

    # Build vertical segment from longest column
    vertical_segment = []

    # find the starting row of the longest segment in the column
    row_list = col_counts[longest_col]
    row_list.sort()
    start_row = -1
    for i in range(len(row_list)):
        if i == 0:
            start_row = row_list[i]
        elif row_list[i] == row_list[i-1] + 1:
          pass # continue
        else:
            if (row_list[i-1] - start_row + 1) == longest_col_len:
                break # found it
            else:
              start_row = row_list[i]

    for r in range(start_row, start_row + longest_col_len):
        vertical_segment.append((r, longest_col))

    return vertical_segment

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find vertical line of grey pixels
    vertical_line = find_vertical_line(input_grid)

    # Color vertical line pixels blue
    if vertical_line:
        for r, c in vertical_line:
            output_grid[r, c] = 1

        # Color other grey pixels based on position relative to vertical line
        grey_pixels = np.argwhere(input_grid == 5)
        vertical_col = vertical_line[0][1]
        for r, c in grey_pixels:
            if c < vertical_col:
                output_grid[r, c] = 4  # Yellow for left
            elif c > vertical_col:
                output_grid[r, c] = 2  # Red for right

    return output_grid
```
