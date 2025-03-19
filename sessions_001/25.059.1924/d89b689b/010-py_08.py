"""
Identifies single-pixel colored objects in the input grid, removes any multi-pixel blocks, and repositions the single-pixel objects into a 2x2 square in the center of the output grid. The 2x2 block has a specific color arrangement: top-left: grey, top-right: maroon, bottom-left: red, bottom-right: blue.
"""

import numpy as np

def find_single_pixels(grid):
    # Find coordinates of single pixels of specified colors
    single_pixels = []
    for color in [1, 2, 5, 9]:  # blue, red, grey, maroon
        pixels = np.argwhere(grid == color)
        for p in pixels:
          single_pixels.append((tuple(p),color))
    return single_pixels

def transform(input_grid):
    # Initialize output grid with white background
    output_grid = np.zeros_like(input_grid)

    # Find single pixels
    single_pixels = find_single_pixels(input_grid)
    
    # Target positions for the 2x2 block in the center
    center = (input_grid.shape[0] // 2, input_grid.shape[1] // 2)
    target_positions = {
        5: (center[0] - 1, center[1] - 1),  # grey: top-left
        9: (center[0] - 1, center[1]),      # maroon: top-right
        2: (center[0], center[1] - 1),      # red: bottom-left
        1: (center[0], center[1])           # blue: bottom-right
    }

    # Place single pixels in output grid at target positions
    for pixel,color in single_pixels:
            if color in target_positions:
                output_grid[target_positions[color]] = color
    

    return output_grid