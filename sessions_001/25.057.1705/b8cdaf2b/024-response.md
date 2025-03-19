# b8cdaf2b • 024 • refine_coder

---
```python
"""
1.  **Initialize:** Create an output grid the same size as the input grid, filled with zeros (representing white).
2. **Iterate:** Iterate through *all* cells of the input grid.
3. **Observe Yellow and Red Clusters:** For each cell in the input that is part of a yellow 2x2 square,
    do not assume adjacency between the yellow and red 2 x 2 squares.
4. **Determine New Yellow Position:** If a cell is part of 2x2 yellow square, place a yellow
pixel in the output.
5. **Row positioning:** if the yellow 2x2 occupies rows 4 and 5 in the input, put a yellow
pixel on row 0 of the same column in the output.
6. **Row positioning:** if the yellow 2x2 occupies rows 2 and 3, or 1 and 2, or 0
   and 1 in the input, put a yellow pixel on row 2 of the same column in the output.

7.  **Output:** The modified grid is the final output.
"""

import numpy as np

def find_2x2_squares(grid, color):
    """Finds the top-left corner coordinates of all 2x2 squares of the given color."""
    rows, cols = grid.shape
    squares = []
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] == color and
                grid[r + 1, c] == color and
                grid[r, c + 1] == color and
                grid[r + 1, c + 1] == color):
                squares.append((r, c))
    return squares

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find all 2x2 yellow squares
    yellow_squares = find_2x2_squares(input_grid, 4)

    # Determine output row and place yellow pixels
    for r, c in yellow_squares:
        if r >= rows-2 :
          output_row = 0
        else:
          output_row = 2
        output_grid[output_row,c] = 4
        output_grid[output_row,c+1] = 4

    return output_grid
```
