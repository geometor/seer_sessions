# b230c067 • 012 • refine_coder

---
```python
"""
1.  **Identify the Azure Block:** Find the contiguous block of azure (8) pixels. This block forms a rectangle.
2.  **Recolor Top Row:** Change the color of the pixels in the top row of the identified azure block to red (2).
3.  **Recolor Remaining Rows:** Change the color of all remaining azure pixels in the block (those *not* in the top row) to blue (1).
4.  **Output:** The resulting grid is the output. All pixels not part of the initial azure block retain their original color.
"""

import numpy as np

def find_azure_block(grid):
    """Finds the bounding box of the contiguous azure (8) block."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 8:
                min_row = min(min_row, i)
                min_col = min(min_col, j)
                max_row = max(max_row, i)
                max_col = max(max_col, j)

    if min_row == rows:  # No azure block found
        return None

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)  # Initialize output grid
    azure_block = find_azure_block(output_grid)

    if azure_block is None:  # Handle cases with no azure pixels
        return output_grid

    min_row, min_col, max_row, max_col = azure_block

    # Recolor top row to red (2)
    for j in range(min_col, max_col + 1):
        output_grid[min_row, j] = 2

    # Recolor remaining rows to blue (1)
    for i in range(min_row + 1, max_row + 1):
        for j in range(min_col, max_col + 1):
            output_grid[i, j] = 1

    return output_grid
```
