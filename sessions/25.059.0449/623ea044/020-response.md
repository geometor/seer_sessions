# 623ea044 • 020 • refine_coder

---
```python
"""
1.  **Find the Seed:** Locate the single azure (8) pixel within the input grid. This pixel is the "seed" for the transformation.
2.  **Initialize Output:** Create an output grid filled with black (0) pixels, with same dimensions of input.
3.  **Diagonal Expansion:** Starting from the seed pixel, extend azure (8) pixels diagonally in all four directions (up-left, up-right, down-left, and down-right).
4.  **Edge Termination:** Continue the diagonal expansion in each direction until the edge of the output grid is reached.
5. **Output:** The output grid is all black pixels, except for the diagonally expanded lines.
"""

import numpy as np

def find_seed_pixel(grid):
    # Find the coordinates of the azure (8) pixel.
    rows, cols = np.where(grid == 8)
    if len(rows) > 0:  # Check if an 8 was found
       return rows[0], cols[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a zero-filled grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)

    # Find the seed pixel.
    seed_coords = find_seed_pixel(input_grid)
    if seed_coords is None:
        return output_grid # return if no seed pixel

    seed_row, seed_col = seed_coords

    # set seed pixel
    output_grid[seed_row, seed_col] = 8

    # Get grid dimensions.
    height, width = input_grid.shape

    # Expand diagonally.
    for i in range(1, max(height, width)):
        # Up-left
        if seed_row - i >= 0 and seed_col - i >= 0:
            output_grid[seed_row - i, seed_col - i] = 8
        # Up-right
        if seed_row - i >= 0 and seed_col + i < width:
            output_grid[seed_row - i, seed_col + i] = 8
        # Down-left
        if seed_row + i < height and seed_col - i >= 0:
            output_grid[seed_row + i, seed_col - i] = 8
        # Down-right
        if seed_row + i < height and seed_col + i < width:
            output_grid[seed_row + i, seed_col + i] = 8

    return output_grid
```
