# 8f2ea7aa • 018 • refine_coder

---
```python
"""
The transformation rule involves identifying 2x2 magenta (color 6) squares in the input grid. 
The output grid maintains the same dimensions and background (color 0). 
The rule replicates the 2x2 magenta squares based on these spatial conditions:
1. If a 2x2 magenta square is present and there is an even number of rows or an even number of columns, 
   the square is replicated to fill every available 2x2 section of the grid lines.
2. If a 2x2 magenta square is present and there is an odd number of both rows and columns, 
   the square appears only where it was in the original image.
"""

import numpy as np

def find_2x2_squares(grid, color):
    """
    Finds all 2x2 squares of the specified color in the grid.
    """
    squares = []
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                squares.append((r, c))
    return squares

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid, ensures same dimensions
    output_grid = np.zeros_like(input_grid)

    # Find 2x2 magenta squares
    magenta_squares = find_2x2_squares(input_grid, 6)

    if magenta_squares:
        #if even rows or even cols, fill with 2x2 at every opportunity
        if output_grid.shape[0] %2 == 0 or output_grid.shape[1] % 2 == 0:
            for r in range(0, output_grid.shape[0] -1, 2):
                for c in range(0,output_grid.shape[1] -1, 2):
                  output_grid[r:r+2, c:c+2] = 6
        else:
          #copy the input to output
          output_grid = np.copy(input_grid)

    return output_grid
```
