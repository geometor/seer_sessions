# b7249182 • 012 • refine_coder

---
```python
"""
1.  **Locate Key Pixels:** Find the coordinates of the single green (3) pixel and the single blue (1) pixel within the input grid.

2.  **Horizontal Fill:**
    *   Create a horizontal sequence of pixels in a single row of the output grid.
    *   Starting from the green pixel's column and extending left to the edge of the grid, fill with green (3).
    *   Starting from the blue pixel's column and extending right to the edge of the grid, fill with blue (1).
    *   Fill the space between the green and the blue with green to the left of the mid point and blue to the right.

3.  **Vertical Fill:**
    *   Fill all rows of the output grid with the horizontal sequence generated.

4. **Preserve:**
   * The output grid will have the same dimensions as the input grid.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                return (r_idx, c_idx)
    return None

def transform(input_grid):
    # Initialize output_grid with the same dimensions as input_grid, filled with white (0)
    output_grid = np.zeros_like(input_grid)
    
    # Find the green and blue pixels
    green_coords = find_pixel(input_grid, 3)
    blue_coords = find_pixel(input_grid, 1)

    if green_coords is None or blue_coords is None:
        return output_grid # Return empty grid if either color is not found

    # Create the horizontal sequence
    row_index = green_coords[0]  # Use the row of the green pixel
    mid_point = (green_coords[1] + blue_coords[1]) // 2

    # Fill with green from green_coords to the left edge
    for c in range(green_coords[1], -1, -1):
        output_grid[row_index, c] = 3

    # Fill with blue from blue_coords to the right edge
    for c in range(blue_coords[1], output_grid.shape[1]):
        output_grid[row_index, c] = 1

    # Fill the space between green and blue
    for c in range(green_coords[1] + 1, blue_coords[1]):
        if c <= mid_point:
            output_grid[row_index,c] = 3
        else:
            output_grid[row_index,c] = 1

    # Vertical Fill: Copy the generated row to all other rows
    for r in range(output_grid.shape[0]):
        output_grid[r, :] = output_grid[row_index, :]

    return output_grid
```
