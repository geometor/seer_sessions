```python
"""
1.  **Identify '7's:** Find all pixels with the color orange (7).

2.  **Conditional '7' Change:**
    *   A '7' pixel changes to gray (5) if and only if it is directly adjacent (horizontally or vertically, *not* diagonally) to an azure (8) pixel or to any pixel of a different color, other than 1.

3.  **Identify '1's:** Locate pixels colored blue (1).

4.  **Conditional '1' change**
    * A '1' pixel should be changed to gray (5) if and only if it is directly adjacent (horizontally or vertically, *not diagonally*) to any other color, including 8.

5. **Identify '8's** Locate pixels colored azure (8).
   
6.  **Conditional '8' change**
    * An '8' pixel *does not* change.

7. **Preservation:** All other pixels retain their original colors.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to check neighbors horizontally and vertically
    def get_hv_neighbors(r, c):
        neighbors = []
        if r > 0:
            neighbors.append((r - 1, c))  # Up
        if r < rows - 1:
            neighbors.append((r + 1, c))  # Down
        if c > 0:
            neighbors.append((r, c - 1))  # Left
        if c < cols - 1:
            neighbors.append((r, c + 1))  # Right
        return neighbors

    # Conditional '7' Change
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 7:
                neighbors = get_hv_neighbors(r, c)
                for nr, nc in neighbors:
                    if input_grid[nr, nc] == 8 or (input_grid[nr,nc] != 7 and input_grid[nr,nc] != 1):
                        output_grid[r, c] = 5
                        break  # Change only once

    # Conditional '1' change
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 1:
          neighbors = get_hv_neighbors(r,c)
          for nr, nc in neighbors:
            if input_grid[nr, nc] != 1:
              output_grid[r,c] = 5
              break

    return output_grid
```