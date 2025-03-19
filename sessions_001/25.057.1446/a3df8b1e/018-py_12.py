"""
1. Count Blue Pixels: Determine the number of blue pixels in the input grid.
2. Zero Blue Pixels: If there are no blue pixels, the output grid is all black (all pixels are 0).
3. One Blue Pixel: If there is exactly one blue pixel, the output is a blue cross (+) shape. The cross is centered at the row and column where the blue pixel was found in the input. The arms of the cross extend to the edges of the grid.  All other pixels in the output grid are black (0).
4. Multiple Blue Pixels: If there are two or more blue pixels, the output grid is all black (all pixels are 0).
"""

import numpy as np

def count_blue_pixels(grid):
    # Count the number of blue pixels (value 1) in the grid
    count = 0
    for row in grid:
        for pixel in row:
            if pixel == 1:
                count += 1
    return count

def find_blue_pixel_position(grid):
    # Find the coordinates of the blue pixel (value 1)
    # Only used if exactly 1 blue pixel
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                return (i, j)
    return None  # should not happen, based on counts


def transform(input_grid):
    # initialize output_grid with the same dimensions and filled with 0s
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Count blue pixels
    blue_count = count_blue_pixels(input_grid)

    # Handle cases based on count
    if blue_count == 0:
        # All black output
        return output_grid
    elif blue_count == 1:
        # Create blue cross
        blue_row, blue_col = find_blue_pixel_position(input_grid)

        # Create cross
        for r in range(rows):
            for c in range(cols):
                # set entire row and col to blue
                if r == blue_row or c == blue_col:
                    output_grid[r,c] = 1
        return output_grid
    else:
        # Two or more blue pixels, all black output
        return output_grid