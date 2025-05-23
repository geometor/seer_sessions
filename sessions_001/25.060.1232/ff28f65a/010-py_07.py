"""
Examine the input grid for 2x2 squares of color 2 (red). Create a smaller output grid where the presence of red squares is 
represented by a blue (1) pixel at the corresponding x-coordinate of the top-left corner of each red square.
All other cells in the output grid are white (0). The output grid's dimensions are determined by reducing the input grid size.
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

    # reduce dimensions
    output_height = input_grid.shape[0] -2
    output_width = input_grid.shape[1] -2

    
    # Initialize the output grid with all white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Mark the presence of red squares with blue (1) in the output
    for x, y in red_squares:
        if y == 1 and x < output_grid.shape[1]:  # y of 1 corresponds to what would become row 0
              output_grid[0,x-1] = 1
        if y == 3 and x-2 < output_grid.shape[1]: #y of 3 correspond to row 1
              output_grid[0,x-1] = 1

    return output_grid