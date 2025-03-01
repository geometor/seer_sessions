"""
The input grid is expanded to double its size. The central yellow square expands
by one pixel in all directions. A magenta frame surrounds the output, and the
original corner maroon pixels are placed in the output corners.
"""

import numpy as np

def expand_yellow_square(input_grid, output_grid):
    """Expands the central yellow square by one pixel in all directions."""
    yellow_positions = np.array(np.where(input_grid == 4)).T
    if len(yellow_positions) == 0:
        return

    center_y = np.mean(yellow_positions[:, 0]).astype(int)
    center_x = np.mean(yellow_positions[:, 1]).astype(int)

    output_center_y = center_y * 2 + 1
    output_center_x = center_x * 2 + 1
    
    output_size = len(output_grid)
    
    # determine size of input yellow square
    input_yellow_size = yellow_positions[:,0].max() - yellow_positions[:,0].min() + 1
    
    # compute the size of expanded yellow square
    output_yellow_size = input_yellow_size + 2

    min_y = max(0, output_center_y - output_yellow_size // 2)
    min_x = max(0, output_center_x - output_yellow_size // 2)
    max_y = min(output_size -1, output_center_y + (output_yellow_size -1) // 2 + (output_yellow_size -1 )% 2)
    max_x = min(output_size -1, output_center_x + (output_yellow_size - 1) // 2 + (output_yellow_size -1 )% 2)

    for r in range(min_y, max_y + 1):
        for c in range(min_x, max_x + 1):
            output_grid[r][c] = 4

def place_maroon_corners(input_grid, output_grid):
    """Places maroon corner pixels from input to output grid corners."""
    input_size = len(input_grid)
    output_size = len(output_grid)

    if input_grid[0, 0] == 9:
        output_grid[0, 0] = 6
        output_grid[1,1] = 6
    if input_grid[0, -1] == 9:
        output_grid[0, -1] = 6
        output_grid[1,-2] = 9
    if input_grid[-1, 0] == 9:
        output_grid[-1, 0] = 6
        output_grid[-2,1] = 9
    if input_grid[-1, -1] == 9:
        output_grid[-1, -1] = 6
        output_grid[-2,-2] = 6

def create_magenta_frame(output_grid):
    """Creates a magenta frame around the output grid."""
    output_size = len(output_grid)
    output_grid[0, :] = 6  # Top row
    output_grid[-1, :] = 6  # Bottom row
    output_grid[:, 0] = 6  # Left column
    output_grid[:, -1] = 6  # Right column

def fill_second_row_col(output_grid):
    output_size = len(output_grid)

    output_grid[-1,::2] = 6
    output_grid[-1, 1::2] = 9

    output_grid[::2,0] = 6
    output_grid[1::2,0] = 6

    output_grid[::2,-1] = 6
    output_grid[1::2, -1] = 9
        

def transform(input_grid):
    # Initialize output grid with double the dimensions
    input_size = len(input_grid)
    output_size = input_size * 2
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Expand the central yellow square
    expand_yellow_square(input_grid, output_grid)

    # Create the magenta frame
    create_magenta_frame(output_grid)

    # Place maroon corners
    place_maroon_corners(input_grid, output_grid)
    
    # fill the second row and col
    fill_second_row_col(output_grid)

    return output_grid