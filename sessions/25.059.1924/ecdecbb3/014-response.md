# ecdecbb3 • 014 • refine_coder

---
```python
"""
1.  **Identify Azure Lines:** Locate the two vertical azure (8) lines in the input grid. These lines act as boundaries.
2.  **Locate Red Region:** Find the horizontal red (2) region (a contiguous block of red pixels in a single row). Note its starting column, ending column, and row number.
3.  **Expand Red Region:** Extend the red region horizontally:
    *   **Left:** Extend to the left until the column *of* the left azure line.
    *   **Right:** Extend to the right until the column *of* the right azure line.
4. **Place Azure Markers** On the row immediately below the red region, if the row exists:
    * Place a single azure pixel in the column where the *original* red region began, but only if that column position falls *within* the azure columns.
    * Place a single azure pixel in the column where the *original* red region ended, but only if that column position falls *within* the azure columns.
5.  If there are other, disjoint red regions on other rows, repeat steps 2-4.
"""

import numpy as np

def find_vertical_lines(grid, color):
    lines = []
    for col in range(grid.shape[1]):
        if all(grid[:, col] == color):
            lines.append(col)
    return lines

def find_red_regions(grid):
    red_regions = []
    for row in range(grid.shape[0]):
        start_col = None
        for col in range(grid.shape[1]):
            if grid[row, col] == 2:
                if start_col is None:
                    start_col = col
            elif start_col is not None:
                red_regions.append((row, start_col, col - 1))
                start_col = None
        if start_col is not None:
            red_regions.append((row, start_col, grid.shape[1] - 1))
    return red_regions

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find azure lines
    azure_lines = find_vertical_lines(input_grid, 8)
    if len(azure_lines) != 2:
        return output_grid # Requires exactly two azure lines

    left_azure, right_azure = azure_lines

    # find the red regions
    red_regions = find_red_regions(input_grid)

    for red_row, min_col, max_col in red_regions:

        # Expand red region horizontally
        # expand left
        for col in range(min_col, left_azure -1, -1):
          output_grid[red_row, col] = 2
        # expand right
        for col in range(max_col, right_azure + 1):
          output_grid[red_row, col] = 2

        # Fill azure below expanded region ends, if next to an azure line
        fill_row = red_row + 1
        if fill_row < output_grid.shape[0]:
            # check left fill. Original min_col
            if min_col >= left_azure and min_col <= right_azure :
                output_grid[fill_row, min_col] = 8

            # check right fill. Original max_col
            if max_col >= left_azure and max_col <= right_azure:
                output_grid[fill_row, max_col] = 8

    return output_grid
```
