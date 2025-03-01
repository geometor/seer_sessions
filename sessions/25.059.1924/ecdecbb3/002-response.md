# ecdecbb3 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all red (2) pixels and azure (8) lines within the input grid.
2.  **For each red pixel:**
    *   Find the nearest azure line. The nearest line is determined by the shortest number of steps in cardinal directions that are required to reach a pixel that is part of the line
    *   Extend the red pixel towards that line. Do so by replacing the pixels along the shortest path to the azure line by red pixels.
3. **Preserve the existing:** Keep existing azure lines.
"""

import numpy as np

def find_objects(grid, color):
    """Finds coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def is_line(grid, coord, color):
    """Checks if a coordinate is part of a horizontal or vertical line of a given color."""
    row, col = coord
    # Check horizontal
    if col > 0 and grid[row, col - 1] == color:
        return True
    if col < grid.shape[1] - 1 and grid[row, col + 1] == color:
        return True
    # Check vertical
    if row > 0 and grid[row - 1, col] == color:
        return True
    if row < grid.shape[0] - 1 and grid[row + 1, col] == color:
        return True
    return False

def find_nearest_line(grid, start_coord, line_color):
    """Finds the nearest coordinate of a line of the specified color."""
    min_dist = float('inf')
    nearest_line_coord = None

    line_coords = find_objects(grid, line_color)
    for line_coord in line_coords:
      if is_line(grid, line_coord, line_color):
        row_dist = abs(start_coord[0] - line_coord[0])
        col_dist = abs(start_coord[1] - line_coord[1])
        dist = row_dist + col_dist  # Manhattan distance

        if dist < min_dist:
            min_dist = dist
            nearest_line_coord = line_coord
    return nearest_line_coord
    

def extend_pixel(grid, start_coord, end_coord, color):
    """Extends a pixel from start_coord to end_coord (inclusive) with the given color."""
    row1, col1 = start_coord
    row2, col2 = end_coord

    # Determine direction of extension
    row_step = 0 if row1 == row2 else (1 if row1 < row2 else -1)
    col_step = 0 if col1 == col2 else (1 if col1 < col2 else -1)
    
    # Extend vertically or horizontally only - not diagonally
    if row_step != 0 and col_step != 0: # should never happen
        return

    current_row, current_col = row1, col1
    while (current_row, current_col) != (row2 + row_step, col2+col_step):
      grid[current_row, current_col] = color
      current_row += row_step
      current_col += col_step

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find red pixels
    red_pixels = find_objects(input_grid, 2)

    # change output pixels by extending red pixels to nearest azure
    for red_pixel in red_pixels:
        nearest_azure_line_coord = find_nearest_line(input_grid, red_pixel, 8)
        if nearest_azure_line_coord is not None:
            extend_pixel(output_grid, red_pixel, nearest_azure_line_coord, 2)
    return output_grid
```
