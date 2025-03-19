# db3e9e38 • 014 • refine_coder

---
```python
"""
1. **Identify Anchor:** Find the topmost, then leftmost, orange (7) pixel in the input grid.
2. **Construct Inverse "L":** Starting from the anchor pixel, create an inverse "L" shape.
3. **Orientation:** The "L" extends upwards and to the left of the anchor.
4. **Color Alternation:** The "L" shape is filled with alternating orange (7) and azure (8) pixels. The anchor pixel itself does *not* change. The first pixel placed (adjacent to the anchor) should be orange.
5. **Size:** The horizontal size in examples 1 and 2 is correlated with orange line height, and the vertical line has length N-1, where N is the number of rows of input grid.
"""

import numpy as np

def find_anchor(grid):
    # Find the topmost, then leftmost, orange (7) pixel.
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 7:
                return r, c
    return None, None

def get_vertical_orange_line_length(grid, start_row, start_col):
    # Helper function to get the vertical orange line length from the anchor
    if start_row is None or start_col is None:
        return 0

    rows, _ = grid.shape
    line_length = 0
    for r in range(start_row, rows):
        if grid[r, start_col] == 7:
            line_length += 1
        else:
            break
    return line_length


def transform(input_grid):
    # Initialize output_grid as a copy of input.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the anchor point (topmost, leftmost orange pixel).
    anchor_row, anchor_col = find_anchor(output_grid)

    if anchor_row is None:
        return output_grid  # No transformation if no anchor

    # get the length of the vertical line
    vertical_line_length = get_vertical_orange_line_length(input_grid, anchor_row, anchor_col)

    # Construct the inverse "L".
    # Vertical part
    for r in range(anchor_row -1, -1, -1):
      output_grid[r,anchor_col ] = 7 if (anchor_row - r) % 2 != 0 else 8

    #Horizontal part
    h_length = vertical_line_length if vertical_line_length > 0 else 1
    for c in range(anchor_col - 1, max(anchor_col-h_length-1,-1), -1):
      output_grid[anchor_row, c] = 7 if (anchor_col - c) % 2 != 0 else 8

    return output_grid
```
