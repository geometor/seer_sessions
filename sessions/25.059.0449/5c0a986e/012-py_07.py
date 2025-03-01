"""
1.  **Identify Red and Blue Objects:** Find all contiguous regions (objects) of red (2) and blue (1) pixels in the input grid.
2.  **Locate Extrema:** For the red object, find the bottom-rightmost pixel. For the blue object, find the top-leftmost pixel.
3.  **Create Diagonal:** Draw a diagonal line of pixels connecting the bottom-right of the red object to the top-left of the blue object.
4.  **Alternate Colors:** Starting from the pixel immediately below and to the right from the bottom-right pixel of the red object, color the diagonal path, alternating between blue (1) and black (0). The pixel after red starts with blue.
5. **Preserve:** The original red and blue objects remain.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of a specific color."""
    objects = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []

        visited.add((row, col))
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                objects.append(dfs(r, c))
    return objects

def find_extrema(object_pixels):
    """Finds the top-left and bottom-right pixels of an object."""
    if not object_pixels:
        return None, None

    min_row = min(pixel[0] for pixel in object_pixels)
    max_row = max(pixel[0] for pixel in object_pixels)
    min_col = min(pixel[1] for pixel in object_pixels)
    max_col = max(pixel[1] for pixel in object_pixels)

    # Find top-left (min_row, min_col) and bottom-right (max_row, max_col).
    #  Note: there might be multiple pixels with same row/col, so get exact pixel
    top_left = (min_row, min_col)
    bottom_right = (max_row, max_col)

    for r, c in object_pixels:
      if r == min_row and c < top_left[1]:
        top_left = (r,c)
      if r == max_row and c > bottom_right[1]:
        bottom_right = (r, c)

    return top_left, bottom_right

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find red and blue objects
    red_objects = find_objects(grid, 2)
    blue_objects = find_objects(grid, 1)
    
    # Handle cases with no red or blue objects
    if not red_objects or not blue_objects:
        return output_grid
    
    # Use the first red and blue object found (in case there are multiple)
    red_object = red_objects[0]
    blue_object = blue_objects[0]

    # Locate extrema
    _, red_bottom_right = find_extrema(red_object)  # We only need bottom-right
    blue_top_left, _ = find_extrema(blue_object)    # We only need top-left

    # Create diagonal path
    r_row, r_col = red_bottom_right
    b_row, b_col = blue_top_left

    # Adjust starting point for alternating colors
    current_row = r_row + 1
    current_col = r_col + 1
    
    # Determine direction
    row_step = 1 if b_row >= current_row else -1
    col_step = 1 if b_col >= current_col else -1

    # Alternate colors along the diagonal
    color_toggle = 1  # Start with blue

    while (row_step > 0 and current_row <= b_row) or (row_step < 0 and current_row >= b_row):
      if (col_step > 0 and current_col <= b_col) or (col_step < 0 and current_col >= b_col):

        if 0 <= current_row < output_grid.shape[0] and 0 <= current_col < output_grid.shape[1]:
            output_grid[current_row, current_col] = color_toggle
        color_toggle = 1 if color_toggle == 0 else 0  # Alternate between blue and black

        current_col += col_step
      current_row += row_step
    return output_grid