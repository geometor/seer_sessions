# 05269061 • 012 • refine_coder

---
```python
"""
1.  **Create Output Grid:** Create an output grid with the same dimensions (height and width) as the input grid.
2.  **Ignore Input Values:** Disregard the numerical values present in the input grid. The input grid serves only to determine the size of the output.
3. **Checkerboard Pattern:** Create output by filling the grid with the two colors 1 (blue) and 2 (red) forming a 2 color checkerboard.
4.  **Starting Color:** Always start with color 2 (red) in the top-left cell (row 0, column 0) of the output grid.
5. **Fill based on index:** Determine whether to fill cells based on the sum of its row, and column value:
    *   If `(row + column)` is even, fill the cell with the color 2 (red).
    *   If `(row + column)` is odd, fill the cell with the color 1 (blue).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid to a checkerboard pattern of 1s and 2s."""

    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the output grid
    for row in range(rows):
        for col in range(cols):
            # If (row + column) is even, fill with 2 (red)
            if (row + col) % 2 == 0:
                output_grid[row, col] = 2
            # If (row + column) is odd, fill with 1 (blue)
            else:
                output_grid[row, col] = 1

    return output_grid
```

