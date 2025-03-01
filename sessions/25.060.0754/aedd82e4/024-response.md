# aedd82e4 • 024 • refine_coder

---
```python
"""
1.  **Red Pixel Preservation:** All red pixels in the input grid remain red in the output grid, *except* if a red pixel is at the exact center of the grid.
2.  **Center Pixel Transformation (Conditional):** If the center pixel of the input grid is red, it is changed to blue in the output grid.
3.  **White to Blue Conversion adjacent to Red:** Any white pixel that is *anywhere* and *adjacent* (horizontally, vertically, or diagonally) to a red pixel in the *input* grid is changed to blue in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    # Find all red pixel coordinates in the input grid
    red_pixels = np.argwhere(input_grid == 2)

    # Center Pixel Transformation
    if input_grid[center_row, center_col] == 2:
        output_grid[center_row, center_col] = 1

    # Iterate through all red pixels
    for red_row, red_col in red_pixels:
        # Iterate through adjacent cells (including diagonals)
        for i in range(max(0, red_row - 1), min(rows, red_row + 2)):
            for j in range(max(0, red_col - 1), min(cols, red_col + 2)):
                # Check if the adjacent cell is white
                if input_grid[i, j] == 0:
                    output_grid[i, j] = 1  # Change to blue

    return output_grid
```

