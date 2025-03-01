"""
1.  **Identify the Red Region:** Find the bounding box of the largest contiguous red (2) region. This defines the outer boundary.
2. **Center the Object**: Remove any rows or columns on the edges of the red object that consist only of red pixels.
3.  **Identify/Create Black Region:**
    *   If a green (3) region exists within the red region, replace the green pixels with black (0) pixels, maintaining the original shape and position of the green region.
    *   If no green region exists, create a black region within the red region. The black region should occupy the center of the red region. The new black object height should be determined by `red_object_height - 4`, and width should be `red_object_width - 4`.
4.  **Output:** Return the modified grid.
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

def center_object(grid, color):
    # Find the object
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return grid  # Handle case where color is not found
    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)

    # Remove empty rows and columns from top, bottom, left, and right
    while np.all(grid[min_y, min_x:max_x+1] == color):
        min_y += 1
    while np.all(grid[max_y, min_x:max_x+1] == color):
        max_y -= 1
    while np.all(grid[min_y:max_y+1, min_x] == color):
        min_x += 1
    while np.all(grid[min_y:max_y+1, max_x] == color):
        max_x -= 1

    # Create new grid
    new_height = max_y - min_y + 1
    new_width = max_x - min_x + 1
    new_grid = np.full((new_height, new_width), color, dtype=int)

    # Copy the object into the new grid
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
          if (y>= 0 and y < grid.shape[0] and x>=0 and x < grid.shape[1]):
            new_grid[y-min_y, x-min_x] = grid[y, x]
    return new_grid



def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the red region.
    red_top_left, red_bottom_right = find_object(input_grid, 2)

    if red_top_left is None:
      return output_grid
    
    output_grid = center_object(output_grid, 2)

    red_top_left, red_bottom_right = find_object(output_grid, 2)
    # Find the green region.
    green_top_left, green_bottom_right = find_object(output_grid, 3)


    # Identify/Create Black Region
    if green_top_left is not None:
        # Replace green with black.
        for y in range(green_top_left[0], green_bottom_right[0] + 1):
            for x in range(green_top_left[1], green_bottom_right[1] + 1):
                output_grid[y, x] = 0
    else:
        # Create black region in the center.
        red_height = red_bottom_right[0] - red_top_left[0] + 1
        red_width = red_bottom_right[1] - red_top_left[1] + 1

        black_height = max(0, red_height - 4)  # Ensure non-negative
        black_width = max(0, red_width - 4) # Ensure non-negative


        black_top = red_top_left[0] + (red_height - black_height) // 2
        black_left = red_top_left[1] + (red_width - black_width) // 2
        black_bottom = black_top + black_height
        black_right = black_left + black_width
        for y in range(max(0,black_top), min(output_grid.shape[0],black_bottom)):
            for x in range(max(0,black_left), min(output_grid.shape[1], black_right)):
                output_grid[y, x] = 0

    return output_grid