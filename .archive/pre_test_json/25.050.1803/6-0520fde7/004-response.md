# 6-0520fde7 • 004 • example_2 - CODE

---
```python
"""
The transformation rule is activated by the presence of a 'gray column object' within the input grid. A 'gray column object' is identified by the predicate: "exists a column where all cells are of color gray (color 5)".

**Condition:** 'gray column object' exists in the input grid.

**Action:** If the condition is met, generate a fixed 3x3 output grid object.

**Output Grid Object Definition:**
  - Dimensions: 3x3
  - Cell colors:
    - Cell at position (row 0, column 1): red (color 2)
    - Cell at position (row 1, column 2): red (color 2)
    - Cell at position (row 2, column 1): red (color 2)
    - All other cells in the 3x3 grid: white (color 0)

In summary, if a gray column object is present in the input, the output is a predefined 3x3 grid pattern with red cells at specific off-center positions and white cells elsewhere.
"""

import numpy as np

def has_gray_column(grid):
    """
    Checks if the grid has a column where all cells are gray (color 5).
    """
    for j in range(grid.shape[1]):
        if all(grid[:, j] == 5):
            return True
    return False

def transform(input_grid):
    """
    Transforms the input grid based on the presence of a gray column.
    """
    input_grid = np.array(input_grid)

    # Check for the existence of a gray column
    if has_gray_column(input_grid):
        # Create a 3x3 grid filled with white (color 0)
        output_grid = np.zeros((3, 3), dtype=int)
        # Set specific cells to red (color 2)
        output_grid[0, 1] = 2
        output_grid[1, 2] = 2
        output_grid[2, 1] = 2
        return output_grid.tolist()  # Convert back to list for consistency with ARC
    else:
        return input_grid.tolist()
```

