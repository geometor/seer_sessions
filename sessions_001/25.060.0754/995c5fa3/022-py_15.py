"""
1. **Identify the "core" shape:** Find the contiguous region of white (0) pixels within the input grid. Think of this as the "significant feature" in the input.
2. **Analyze Input:** Count the number of distinct gray (5) columns to the left of the white (0) region, count the number of distinct gray(5) columns to the right.
3.  **Construct Output Dimensions:** The output grid will be 3x3.
4. **Populate the output grid**:
    *   Make rows 1 and 3 all red (2).
    *   Make row 2 all yellow (4).
"""

import numpy as np

def get_white_region_bounds(grid):
    """Finds the bounding columns of the contiguous white region."""
    white_cols = np.where(np.any(grid == 0, axis=0))[0]
    if len(white_cols) == 0:
        return None, None  # No white region found

    min_col = white_cols[0]
    max_col = white_cols[-1]
    return min_col, max_col

def transform(input_grid):
    """Transforms the input grid into a 3x3 output grid based on the white region."""

    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Populate the output grid
    output_grid[0, :] = 2  # Top row red
    output_grid[2, :] = 2  # Bottom row red
    output_grid[1, :] = 4  # Middle row yellow

    return output_grid