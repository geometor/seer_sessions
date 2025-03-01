"""
The transformation extracts a single instance of a repeating object from the input grid, places it in a new grid, and fills the border with the frame background color.
"""

import numpy as np

def find_repeating_object(grid):
    # find repeating object size and shape
    rows, cols = len(grid), len(grid[0])
    
    # Iterate through potential object sizes (limiting to half of grid dimensions)
    for obj_height in range(1, rows // 2 + 1):
        for obj_width in range(1, cols // 2 + 1):
            # Check if grid dimensions are divisible by the potential object size
            if rows % obj_height == 0 and cols % obj_width == 0:
                # Extract the top-left corner as the potential object
                potential_object = [row[:obj_width] for row in grid[:obj_height]]
                
                # Check if this pattern repeats throughout the grid
                is_repeating = True
                for i in range(0, rows, obj_height):
                    for j in range(0, cols, obj_width):
                        # Extract region to compare with the potential object
                        region = [row[j:j + obj_width] for row in grid[i:i + obj_height]]
                        if region != potential_object:
                            is_repeating = False
                            break
                    if not is_repeating:
                        break
                
                if is_repeating:
                    return potential_object, obj_height, obj_width
    return None, 0, 0

def get_frame_color(input_grid, object_height, object_width):
  # get the color of pixel in top left corner of grid
    return input_grid[0][0]


def transform(input_grid):
    # Find the repeating object and its dimensions
    object_grid, obj_height, obj_width = find_repeating_object(input_grid)

    # find frame color
    frame_color = get_frame_color(input_grid, obj_height, obj_width)

    # Initialize output grid
    output_grid = np.full((obj_height + 2, obj_width + 2), frame_color, dtype=int)

    # fill the inner grid with the object
    for i in range(obj_height):
        for j in range(obj_width):
          output_grid[i+1][j+1] = object_grid[i][j]

    return output_grid