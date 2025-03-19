# a2fd1cf0 • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Key Pixels:** Locate the red (2) and green (3) pixels within the input grid. Note their positions.
2.  **Determine Azure Line Column:** The azure (8) line will be in the same column as the green pixel.
3.  **Determine Azure line start and end:** The line end row is the row before the row containing the green pixel. The line start row is the row that contains the red pixel.
4.  **Draw Azure Line:** Create a vertical line of azure (8) pixels.
5. **Preserve Key Pixels:** Keep red and green pixels at initial positions.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return row, col
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the red and green pixels
    red_pixel_pos = find_pixel(input_grid, 2)
    green_pixel_pos = find_pixel(input_grid, 3)

    if red_pixel_pos is None or green_pixel_pos is None:
        return output_grid # if not found - return the grid

    # Determine the column and rows for the azure line
    column = green_pixel_pos[1]
    start_row = red_pixel_pos[0]
    end_row = green_pixel_pos[0] -1

    # Draw the azure line
    for row in range(start_row, end_row + 1):
        output_grid[row, column] = 8

    return output_grid
```
