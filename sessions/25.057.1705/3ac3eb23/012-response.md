# 3ac3eb23 • 012 • refine_coder

---
```python
"""
1.  **Identify the single yellow pixel:** Locate the single yellow (4) pixel within the input grid.
2.  **Count Rows Below:** Determine the number of rows existing *below* the row containing the yellow pixel.
3. **Transformation Rule:**
   *   **IF** the yellow pixel exists, *and* there is one or more rows below it, **THEN**:
        * Starting from the row immediately below the yellow pixel, and in every other row following, change the color of the pixel in that column to yellow (4). Continue this pattern to the last row of the grid.
        * For example, if the yellow pixel is on Row 2, then update rows 3, 5, etc.
   * **IF** there are zero rows below or no yellow pixel is found:
      * the output grid is an exact copy of the input grid.
4. **All other pixels:** Maintain the original colors of all other pixels in the grid.
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

        # Count rows below
        rows_below = len(input_grid) - start_row - 1

        # Conditional Transformation
        if rows_below > 0:
            # Alternate colors vertically.
            for row in range(start_row + 1, len(output_grid)):
                if (row - start_row) % 2 != 0:  #every other cell from start
                    output_grid[row, col] = 4

    return output_grid
```
