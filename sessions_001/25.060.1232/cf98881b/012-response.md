# cf98881b • 012 • refine_coder

---
```python
"""
1. **Find the Anchor:** Locate the top-leftmost yellow (color value 4) pixel within the input grid. This pixel serves as the anchor point for the transformation.
2.  **Attempt Subgrid Extraction:** Attempt to extract a 4x4 subgrid from the input grid. The top-left corner of this subgrid should be the location of the anchor pixel found in step 1.
3.  **Boundary Check:** Before extracting the subgrid, check if a 4x4 area starting at the anchor point would extend beyond the boundaries of the input grid.
4.  **Conditional Output:**
    *   If the 4x4 subgrid can be extracted without exceeding the input grid's boundaries, the output grid is this extracted subgrid.
    *   If extracting the 4x4 subgrid would exceed the boundaries, the output grid is an empty grid (0x0).
"""

import numpy as np

def find_top_leftmost_color(grid, color):
    # Iterate through the grid to find the top-leftmost occurrence of the specified color.
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                return (r_idx, c_idx)
    return None  # Return None if the color is not found.

def transform(input_grid):
    # Convert input_grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the top-leftmost yellow pixel (color 4).
    top_left_corner = find_top_leftmost_color(input_grid, 4)

    # If no yellow pixel is found, return an empty grid.
    if top_left_corner is None:
        return np.zeros((0, 0), dtype=int)

    # Attempt to extract the 4x4 subgrid.
    start_row, start_col = top_left_corner
    end_row = start_row + 4
    end_col = start_col + 4

    # Boundary check: If subgrid exceeds input_grid bounds, return 0x0 grid.
    if end_row > input_grid.shape[0] or end_col > input_grid.shape[1]:
        return np.zeros((0, 0), dtype=int)

    # Extract and return the subgrid.
    output_grid = input_grid[start_row:end_row, start_col:end_col]
    return output_grid.tolist()
```
