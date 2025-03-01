# e179c5f4 • 018 • example_3 • investigate_coder

---
```python
"""
1.  **Locate the Seed:** Find the (x, y) coordinates of the single blue pixel ('1') within the input grid.
2.  **Initialize Output:** Create an output grid of the same dimensions as the input grid, filled entirely with azure ('8')
3.  **cross pattern:** fill a cross, or plus shape, around the located seed with blue pixels
    - the length of the cross is determined by the grid size
    - for a 10 x 4 grid, there are 5 cells above and below for the vertical line, and 2 to the left, and one to the right forming the cross bar.
4. leave the seed cell as an azure pixel.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a specific color pixel.
    for y, row in enumerate(grid):
        for x, pixel in enumerate(row):
            if pixel == color:
                return x, y
    return None

def transform(input_grid):
    # Initialize output_grid with azure (8).
    output_grid = np.full(np.shape(input_grid), 8)

    # Find the coordinates of the blue (1) pixel.
    seed_x, seed_y = find_pixel(input_grid, 1)

    # Create cross pattern.
    height, width = output_grid.shape
    for i in range(height):
        output_grid[i, seed_x] = 1  # Vertical line
    for j in range(width):
        output_grid[seed_y, j] = 1  # Horizontal line

    # change the original seed location back to 8
    output_grid[seed_y,seed_x] = 8
    return output_grid
```
