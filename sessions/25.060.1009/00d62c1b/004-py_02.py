"""
The transformation rule is to insert a yellow (4) pixel between any two adjacent green (3) pixels in the horizontal or vertical direction.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col, color):
    """
    Finds adjacent pixels of the specified color.
    """
    rows, cols = grid.shape
    adjacent = []
    
    # Check horizontal and vertical neighbors
    if row > 0 and grid[row-1, col] == color:
        adjacent.append((row - 1, col))  # Up
    if row < rows - 1 and grid[row+1, col] == color:
        adjacent.append((row + 1, col))  # Down
    if col > 0 and grid[row, col-1] == color:
        adjacent.append((row, col - 1))  # Left
    if col < cols - 1 and grid[row, col+1] == color:
        adjacent.append((row, col + 1))  # Right
        
    return adjacent

def transform(input_grid):
    """
    Transforms the input grid according to the rule: insert a yellow (4) pixel
    between any two adjacent green (3) pixels.
    """
    # Initialize the output grid with the same values as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for row in range(rows):
        for col in range(cols):
            # Check if current cell is green
            if input_grid[row, col] == 3:
                adjacent_greens = get_adjacent_pixels(input_grid, row, col, 3)
                # Check all adjacent cells to current one
                for adj_row, adj_col in adjacent_greens:
                  # insert a 4 between any two adjacent 3s
                  # check for vertical adjacency
                  if adj_row < row:
                      output_grid[row-1,col] = 4
                  elif adj_row > row:
                      output_grid[row+1,col] = 4
                  # check for horizontal adjacency
                  elif adj_col < col:
                      output_grid[row,col-1] = 4
                  elif adj_col > col:
                      output_grid[row, col+1] = 4

    return output_grid