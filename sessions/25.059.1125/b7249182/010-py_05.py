"""
1.  **Identify Key Pixels:** Locate the green (3) and blue (1) pixels in the input grid.

2.  **Horizontal Expansion:**
    *   From the green pixel's original location, create a horizontal sequence of green pixels extending to the left and right, until the middle of the distances between the blue and green pixel
    *   From the blue pixel's initial location, create a sequence of blue pixels extending horizontally to the right and to the left until the middle of the distance between the green and blue pixels.

3.  **Connect the sequences:**
    *   Create a new row in the output grid by combining the expanded green and blue sequences. The sequences starts at the left boundary and are connected at their mid point.

4.  **Vertical Replication**:
    *   Replicate the created sequence of green and blue pixels vertically, both up and down by two rows. The pixel at the horizontal position of the original green pixel will have a color of green. The pixel at the horizontal position of the original blue pixel will have the color of blue.

5.  **Fill Remaining:** All other cells in the output grid remain white (0).
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
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find the green and blue pixels
    green_coords = find_pixel(input_grid, 3)
    blue_coords = find_pixel(input_grid, 1)

    if green_coords is None or blue_coords is None:
        return output_grid # Return empty grid if either color is not found

    # Horizontal Expansion and connection
    row_index = green_coords[0]
    mid_point = (green_coords[1] + blue_coords[1]) // 2
    
    # expand green to the left
    for c in range(green_coords[1], -1, -1):
        output_grid[row_index, c] = 3

    # expand green to the mid point
    for c in range(green_coords[1] + 1, mid_point):
        output_grid[row_index, c] = 3

    # expand blue to the right
    for c in range(blue_coords[1], len(output_grid[0])):
          output_grid[row_index, c] = 1
    # expand blue to the left up to the midpoint
    for c in range(blue_coords[1]-1, mid_point-1, -1):
      output_grid[row_index, c] = 1
    
    # vertical replication of the sequence
    for i in range(-2, 3):
        if row_index + i >= 0 and row_index + i < len(output_grid):
           output_grid[row_index + i, :] = output_grid[row_index,:]
           output_grid[row_index + i, green_coords[1]] = 3
           output_grid[row_index + i, blue_coords[1]] = 1

    return output_grid