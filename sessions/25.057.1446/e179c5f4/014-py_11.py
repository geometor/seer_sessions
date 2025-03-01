"""
1.  **Background Replacement:** Change all white (0) pixels in the input grid to azure (8).
2.  **Shape Creation:** Create a cross/plus sign shaped object.
    -   The cross is made of blue (1) pixels.
    -   The dimensions of the cross is 3x3.
    -    The center of the cross will be placed at the input blue pixel.
3. Render the output grid with background and shape.
"""

import numpy as np

def find_pixel_location(grid, color):
    # Find the location of the first pixel of the specified color.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                return (i, j)
    return None

def transform(input_grid):
    # initialize output_grid as a copy of input grid
    output_grid = np.copy(input_grid)

    # change all 0 (white) to 8 (azure)
    output_grid[output_grid == 0] = 8

    # Find the location of the blue (1) pixel in the input grid.
    blue_pixel_location = find_pixel_location(input_grid, 1)

    # Create cross 
    if blue_pixel_location:
        row, col = blue_pixel_location
        # define cross shape, size 3
        output_grid[row, col] = 1
        if row > 0:
          output_grid[row - 1, col] = 1
        if row < output_grid.shape[0] - 1:
          output_grid[row + 1, col] = 1
        if col > 0:
          output_grid[row, col - 1] = 1
        if col < output_grid.shape[1] -1:
          output_grid[row, col+1] = 1
        

    return output_grid