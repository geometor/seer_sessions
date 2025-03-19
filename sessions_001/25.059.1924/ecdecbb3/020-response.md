# ecdecbb3 • 020 • refine_coder

---
```python
"""
1.  **Red Column Extension:** Identify all columns in the input grid that contain at least one red (2) pixel. For each of these identified columns, create a corresponding column in the output grid filled entirely with red pixels. This red column spans the full height of the output grid.

2.  **Azure Line Identification:** Identify all rows in the input grid that consist of a complete horizontal line of azure (8) pixels.

3.  **Azure Pixel Placement:**
    *   For each identified azure line (row):
        *   Check each column of the grid, starting from the leftmost column (index 0).
        *   If a column does *not* contain a red pixel (i.e., it's not one of the extended red columns), place a single azure pixel at the intersection of the current azure row and that column.
        *   Stop after placing one azure pixel for the current azure line.
        *   If all columns are red columns, no azure pixel is placed for the current azure line.

4.  Fill the rest of the output grid that does not contain a red or azure pixel with the background color 0/white.
"""

import numpy as np

def get_red_pixel_columns(input_grid):
    """Finds the columns containing red pixels."""
    red_cols = []
    for col in range(input_grid.shape[1]):
        for row in range(input_grid.shape[0]):
            if input_grid[row, col] == 2:
                red_cols.append(col)
                break  # Move to the next column after finding a red pixel
    return red_cols

def get_azure_lines(input_grid):
    """Finds the rows containing azure lines."""
    azure_rows = []
    for row in range(input_grid.shape[0]):
        if all(input_grid[row, :] == 8):
            azure_rows.append(row)
    return azure_rows

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Red Column Extension
    red_columns = get_red_pixel_columns(input_grid)
    for col in red_columns:
        for row in range(rows):
            output_grid[row, col] = 2

    # 2. Azure Line Identification
    azure_lines = get_azure_lines(input_grid)

    # 3. Azure Pixel Placement
    for azure_row in azure_lines:
        for col in range(cols):
            if col not in red_columns:
                output_grid[azure_row, col] = 8
                break  # Stop after placing one azure pixel

    return output_grid
```
