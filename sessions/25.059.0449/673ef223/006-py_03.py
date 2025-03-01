"""
Transforms the input grid by expanding an azure region horizontally to the left, introducing a yellow pixel to the right of the original azure pixel, maintaining the left red line, and transforming the right red line into an azure region.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of all pixels of the specified color.
    objects = []
    rows, cols = np.where(grid == color)
    for r, c in zip(rows, cols):
        objects.append((r, c))
    return objects

def find_rightmost_red_line_start(grid):
    # Find the starting column of the rightmost red line.
    red_pixels = find_objects(grid, 2)
    if not red_pixels:
        return None
    max_col = -1
    for _, c in red_pixels:
        if c > max_col:
            max_col = c
    return max_col

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    input_height, input_width = input_grid.shape

    # Find the azure and red pixels.
    azure_pixels = find_objects(input_grid, 8)
    red_pixels = find_objects(input_grid, 2)

    # 1. & 2. Left azure transformation.
    for r, c in azure_pixels:
        if c < input_width / 2:  # Check for left side
            for i in range(3):
                if c - i - 1 >= 0:  # Check boundary
                    output_grid[r, c - i - 1] = 8  # Expand azure to the left.

            # 3. Yellow Insertion
            if c + 1 < input_width:  # Check boundary
                output_grid[r, c + 1] = 4  # Add a yellow pixel to the right.

    # 4, 5, 6. Right red line transformation
    right_red_start = find_rightmost_red_line_start(input_grid)

    if right_red_start is not None:
        for r, c in red_pixels:
            if c == right_red_start: #check that we are using the right most line only
                offset = right_red_start - (c - 6) # calculate the offset
                for i in range(6):
                      if c - i - (offset-5) >= 0 :  # Check boundary, adjust for start to the left of red line.
                        output_grid[r, c - i - (offset - 5)] = 8  # azure, span 6 pixels


    # 7. Maintain left red line: No changes needed as we copied input_grid initially.

    return output_grid