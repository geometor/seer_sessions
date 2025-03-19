# ff28f65a • 030 • refine_coder

---
```python
"""
1. **Identify a 2x2 block of red (value '2') pixels.** If such a block exists, continue; otherwise, output = input.
2. **Locate the Top-Left Corner:** Determine the row and column indices (i, j) of the top-left pixel of the 2x2 red block.
3. **Replace with Blue:** Create a single blue (value '1') pixel at the location of the top-left corner of the red block (i, j) in the output grid.
4. **Clear Remaining Red:** Set all red pixels in the original input to white (value '0') in the output grid.
5. **Result:** Return the modified grid.
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
        # Replace the top-left corner of the red block with a blue pixel
        i, j = red_block_coords
        output_grid = np.zeros_like(input_grid) # start with a blank (all-white) grid
        output_grid[i, j] = 1

    return output_grid
```
