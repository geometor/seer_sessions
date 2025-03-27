```python
"""
1.  **Preserve Color 2:** If a pixel is color 2 (red) in the input grid, keep it as color 2 in the output grid *unless* it is not in the bottom row and is adjacent to color 8 that gets changed to 5.
2. **Change to Gray**: Change all instances of color 1 (blue) to color 5.
3. **Change to Gray**: Change all instances of color 3 (green) to color 5.
4.  **Change to Gray:** Change all instances of color 8 (azure) to color 5 (grey).
5. **Preserve Color 4:** Do not change color 4.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Change 1, 3, and 8 to 5
            if input_grid[r, c] in [1, 3, 8]:
                output_grid[r, c] = 5
            # Preserve color 2 unless it's adjacent to an 8 *and* not in the bottom row
            elif input_grid[r,c] == 2:
                if r < rows - 1: # Not in the last row
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr,nc] == 8:
                            output_grid[r,c] = 5
                            break

    return output_grid
```