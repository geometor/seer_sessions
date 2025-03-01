# a3df8b1e • 012 • refine_coder

---
```python
"""
1.  **Identify Starting Point:** Find the blue pixel in the input grid. The output diagonal line starts at this location.
2.  **Generate Diagonal:** From the starting point, create a diagonal line of blue pixels.  The line extends upwards and to the right.  For each step, move one row up and one column to the right.
3. **Preserve Other Colors:** Copy all non-blue pixels from the input grid to the exact same positions in the output grid.
4. **Termination:** Continue the diagonal pattern until the edges of the grid prevent moving further up or right.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same values as the input grid
    output_grid = input_grid.copy()

    # Find the location of the blue pixel (value 1) in the input grid.
    blue_pixel_location = np.where(input_grid == 1)

    # if no blue, return the input as is
    if len(blue_pixel_location[0]) == 0:
        return output_grid

    # Get the starting row and column
    start_row, start_col = blue_pixel_location[0][0], blue_pixel_location[1][0]

    # Generate the diagonal
    row, col = start_row, start_col
    while row >= 0 and col < output_grid.shape[1]:
        output_grid[row, col] = 1
        row -= 1
        col += 1

    return output_grid
```

