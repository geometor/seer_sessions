"""
Transforms an input grid by horizontally expanding non-zero pixels to the left and right, inserting a gray pixel (5) in between.
"""

import numpy as np

def find_non_zero_pixels(grid):
    # Find coordinates of non-zero pixels
    non_zero_coords = np.argwhere(grid != 0)
    # Sort by column index (x-coordinate)
    non_zero_coords = non_zero_coords[non_zero_coords[:, 1].argsort()]
    return non_zero_coords


def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find and sort non-zero pixels
    non_zero_pixels = find_non_zero_pixels(input_grid)

    if len(non_zero_pixels) != 2:
        return output_grid # Handles cases not matching prompt.  Could raise Exception instead.

    left_pixel = non_zero_pixels[0]
    right_pixel = non_zero_pixels[1]
    
    left_color = input_grid[left_pixel[0], left_pixel[1]]
    right_color = input_grid[right_pixel[0], right_pixel[1]]

    row = left_pixel[0]  # Row for expansion is same.
    
    #Expansion length
    expansion_length = 5
    
    #Calculate center
    center = expansion_length
    
    
    # Left expansion
    for i in range(expansion_length):
        output_grid[row, i] = left_color

    #Insert Grey
    output_grid[row,center] = 5

    # Right expansion
    for i in range(center + 1, center + 1 + expansion_length):
        output_grid[row, i] = right_color


    return output_grid