# d687bc17 • 006 • refine_coder

---
```python
"""
Preserves a frame of blue (1) pixels and duplicates interior pixels of other colors directly below their original positions.
"""

import numpy as np

def find_frame(grid):
    # Find the bounding box of the blue (1) pixels.
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:  # No blue pixels, no frame
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, max_row, min_col, max_col)

def duplicate_interior_pixels(input_grid, frame):
    # Duplicate interior pixels (non-blue) within the frame.
    output_grid = np.copy(input_grid)
    min_row, max_row, min_col, max_col = frame

    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if input_grid[r, c] != 1:
                # Find the next available row below within the frame
                for next_row in range(r + 1, max_row + 1):
                    if output_grid[next_row,c] == 1:
                       output_grid[next_row, c] = input_grid[r, c]
                       break  # Only one duplicate per pixel
    return output_grid

def transform(input_grid):
    # Find the frame.
    frame = find_frame(input_grid)
    if frame is None:
        return input_grid  # No frame, return original grid

    # Duplicate interior pixels.
    output_grid = duplicate_interior_pixels(input_grid, frame)

    return output_grid
```
