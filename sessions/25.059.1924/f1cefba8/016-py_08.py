"""
1.  **Identify Objects:** Locate the outer red (2) rectangular region and the inner green (3) rectangular region.
2.  **Modify Green Region:**  The central green pixels along the y-axis (vertical) maintains its vertical position, except for the top and bottom pixels, which are changed to red. All the other green pixels are modified based on its surrounding pixel. If the left pixel is red, it becomes red. Otherwise if it is green, it becomes green.
3.  **Add black pixels:** add a green pixel at the top, and bottom of the center of the grid.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Handle case where color is not found
    
    # Calculate bounding box.
    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)
    return (min_y, min_x), (max_y, max_x)


def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the red and green regions.
    red_top_left, red_bottom_right = find_object(input_grid, 2)
    green_top_left, green_bottom_right = find_object(input_grid, 3)

    if red_top_left is None or green_top_left is None:
            return output_grid

    # Modify Green Region
    for y in range(green_top_left[0], green_bottom_right[0] + 1):
      for x in range(green_top_left[1], green_bottom_right[1] + 1):
        if input_grid[y,x] == 3:
            if x == (green_top_left[1] + green_bottom_right[1]) // 2 :
                if y != green_top_left[0] and y != green_bottom_right[0]:
                  output_grid[y,x] = 3
                else:
                    output_grid[y,x] = 2

            elif input_grid[y, x-1] == 2:
                output_grid[y, x] = 2


    # Add black pixels.
    center_x = input_grid.shape[1] // 2
    output_grid[0, center_x] = 3
    output_grid[-1, center_x] = 3
    
    return output_grid