"""
1.  **Outline:** Create a 10x10 grid.
2.  **Border:** Fill the outermost border (top, bottom, left, and right edges) of the grid with green pixels (value 3).
3. **Central Cross:** in the central 6 x 6 grid (i.e., skip the first and last row and first and last column), make a cross with arm length 3 (including the center pixel, which will already be set to 3 from previous step):
    *   Fill the central vertical line and center horizontal line within the 6 x 6 grid with green(3) pixels except for the pixels at locations (3,1),(3,8) and (8,3),(8,8) where (0,0) is top left.
4.  **Background:** All other pixels remain white (value 0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Fill the border with 3s (green)
    output_grid[0, :] = 3  # Top row
    output_grid[rows - 1, :] = 3  # Bottom row
    output_grid[:, 0] = 3  # Left column
    output_grid[:, cols - 1] = 3  # Right column

    # Create the central cross within the 6x6 subgrid
    for i in range(2, 8):
        output_grid[i, 2] = 3
        output_grid[i, 7] = 3
        output_grid[2, i] = 3
        output_grid[7, i] = 3

    return output_grid