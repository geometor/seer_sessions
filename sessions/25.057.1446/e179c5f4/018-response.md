# e179c5f4 • 018 • refine_coder

---
```python
"""
1.  **Background Replacement:** Replace all white (0) pixels in the input grid with azure (8) pixels. The input and output grids have the same dimensions.
2.  **Identify Blue Pixels:** Find the locations of *all* blue (1) pixels in the input grid.
3.  **Create Crosses:** For *each* blue pixel found in the input:
    *   Create a 3x3 cross shape centered at the blue pixel's location. The cross is made of blue (1) pixels. The cross is formed by the center pixel, and pixels above, below, left, and right of the center.
4.  **Render Output:** Output the modified grid, which now includes the azure background and all generated blue crosses.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input grid
    output_grid = np.copy(input_grid)

    # change all 0 (white) to 8 (azure)
    output_grid[output_grid == 0] = 8

    # Find the locations of all blue (1) pixels in the input grid.
    blue_pixels = np.where(input_grid == 1)
    blue_pixel_locations = list(zip(blue_pixels[0], blue_pixels[1]))

    # Create cross for each blue pixel
    for row, col in blue_pixel_locations:
        # define cross shape, size 3x3
        output_grid[row, col] = 1  # Center
        if row > 0:
            output_grid[row - 1, col] = 1  # Up
        if row < output_grid.shape[0] - 1:
            output_grid[row + 1, col] = 1  # Down
        if col > 0:
            output_grid[row, col - 1] = 1  # Left
        if col < output_grid.shape[1] - 1:
            output_grid[row, col + 1] = 1  # Right

    return output_grid
```

