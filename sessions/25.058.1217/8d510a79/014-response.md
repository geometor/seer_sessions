# 8d510a79 • 014 • refine_coder

---
```python
"""
1.  **Identify the Horizontal Gray Line:** Search the input grid for a horizontal line (row) where all pixels are gray (value 5). Note the row index if found.
2.  **Conditional Reflection:**
    *   **If a gray line exists:** Vertically reflect the grid's contents across this gray line.  For each row *above* the gray line, its contents are copied to the row that is an equal distance *below* the gray line. The gray line itself remains unchanged.
    * **If a gray line does not exist:** The output grid is identical to the input grid.
"""

import numpy as np

def find_gray_line(grid):
    """Finds the row index of a horizontal gray line, if it exists."""
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1  # Return -1 if no gray line is found

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    gray_line_row = find_gray_line(input_grid)

    if gray_line_row != -1:
        # Perform vertical reflection
        height = input_grid.shape[0]
        for j in range(input_grid.shape[1]):
            for i in range(gray_line_row):
                # Calculate the reflected index
                reflected_i = 2 * gray_line_row - i
                # Check bounds before copying
                if 0 <= reflected_i < height:
                     output_grid[reflected_i, j] = input_grid[i, j]
    else:
        # Output is identical to input
        pass # output_grid is already a copy of input_grid

    return output_grid
```
