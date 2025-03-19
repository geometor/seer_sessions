# cce03e0d • 011 • refine_coder

---
```python
"""
1.  **Measure Input:** Determine the height and width of the input grid. Let this value be *N*.
2.  **Create Output Grid:** Create a new square grid with dimensions 3*N x 3*N. Initialize all cells to white (0).
3.  **Place Original:** Copy the original input grid and place it in the top-right corner of the output grid. The top-left corner of input will correspond to cell(*2N*, *2N*) in the new grid.
4.  **Place Mirrored:** Copy the original input grid and place a mirrored copy in the bottom left corner. The position of the mirrored copy will be from (0,0) to (*N*,*N*).
5.  **Return the output grid.**
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""

    # 1. Measure Input
    n = len(input_grid)

    # 2. Create Output Grid
    output_grid = np.zeros((3 * n, 3 * n), dtype=int)

    # 3. Place Original in top-right
    output_grid[0:n, 2*n:3*n] = input_grid

    # 4. Place Mirrored in bottom-left
    output_grid[2*n:3*n, 0:n] = input_grid
    
    # 5. Return the output grid
    return output_grid
```
