"""
Identifies gray (5) pixels in the input grid and transforms them into blue (1) pixels in the output grid.
The transformation expands each gray pixel into a 3x3 square of blue pixels.
If gray pixels are diagonally adjacent, a blue line connects them. White (0) pixels remain unchanged.
"""

import numpy as np

def get_gray_pixels(grid):
    # Find coordinates of all gray pixels (value 5).
    return np.argwhere(grid == 5)

def connect_diagonals(grid, gray_pixels):
    # Connect diagonally adjacent gray pixels with a blue line.
    output_grid = np.copy(grid)
    for i in range(len(gray_pixels)):
        for j in range(i + 1, len(gray_pixels)):
            row1, col1 = gray_pixels[i]
            row2, col2 = gray_pixels[j]
            
            if abs(row1 - row2) == abs(col1 - col2) and (abs(row1 - row2) >1 ): # Check for diagonal adjacency and distance >1
              
              # Determine direction
              row_step = 1 if row2 > row1 else -1
              col_step = 1 if col2 > col1 else -1

              # Draw the line
              current_row, current_col = row1 + row_step, col1 + col_step
              while current_row != row2:
                  output_grid[current_row, current_col] = 1
                  current_row += row_step
                  current_col += col_step

    return output_grid

def transform(input_grid):
    # Initialize output grid with zeros and same dimensions as input.
    output_grid = np.zeros_like(input_grid)

    # Find gray pixels in the input grid.
    gray_pixels = get_gray_pixels(input_grid)

    # Create 3x3 blue squares around each gray pixel.
    for row, col in gray_pixels:
        for i in range(max(0, row - 1), min(input_grid.shape[0], row + 2)):
            for j in range(max(0, col - 1), min(input_grid.shape[1], col + 2)):
                output_grid[i, j] = 1
                
    # Connect diagonal gray pixels
    output_grid = connect_diagonals(output_grid, gray_pixels)
    
    # Copy the original white (0) from input.
    output_grid[input_grid == 0] = 0
                
    return output_grid