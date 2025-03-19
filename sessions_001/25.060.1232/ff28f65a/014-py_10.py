"""
1. Scan the Input Grid: Examine the input grid to identify all 2x2 squares where all four pixels are red (color 2).

2. Determine Output Grid Size:
    The output grid's height is input_height - (red-square height + red_square.height - 2).
    The output grid's width is input_width - (red_square.width + red-square.width - 2).

3. Place Blue Pixels: For each 2x2 red square found:
    *   Calculate the output x-coordinate: `output_x = x - (input_grid.shape[1] - output_grid.shape[1])`
    *   Calculate the output y-coordinate: `output_y = y - (input_grid.shape[0] - output_grid.shape[0])`

        where `x` and `y` are the top-left coordinates of the 2x2 red square in the *input* grid.
    *   If the calculated `output_x` and `output_y` are within the bounds of the output grid, place a blue pixel (color 1) at the calculated coordinates in the output grid.

4. All Other Pixels: All other pixels in the output grid should be white (color 0).
"""

import numpy as np

def find_squares(grid, color, size):
    """Finds top-left coordinates of squares of a specific color and size."""
    squares = []
    height, width = grid.shape
    for y in range(height - size + 1):
        for x in range(width - size + 1):
            if grid[y, x] == color and np.all(grid[y:y+size, x:x+size] == color):
                squares.append((x, y))  # Note: Appending (x, y)
    return squares

def transform(input_grid):
    # Find red (2) 2x2 squares in the input grid
    red_squares = find_squares(input_grid, 2, 2)

    # Determine output grid size
    output_height = input_grid.shape[0] - (2 + 2 - 2)
    output_width = input_grid.shape[1] - (2 + 2 - 2)
    
    # Initialize the output grid with all white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place blue pixels based on red square locations
    for x, y in red_squares:
        output_x = x - (input_grid.shape[1] - output_grid.shape[1])
        output_y = y - (input_grid.shape[0] - output_grid.shape[0])

        if 0 <= output_x < output_width and 0 <= output_y < output_height:
            output_grid[output_y, output_x] = 1

    return output_grid