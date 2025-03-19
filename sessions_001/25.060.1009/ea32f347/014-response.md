# ea32f347 • 014 • refine_coder

---
```python
"""
Transforms an input grid based on the presence and position of grey (5) pixels.

1.  **Grey Pixel Transformation:**
    *   IF a vertical line of grey pixels exists:
        *   Change the color of the vertical line pixels to blue.
        *   Change the color of grey pixels to the *left* of the line to yellow.
        *   Change the color of grey pixels to the *right* of the line to red.
    *   ELSE IF there are ANY grey pixels (but no vertical line):
        *   change all grey pixels to blue.
    *    ELSE:
        *   make no change.

2.  **Other color transformations**
    *   No other colors should change.
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

    # Check if a vertical line exists
    if vertical_line:
        # Color vertical line pixels blue
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
    else:
        # If no vertical line, check for any grey pixels
        grey_pixels = np.argwhere(input_grid == 5)
        if len(grey_pixels) > 0:
            # Change all grey pixels to blue
            for r, c in grey_pixels:
                output_grid[r, c] = 1

    return output_grid
```
