"""
The transformation rule involves identifying an azure pixel (value 8) in the input grid and generating an "L"-shaped path of gray pixels (value 5) originating from the azure pixel's location. The "L" shape's orientation and dimensions are determined by the edges of a black rectangle present in the input grid. The segments of the "L" extend towards the edges of the black rectangle.
"""

import numpy as np

def find_azure_pixel(grid):
    # Find the coordinates of the azure pixel (value 8).
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 8:
                return (r, c)
    return None  # Should not happen, based on task description.

def find_black_rectangle(grid):
    # Find the top-left and bottom-right coordinates of the black rectangle.
    rows, cols = len(grid), len(grid[0])
    min_r, min_c = rows, cols
    max_r, max_c = -1, -1

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:  # Black pixel
                min_r = min(min_r, r)
                min_c = min(min_c, c)
                max_r = max(max_r, r)
                max_c = max(max_c, c)

    return (min_r, min_c), (max_r, max_c)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the azure pixel.
    azure_pos = find_azure_pixel(input_grid)

    if azure_pos is None:
        return output_grid # Should not happen

    # Find the black rectangle.
    (min_r, min_c), (max_r, max_c) = find_black_rectangle(input_grid)

    # Determine L-shape parameters.
    r, c = azure_pos

    # Determine lengths of segments based on black rectangle edges
    up_length = r - min_r
    down_length = max_r - r
    left_length = c - min_c
    right_length = max_c - c

    # Determine the orientation and lengths based on position relative to the rectangle
    if up_length < down_length:  #up
        length1 = up_length
        if left_length < right_length: #left
            length2 = left_length
            direction = "up-left"
        else:  #right
            length2 = right_length
            direction = "up-right"
    else:   #down
        length1 = down_length
        if left_length < right_length:  #left
            length2 = left_length
            direction = "down-left"

        else:   #right
            length2 = right_length
            direction = "down-right"
            

    # Draw the L-shape based on the determined parameters.

    if direction == "up-left":
        for i in range(1, length1 + 1):
            output_grid[r - i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r - length1, c - i] = 5
    elif direction == "down-left":
        for i in range(1, length1 + 1):
            output_grid[r + i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r + length1, c - i] = 5
    elif direction == "down-right":
        for i in range(1, length1 + 1):
            output_grid[r + i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r + length1, c + i] = 5
    elif direction == "up-right":
        for i in range(1, length1 + 1):
            output_grid[r - i, c] = 5
        for i in range(1, length2 + 1):
            output_grid[r - length1, c + i] = 5

    output_grid[r,c] = 5 # set the azure pixel

    return output_grid