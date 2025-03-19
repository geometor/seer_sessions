"""
The input grid contains a cross-shaped object composed of red pixels. The transformation rotates this red cross 90 degrees clockwise.
The output grid shows the rotated cross. Green pixels in the four corners of the grid remain unchanged.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    return coords

def rotate_point(point, center):
    # Rotate a point 90 degrees clockwise around a center.
    y, x = point
    center_y, center_x = center
    new_y = center_y + (x - center_x)
    new_x = center_x - (y - center_y)
    return (new_y, new_x)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the red cross object.
    red_pixels = find_object(input_grid, 2)
    if len(red_pixels) == 0: # no red pixels
        return output_grid

    # Calculate the center of the red cross.
    center_y = np.mean(red_pixels[:, 0]).astype(int)
    center_x = np.mean(red_pixels[:, 1]).astype(int)
    center = (center_y, center_x)

    # Clear existing red pixels from output grid
    for y, x in red_pixels:
      output_grid[y,x] = 0
      
    # Rotate each red pixel and update the output grid.
    for point in red_pixels:
        new_point = rotate_point(point, center)
        # Check bounds - important because rotation can go out of bounds of original array
        if 0 <= new_point[0] < output_grid.shape[0] and 0 <= new_point[1] < output_grid.shape[1]:
          output_grid[new_point] = 2

    return output_grid