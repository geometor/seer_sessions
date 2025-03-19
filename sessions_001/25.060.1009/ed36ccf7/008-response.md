# ed36ccf7 • 008 • refine_coder

---
```python
"""
1.  **Identify 2x2 Subgrids:** Examine all possible 2x2 subgrids within the input grid.
2. **Check for known rotation patterns**:
    * Check if subgrid matches pattern [[5, 1], [5, 8]].
    * Check if subgrid matches pattern [[5, 0], [0, 0]].
    * Check if subgrid matches pattern [[8, 5], [1, 8]]
3.  **Rotate:** If one of the patterns is found, rotate the identified subgrid 90 degrees clockwise:
    *   Top-left cell to top-right.
    *   Top-right cell to bottom-right.
    *   Bottom-right cell to bottom-left.
    *   Bottom-left cell to top-left.
4.  **Preserve Rest:** All pixels not part of the rotating subgrid remain in their original positions and retain their original colors.
5.  **No Match:** If no matching 2x2 subgrid is found, the output grid is identical to the input grid.
"""

import numpy as np

def rotate_subgrid(grid, top_left_row, top_left_col):
    """Rotates a 2x2 subgrid 90 degrees clockwise."""
    subgrid = grid[top_left_row:top_left_row+2, top_left_col:top_left_col+2]
    rotated_subgrid = np.rot90(subgrid, k=-1)  # k=-1 for clockwise rotation
    grid[top_left_row:top_left_row+2, top_left_col:top_left_col+2] = rotated_subgrid
    return grid

def check_pattern(grid, r, c, pattern):
    """Checks if the 2x2 subgrid at (r, c) matches the given pattern."""
    subgrid = grid[r:r+2, c:c+2]
    return np.array_equal(subgrid, np.array(pattern))

def transform(input_grid):
    """Transforms the input grid by rotating a 2x2 subgrid based on predefined patterns."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through all possible 2x2 subgrids
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check for each pattern
            if check_pattern(output_grid, r, c, [[5, 1], [5, 8]]):
                output_grid = rotate_subgrid(output_grid, r, c)
                return output_grid  # Rotate only the first match
            elif check_pattern(output_grid, r, c, [[5, 0], [0, 0]]):
                output_grid = rotate_subgrid(output_grid, r, c)
                return output_grid  # Rotate only the first match
            elif check_pattern(output_grid, r, c, [[8, 5], [1, 8]]):
                output_grid = rotate_subgrid(output_grid, r, c)
                return output_grid  # Rotate only the first match

    return output_grid  # Return unchanged if no pattern matches
```

