"""
Iterates through the input grid, identifies pixels with a value of 0, and replaces them with the color of the most immediate non-zero neighbor.
If the zero-valued pixel is on the border of similar colored objects, it takes the color of the neighboring group.
"""

import numpy as np

def get_neighbor_colors(grid, row, col):
    """Gets the colors of the immediate neighbors (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = {}

    if row > 0:
        neighbors[(row - 1, col)] =  grid[row - 1, col] # Up
    if row < rows - 1:
        neighbors[(row + 1, col)] = grid[row + 1, col] # Down
    if col > 0:
        neighbors[(row, col-1)] = grid[row, col - 1] # Left
    if col < cols - 1:
        neighbors[(row, col + 1)] = grid[row, col + 1] # Right
    return neighbors
    

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 0:
                # Get the colors of the immediate neighbors.
                neighbor_colors = get_neighbor_colors(input_grid, row, col)
                #find the neighbor and change the value

                neighbor_values = list(neighbor_colors.values())

                if (len(neighbor_values) > 0):
                  non_zero_neighbors = [val for val in neighbor_values if val!=0]
                  if (len(non_zero_neighbors) > 0):
                    output_grid[row, col] = non_zero_neighbors[0]

    return output_grid