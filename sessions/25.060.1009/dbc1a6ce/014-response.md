# dbc1a6ce • 014 • refine_coder

---
```python
"""
Identify all blue (1) pixels within the input grid. For each blue pixel, examine its four directly adjacent neighbors (up, down, left, and right). If a neighboring pixel is white (0), change its color to azure (8). The dimensions of the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is blue (1)
            if output_grid[r, c] == 1:
                # Check and fill adjacent cells (up, down, left, right)
                neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
                for nr, nc in neighbors:
                    if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                        output_grid[nr, nc] = 8

    return output_grid
```

