"""
Scan the input grid for 2x2 red squares. For each square found, place a blue pixel in the output grid. 
The output grid is smaller than the input by 2 in each dimension. The blue pixel's coordinates are 
the top-left coordinates of the red square, both reduced by 1. All other output cells are white.
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
        output_grid[y-1,x-1] = 1

    return output_grid