"""
Iterates through each pixel in the input grid. Identifies horizontal neighbors.
If the left neighbor's value equals the right neighbor's value, specific replacements are made.
If neighbors are 4, and center is 4 becomes 6, if center is 2 becomes 2.
If neighbors are 0, and center is 0 becomes 3, if center is 4 becomes 9.
"""

import numpy as np

def get_horizontal_neighbors(grid, row, col):
    """Gets the immediate left and right neighbors of a pixel.
       Returns None for a neighbor if it's out of bounds.
    """
    rows, cols = grid.shape
    left_neighbor = grid[row, col - 1] if col > 0 else None
    right_neighbor = grid[row, col + 1] if col < cols - 1 else None
    return left_neighbor, right_neighbor

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    output_grid = np.copy(input_grid)  # Initialize output grid
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Get horizontal neighbors
            left_neighbor, right_neighbor = get_horizontal_neighbors(input_grid, row, col)

            # Conditional Replacement
            if left_neighbor is not None and right_neighbor is not None:
                if left_neighbor == right_neighbor:
                    if left_neighbor == 4:
                        if output_grid[row,col] == 4:
                            output_grid[row, col] = 6
                        #elif output_grid[row,col] == 2:
                            #output_grid[row,col] = 2
                    elif left_neighbor == 0:
                        if output_grid[row,col] == 0:
                            output_grid[row, col] = 3
                        elif output_grid[row,col] == 4:
                            output_grid[row,col] = 9

    return output_grid