```python
"""
1.  **Find the Seed:** Locate the single azure (8) pixel within the input grid. This pixel remains unchanged in the output.
2.  **Top-Left Quadrant:** Fill the rectangular region defined by the top-left corner of the grid (0,0) and the row and column of the seed pixel with grey(5) pixels.
3. **Downward extension:** From the azure pixel, create a gray (5) pixel directly below it.
4.  **Bottom-Right Diagonal:** Extend gray (5) pixels diagonally down and to the right of the seed pixel. The extent and specific pattern are irregular and defined as follows:
    a. One gray pixel is placed to the right of the seed pixel.
    b. From there, the gray pixels are extended downwards by one every three rows.
    c. The gray pixels are extended to the right by one every three columns.
"""

import numpy as np

def find_seed(grid):
    # Find the coordinates of the azure (8) pixel.
    rows, cols = np.where(grid == 8)
    if len(rows) > 0:  # Check if an azure pixel was found
        return rows[0], cols[0]
    return None  # Or handle the case where no azure pixel is present

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the seed (azure pixel) location.
    seed_location = find_seed(input_grid)
    if seed_location is None:
        return output_grid # Return original if no seed is found

    row, col = seed_location

    # Top-Left Quadrant Fill
    for r in range(row):
        for c in range(col):
            output_grid[r, c] = 5

    # keep seed
    output_grid[row,col] = 8

    # Downward Extension
    if row + 1 < output_grid.shape[0]:
        output_grid[row + 1, col] = 5

    # Bottom-Right Diagonal
    if col + 1 < output_grid.shape[1]:
        output_grid[row, col + 1] = 5
        current_row = row + 1
        current_col = col + 1

        while current_row < output_grid.shape[0] and current_col < output_grid.shape[1]:
          
          next_row = min(current_row + 3, output_grid.shape[0])
          next_col = min(current_col + 3, output_grid.shape[1])

          # create a diagonal pixel
          if current_row < output_grid.shape[0]:
            output_grid[current_row, current_col] = 5
          # move markers every three
          current_row = next_row
          current_col = next_col



    return output_grid
```
