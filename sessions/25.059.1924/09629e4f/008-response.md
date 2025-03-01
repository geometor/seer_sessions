# 09629e4f • 008 • refine_coder

---
```python
"""
Transforms the input grid based on horizontal grey (5) lines:

1.  **Identify Grey Lines:** Find all horizontal lines that consist entirely of grey (5) pixels.
2.  **Divide into Regions:**  Use the grey lines to divide the grid into regions.
    *   No grey lines: The entire grid is a single region.
    *   One grey line: Two regions (top and bottom).
    *   Two grey lines: Three regions (top, middle, bottom).
3.  **Transform Regions Based on Count:**
    *   If there are *two or more* regions:
        *   The *topmost* region: Create a 3x3 block of red (2) pixels at the top-left corner. All other pixels become black (0).
        *   The *bottommost* region: Create a 3x3 block of magenta (6) pixels at the top-left corner. All other pixels become black (0).
        *   Regions between the top and bottom are not transformed.
    *   If there is only *one* region (the entire grid), no transformation is applied.
4.  **Retain all Gray Lines:** Ensure all grey lines are preserved in the output.
"""

import numpy as np

def get_grey_lines(grid):
    """Finds rows that are entirely grey (5)."""
    return np.where((grid == 5).all(axis=1))[0]

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    grey_lines = get_grey_lines(input_grid)
    num_regions = len(grey_lines) + 1

    if num_regions >= 2:
        # Topmost region transformation
        top_region_end = grey_lines[0]
        output_grid[:top_region_end, :3] = 2  # 3x3 red block
        output_grid[:top_region_end, 3:] = 0  # Clear the rest

        # Bottommost region transformation
        bottom_region_start = grey_lines[-1] + 1
        output_grid[bottom_region_start:, :3] = 6  # 3x3 magenta block
        output_grid[bottom_region_start:, 3:] = 0  # Clear the rest

    # Ensure grey lines are retained
    for row in grey_lines:
        output_grid[row, :] = 5

    return output_grid
```
