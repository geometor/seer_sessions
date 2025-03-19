"""
The input grid contains single-pixel objects. Each object is mirrored horizontally, creating a copy on the opposite side of the grid at an equal distance from a perceived vertical center. The vertical position is maintained. Output grid expands to fit mirrored pixels, doubling when possible, and by a factor of `n + (n - 1)` otherwise.
"""

import numpy as np

def get_object_coordinates(grid):
    # Find the coordinates of the non-zero pixel (the object)
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                return r, c
    return None  # Should not happen in this specific task, but good practice

def transform(input_grid):
    # Find object coordinates.
    object_row, object_col = get_object_coordinates(input_grid)
    object_color = input_grid[object_row][object_col]

    # Determine output dimensions.
    input_height = len(input_grid)
    input_width = len(input_grid[0])

    output_height = input_height + (input_height - 1) if object_row > 0 and input_height > 2 else input_height * 2
    output_width = input_width + (input_width - 1) if object_col > 0 and input_width > 2 else input_width * 2

    # Initialize output grid with zeros.
    output_grid = [[0] * output_width for _ in range(output_height)]

    # Place original object in the output grid
    original_row_output = object_row
    if output_height > input_height and object_row > 0:
        if object_row < input_height // 2:
           original_row_output = object_row
        else: # object_row >= input_height/2
            original_row_output = object_row + (input_height-1) - (input_height - 1 - object_row) - (input_height // 2 if input_height %2 != 0 else input_height // 2 -1) + (1 if input_height % 2 != 0 else 0 )


    output_grid[original_row_output][object_col] = object_color
    
    # Calculate mirrored position.
    # find perceived center
    center = (input_width - 1) / 2
    
    mirrored_col = int(2 * center - object_col)

    # Place mirrored object
    mirrored_row_output = object_row
    if output_height > input_height and object_row > 0:

        if object_row < input_height // 2:
            mirrored_row_output = object_row + input_height -1
        else:
            mirrored_row_output = (object_row + input_height-1) - (input_height * 2 - 1)  # keep relative location
            mirrored_row_output = object_row + (input_height-1) - (input_height - 1 - object_row) - (input_height // 2 if input_height %2 != 0 else input_height // 2 -1)  + (1 if input_height % 2 != 0 else 0 )
            mirrored_row_output += input_height-1


    if mirrored_col >= output_width:
        # this should never happen with the current logic
        mirrored_col = output_width - 1

    output_grid[mirrored_row_output][mirrored_col] = object_color

    return output_grid