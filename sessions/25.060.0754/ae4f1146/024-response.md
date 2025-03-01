# ae4f1146 • 024 • refine_coder

---
```python
"""
Extracts a 3x3 subgrid from the input grid. The subgrid's location is determined
by finding the bounding box of the non-white pixels, and then using the top-left
corner of that bounding box as the top-left corner of the 3x3 subgrid. If
the bounding box is larger than 3x3 the top-left 3x3 corner is always returned,
if it's smaller, then it is padded with white (0)
"""

import numpy as np

def get_bounding_box(grid):
    """Finds the bounding box of the non-white pixels in a grid."""
    grid = np.array(grid)
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:
        return None  # Handle cases with no non-white pixels

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)
    return (min_row, min_col, max_row - min_row + 1, max_col - min_col + 1)

def transform(input_grid):
    """
    Extracts a 3x3 subgrid based on the bounding box of non-white pixels.
    """
    input_array = np.array(input_grid)
    bounding_box = get_bounding_box(input_array)

    if bounding_box:
        min_row, min_col, _, _ = bounding_box
        # Extract up to a 3x3 subgrid, handling boundary conditions
        output_grid = input_array[min_row:min_row+3, min_col:min_col+3]

    else: #if no bounding box, return all white
        output_grid = np.zeros((3, 3), dtype=int)

    # Pad with zeros if the extracted subgrid is smaller than 3x3.
    rows, cols = output_grid.shape
    if rows < 3 or cols < 3:
        padded_grid = np.zeros((3, 3), dtype=int)
        padded_grid[:rows,:cols] = output_grid
        output_grid = padded_grid

    return output_grid.tolist()
```
