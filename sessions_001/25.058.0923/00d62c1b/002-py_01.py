"""
The input is a 6x6 grid. Green pixels (color 3) that are diagonally adjacent to other green pixels are changed to yellow (color 4). Specifically, in a diagonally adjacent pair of green pixels, the one more to the left is the pixel which is changed.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col, include_diagonal=True):
    """
    Gets the coordinates of adjacent pixels to a given cell, handling edges correctly, and supports optional diagonal adjaceny.
    """
    rows, cols = grid.shape
    adjacent_coords = []

    # Define possible neighbor offsets
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    if include_diagonal:
        offsets.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])  # Add diagonal offsets

    for dr, dc in offsets:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            adjacent_coords.append((new_row, new_col))

    return adjacent_coords

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is green.
            if output_grid[row, col] == 3:
                # Get the coordinates of adjacent pixels, including diagonals.
                adjacent_coords = get_adjacent_pixels(output_grid, row, col, include_diagonal=True)
                
                # Check for diagonally adjacent green pixels
                for adj_row, adj_col in adjacent_coords:
                    # make comparisons using tuple of row, col - smaller row, or if same row, then smaller col
                    if output_grid[adj_row, adj_col] == 3:
                        if (adj_row, adj_col) > (row, col) and abs(adj_row - row) == 1 and abs(adj_col - col) == 1:
                            # change this cell to 4, yellow
                            output_grid[row,col] = 4
                        elif (adj_row, adj_col) < (row, col) and abs(adj_row - row) == 1 and abs(adj_col - col) == 1:
                            # change adjacent pixel to 4, yellow
                            output_grid[adj_row,adj_col] = 4
                            
    return output_grid