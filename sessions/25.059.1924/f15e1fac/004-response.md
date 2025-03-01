# f15e1fac • 004 • example_1 • investigate_coder

---
```python
"""
Transformation Rule:

1. **Identify Existing Elements:** Locate all existing azure (8) and red (2) pixels in the input grid.
2. **Red row selection:** For all rows that have a red(2) pixel, perform step 3, else perform step 4.
3. **Red Row Azure Addition:** In the rows that contain a Red(2) pixel. For every azure(8) pixel, add an azure(8) in every cell below it, extending the 'line' of azure color down to the bottom of the grid.
4. **Azure Addition:** For every column that contains azure, extend the lowest azure pixel down to the end of the column.
5. **Result:** Maintain the Red pixels in their original Y position, regardless of other changes.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find rows with red pixels
    red_rows = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                red_rows.add(r)

    # Process each column
    for c in range(cols):
        azure_indices = [r for r in range(rows) if input_grid[r, c] == 8]
        if azure_indices:
            lowest_azure = max(azure_indices)

            for r in range(rows):
                if r in red_rows:
                    # red present, extend the azure to bottom of the grid
                    if input_grid[r,c] == 8:
                        for r_below in range (r, rows):
                            output_grid[r_below,c] = 8

                elif r > lowest_azure:
                        # Extend azure downwards if not a red row
                        output_grid[r,c] = 8
    return output_grid
```
