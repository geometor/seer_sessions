# 9dfd6313 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all non-zero pixels (objects) in the input grid and note their color and original (x, y) coordinates.

2.  **Column Swap.** Swap the values in column 3 with the values in column 1.

3.  **Transpose:** Treat the grid as a matrix and transpose it.  This means swapping rows and columns (element (r, c) becomes element (c, r)).
"""

import numpy as np

def swap_columns(grid, col1, col2):
    """Swaps two columns in a NumPy grid."""
    grid[:, [col1, col2]] = grid[:, [col2, col1]]
    return grid

def transpose(grid):
    """Transposes a NumPy grid."""
    return np.transpose(grid)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # Convert to NumPy array for easier manipulation
    output_grid = np.array(input_grid)

    # Column Swap. Swap column 3 with column 1 (0-indexed, so 2 and 0)
    output_grid = swap_columns(output_grid, 0, 2)

    # Transpose the grid
    output_grid = transpose(output_grid)
    
    return output_grid.tolist()
```
