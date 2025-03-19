# ff28f65a • 028 • example_5 • investigate_coder

---
```python
"""
1.  **Identify a 2x2 block of red (value '2') pixels.** If such block exists, continue, otherwise output = input
2.  **Replace this block:** Create one blue (value '1') pixel located at row 0, column 0.
3. **Clear Remaining Red:** Set all remaining red to white (value '0').
4. **Result:** Return the modified grid.
"""

import numpy as np

def find_2x2_red_block(grid):
    # Iterate through the grid to find a 2x2 block of red pixels
    rows, cols = grid.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 2 and grid[i + 1, j] == 2 and
                grid[i, j + 1] == 2 and grid[i + 1, j + 1] == 2):
                return (i, j)  # Return top-left coordinates of the block
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the 2x2 red block
    red_block_coords = find_2x2_red_block(output_grid)

    if red_block_coords:
       # if found replace with blue pixel at [0,0]
       output_grid = np.zeros_like(input_grid)  # start with all white background
       output_grid[0, 0] = 1

    return output_grid
```
