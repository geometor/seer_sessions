# 3ac3eb23 • 010 • refine_coder

---
```python
"""
1.  **Identify the initial yellow pixel:** Find the single yellow (4) pixel in the input grid.
2.  **Conditional Transformation:**
    *   **IF** the yellow pixel is in the top row, **AND** if there is at least 3 rows below, **THEN**:
        *   Starting from the row immediately below the initial yellow pixel, and for every alternate row afterwards, change the color of the pixel in that column to yellow (4). Continue to the bottom row of the grid.
3.  **Otherwise:** The output grid is identical to the input grid (no transformation).
4. **All other pixels:** All other pixels remain the same color.
"""

import numpy as np

def find_yellow_pixel(grid):
    # Find the coordinates of the yellow pixel (value 4).
    for r in range(len(grid)):
        for c in range(len(grid[0])):
          if grid[r][c] == 4:
            return (r,c)
    return None

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    
    # Find initial yellow pixel.
    yellow_pixel_coords = find_yellow_pixel(input_grid)
    if yellow_pixel_coords is not None:
        start_row, col = yellow_pixel_coords

        # Conditional Transformation
        if start_row == 0 and len(input_grid) >= 4:  # Top row and at least 3 rows below
            # Alternate colors vertically.
            for row in range(start_row + 1, len(output_grid)):
                if (row - start_row) % 2 != 0:  #every other cell from start
                    output_grid[row, col] = 4
        else:
            # No transformation, output is the same as input
            return output_grid

    return output_grid
```

