# 272f95fa • 006 • refine_coder

---
```python
"""
1.  **Identify Azure Lines:** Find all horizontal and vertical lines consisting of azure (8) pixels within the input grid. A valid azure line must also contain at least one white (0) pixel.
2.  **Partition into Regions:** The azure lines partition the grid into rectangular regions.
3.  **Fill Regions by Position:**
    *   **Top Region:** The region *above* the uppermost horizontal azure line is filled with red (2).
    *   **Bottom Region:** The region *below* the lowermost horizontal azure line is filled with blue (1).
    *   **Iterate Between Horizontal Lines:** For each pair of consecutive horizontal azure lines, fill regions defined by vertical lines:
        *   **Left Region:** The region to the *left* of the leftmost vertical azure line is filled with yellow (4).
        *   **Middle Region:** The region *between* the leftmost and rightmost vertical azure lines is filled with magenta (6).
        *   **Right Region:** The region to the *right* of the rightmost vertical azure line is filled with green (3).
"""

import numpy as np

def find_azure_lines(grid):
    # Find the row and column indices where azure (8) lines exist.
    # A valid azure line must also contain at least one white (0) pixel.
    rows, cols = grid.shape
    azure_rows = []
    azure_cols = []

    for r in range(rows):
        if np.any(grid[r, :] == 8):
            if len(set(grid[r, :])) <= 2 and 0 in grid[r,:]:
                azure_rows.append(r)

    for c in range(cols):
        if np.any(grid[:, c] == 8):
            if len(set(grid[:, c])) <= 2 and 0 in grid[:,c]:
                azure_cols.append(c)

    return azure_rows, azure_cols

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.full(input_grid.shape, 0)  # Initialize with white (0)
    rows, cols = output_grid.shape

    # Find azure lines
    azure_rows, azure_cols = find_azure_lines(input_grid)

    # Restore azure lines.
    for r in azure_rows:
        output_grid[r, :] = input_grid[r, :]
    for c in azure_cols:
        output_grid[:, c] = input_grid[:, c]

    # Fill Regions by Position
    if azure_rows:
        # Top regions (red)
        output_grid[0:azure_rows[0], :] = 2

        # Bottom region (blue)
        output_grid[azure_rows[-1] + 1:, :] = 1

    # Iterate Between Horizontal Lines
    if len(azure_rows) > 1:
        for i in range(len(azure_rows) - 1):
            # Fill regions between consecutive horizontal lines
            if azure_cols:

                # Leftmost region (yellow)
                output_grid[azure_rows[i] + 1:azure_rows[i + 1], :azure_cols[0]] = 4

                if len(azure_cols) > 1:
                    # Middle region (magenta)
                    output_grid[azure_rows[i] + 1:azure_rows[i + 1], azure_cols[0] + 1:azure_cols[-1]] = 6
                    # Rightmost region (green)
                    output_grid[azure_rows[i] + 1:azure_rows[i + 1], azure_cols[-1] + 1:] = 3
                else:
                     # Only one vertical line
                    output_grid[azure_rows[i] + 1:azure_rows[i+1], azure_cols[0] + 1:] = 6

            else:
                #No vertical lines
                pass

    elif len(azure_rows) == 1:
        # Fill regions below a single horizontal line
        if azure_cols:
            # Leftmost region (yellow)
            output_grid[azure_rows[0]+1:, :azure_cols[0]] = 4

            if len(azure_cols) > 1:
              # Middle region (magenta)
              output_grid[azure_rows[0]+1:, azure_cols[0]+1:azure_cols[-1]] = 6

              # Rightmost region (green)
              output_grid[azure_rows[0]+1:, azure_cols[-1]+1:] = 3
            else:
                output_grid[azure_rows[0] + 1:, azure_cols[0]+1:] = 6

    return output_grid.tolist()
```
