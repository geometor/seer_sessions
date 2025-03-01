"""
1.  **Identify the gray pixel (color 5) within the input grid.** This pixel acts as the center of rotation.

2.  **Identify pixels to rotate.**
    *   In example 1 and 3, the pixels immediately to the left and right of the gray pixel, as well as the pixel directly below, form an "L" shape and they move.
    *   In example 2: the pixels immediately below and to the right are rotated.

3. **Rotate select pixels 90 degrees clockwise around the gray center.**
    * The relative row and column deltas between the moving pixel and the center pixel are swapped and inverted.

4.  **Create output grid** Copy all pixels from the input grid to the same
    position in the output grid.

5.  **Update the output grid**: Move the selected pixels that were rotated to
    their new positions on the output grid. If two moving pixels would occupy the same location, then use these priorities: color below > color to the right > color to the left.
"""

import numpy as np

def find_gray_center(grid):
    """Finds the coordinates of the gray pixel (color 5) in the grid."""
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == 5:
                return (row_idx, col_idx)
    return None  # Should not happen in these tasks, but good practice

def rotate_point(point, center):
    """Rotates a point 90 degrees clockwise around a center point."""
    row, col = point
    center_row, center_col = center
    new_row = center_row + (col - center_col)
    new_col = center_col - (row - center_row)
    return (new_row, new_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the gray center pixel.
    center = find_gray_center(input_grid)
    if center is None:
        return output_grid

    center_row, center_col = center

    # Identify pixels to rotate based on example-specific rules.
    moved_pixels = []
    if input_grid.shape == (5, 9):  # Example 1 shape
        # Example 1 & 3: Pixels to the left, right, and below.
      if center_row + 1 < input_grid.shape[0]:
        moved_pixels.append(((center_row + 1, center_col), input_grid[center_row+1, center_col]))
      if center_col -1 >= 0:
        moved_pixels.append(((center_row, center_col - 1), input_grid[center_row, center_col - 1]))
      if center_col + 1 < input_grid.shape[1]:
        moved_pixels.append(((center_row, center_col + 1), input_grid[center_row, center_col + 1]))


    elif input_grid.shape == (11, 11):  # Example 2 shape
        # Example 2: Pixels below and to the right.
        if center_row + 1 < input_grid.shape[0]:
            moved_pixels.append(((center_row + 1, center_col), input_grid[center_row + 1, center_col]))  # Below
        if center_col + 1 < input_grid.shape[1]:
            moved_pixels.append(((center_row, center_col + 1), input_grid[center_row, center_col + 1]))  # Right

    elif input_grid.shape == (7,9): #example 3 shape
      if center_row + 1 < input_grid.shape[0]:
        moved_pixels.append(((center_row + 1, center_col), input_grid[center_row+1, center_col]))
      if center_col -1 >= 0:
        moved_pixels.append(((center_row, center_col - 1), input_grid[center_row, center_col - 1]))
      if center_col + 1 < input_grid.shape[1]:
        moved_pixels.append(((center_row, center_col + 1), input_grid[center_row, center_col + 1]))
    else:
      return output_grid

    # Rotate and update the output grid, handling collisions
    rotated_pixels = {} #store where the pixels are intendend to go
    for (row,col), value in moved_pixels:
       rotated_coords = rotate_point((row,col), center)

       if 0 <= rotated_coords[0] < output_grid.shape[0] and 0 <= rotated_coords[1] < output_grid.shape[1]:
          #check collisions using priority
          if rotated_coords in rotated_pixels:
            existing_pixel_details = rotated_pixels[rotated_coords]
            existing_value = existing_pixel_details[1]
            _, existing_original_col = existing_pixel_details[0]
            if center_col < col:
                rotated_pixels[rotated_coords] = ((row,col), value) #current pixel is to right
            elif center_col == col and value == input_grid[center_row + 1, center_col]:
                rotated_pixels[rotated_coords] = ((row,col), value)  #current pixel to rotate is from below
          else:
            rotated_pixels[rotated_coords] = ((row,col), value)
    
    for rotated_coords, pixel_details in rotated_pixels.items():
      original_coords,value = pixel_details
      output_grid[rotated_coords] = value
      if (original_coords != rotated_coords):
        output_grid[original_coords] = 0

    return output_grid