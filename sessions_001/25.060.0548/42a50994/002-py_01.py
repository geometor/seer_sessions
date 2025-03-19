"""
The transformation rule filters colored pixels based on their adjacency to other pixels of the same color.
A colored pixel is retained if it has at least one horizontally or vertically adjacent neighbor of the same color.
Otherwise, the pixel is removed (set to color 0).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """
    Filters colored pixels in the input grid, keeping those with at least one
    same-color neighbor (horizontally or vertically).
    """
    input_grid = np.array(input_grid) # ensure numpy array
    output_grid = np.copy(input_grid)  # Initialize output as a copy
    rows, cols = input_grid.shape

    # Iterate through all pixels
    for row in range(rows):
        for col in range(cols):
            current_color = input_grid[row, col]

            # Only process non-black pixels
            if current_color != 0:
                neighbors = get_neighbors(input_grid, row, col)
                same_color_neighbors = 0
                for neighbor_row, neighbor_col in neighbors:
                    if input_grid[neighbor_row, neighbor_col] == current_color:
                        same_color_neighbors += 1

                # Remove pixel if no same-color neighbors
                if same_color_neighbors == 0:
                    output_grid[row, col] = 0

    return output_grid.tolist() # return as list