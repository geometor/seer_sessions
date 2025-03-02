# feca6190 • 002 • example_5 • investigate_coder

---
```python
"""
Expands a 1xN input grid into an NxN output grid, projecting non-zero values diagonally in both directions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 1xN input grid into an NxN output grid by projecting non-zero values diagonally.

    Args:
        input_grid: A 1xN list representing the input grid.

    Returns:
        An NxN list of lists representing the output grid.
    """
    n = len(input_grid)
    output_grid = np.zeros((n, n), dtype=int)

    # Iterate through the input grid
    for i, value in enumerate(input_grid):
        # If the value is non-zero, project it diagonally
        if value != 0:
            # Project diagonally top-right to bottom-left
            for j in range(n):
                if 0 <= i - j < n :
                    output_grid[j, i-j] = value
                if 0 <= i + j < n:
                    output_grid[j, i + j] = value


    return output_grid.tolist()
```
