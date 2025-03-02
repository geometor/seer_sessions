# dae9d2b5 • 031 • refine_coder

---
```python
"""
The output grid is always 3x3. The transformation rule is as follows:

1. **Blue/Red Rule**: If Blue and Red are present: Output is Magenta at (0,1)
2. **Green/Yellow Rule**: If Green and Yellow are present:
    * Green is directly above Yellow, output is Magenta at (2,0)
    * Green is to the left of Yellow: output is Magenta at (1,0).
    * Green and Yellow are diagonal (Green is NW): output is magenta at (0,0), (2,2)
    * In cases of conflict, prioritize Green/Yellow positioning
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the positions of pixels of a specific color."""
    rows, cols = grid.shape
    positions = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                positions.append((r, c))
    return positions

def transform(input_grid):
    # Initialize output_grid as 3x3 with all white (0) pixels.
    output_grid = np.zeros((3, 3), dtype=int)

    # Find Blue (1) and Red (2) pixels.
    blue_pixels = find_pixels(input_grid, 1)
    red_pixels = find_pixels(input_grid, 2)

    # Find Green (3) and Yellow (4) pixels.
    green_pixels = find_pixels(input_grid, 3)
    yellow_pixels = find_pixels(input_grid, 4)

    # Blue/Red Rule
    if blue_pixels and red_pixels:
        output_grid[0, 1] = 6

    # Green/Yellow Rule
    if green_pixels and yellow_pixels:
        green_row, green_col = green_pixels[0]
        yellow_row, yellow_col = yellow_pixels[0]

        if green_row < yellow_row and green_col == yellow_col:
              output_grid[2,0] = 6
        elif green_col < yellow_col:
            output_grid[1, 0] = 6
        elif green_row < yellow_row and green_col < yellow_col: #green is NW, yellow is SE
            output_grid[0,0] = 6
            output_grid[2,2] = 6


    return output_grid
```
