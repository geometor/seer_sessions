"""
The transformation rule involves identifying a single blue square in the input grid. This square is then copied to the output grid. The position of the output square is determined as follows: Find the lowest available row and the lowest available column not already occupied, place the top left corner of the square there. If the grid height is `h`, the square's height is `sh`, then the target top row is `h - sh`. If no columns are occupied, then place at column 0.
"""

import numpy as np

def find_blue_square(grid):
    # Find the coordinates of the blue square (color 1).
    rows, cols = grid.shape
    blue_coords = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                blue_coords.append((r, c))
    if not blue_coords:
        return None, None, None, None

    min_r = min(coord[0] for coord in blue_coords)
    max_r = max(coord[0] for coord in blue_coords)
    min_c = min(coord[1] for coord in blue_coords)
    max_c = max(coord[1] for coord in blue_coords)
    width = max_c - min_c + 1
    height = max_r - min_r + 1

    # Check if it's a square.
    if width != height:
        return None, None, None, None
    
    return (min_r, min_c), width, height, blue_coords # return top-left, and all coordinates

def transform(input_grid):
    # Initialize output_grid as all zeros with the same shape as the input.
    output_grid = np.zeros_like(input_grid)

    # Find the blue square in the input grid.
    top_left, width, height, blue_coords = find_blue_square(input_grid)

    if top_left is not None:
        # Calculate the target position (bottom-left corner).
        target_row = output_grid.shape[0] - height
        target_col = 0

        # Copy the square to the target position.
        #for r in range(height):
        #    for c in range(width):
        #        output_grid[target_row + r, target_col + c] = 1
        for r, c in blue_coords:
            output_r = target_row + (r - top_left[0])
            output_c = target_col + (c - top_left[1])
            output_grid[output_r, output_c] = 1


    return output_grid