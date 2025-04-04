# ecdecbb3 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Red Pixel Replication:** For each red (2) pixel in the input, replicate it vertically downwards and upwards to create a column of red pixels. The column spans from row 0 and down to the max length of original grid.

2.  **Azure Line Interaction:** For each horizontal azure (8) line in the input, examine each of its constituent azure pixels, specifically checking its column.

3. **Combination:**
    - Check for overlap between the red pixel columns from Step 1, and the existing azure pixels.
    - If an azure pixel in the input shares the same column index as a replicated red pixel column, keep the red color.
    - If an azure line pixel is not located in the column of replicated red, keep the azure pixel in the output at the input grid position.
4. The final output is composed of a the white background, plus the modified pattern of red pixels and blue lines.
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

    # 1. Red Pixel Replication
    red_columns = get_red_pixel_columns(input_grid)
    for col in red_columns:
        for row in range(rows):
            output_grid[row, col] = 2

    # 2 & 3. Azure Line Interaction and Combination
    azure_lines = get_azure_lines(input_grid)
    for row in azure_lines:
      for col in range(cols):
        if col not in red_columns:
          output_grid[row,col] = 8
        

    return output_grid
```
