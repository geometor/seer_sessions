"""
Replaces gray (5) pixels with azure (8) pixels if the gray pixel has any azure neighbor, checking first if a gray (5) is fully surrounded by azure(8)s
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighboring pixel values.
    """
    rows, cols = grid.shape
    neighbors = []
    
    # Orthogonal neighbors
    if row > 0:
        neighbors.append((grid[row - 1, col], (row-1, col)))  # Up
    if row < rows - 1:
        neighbors.append((grid[row + 1, col], (row+1, col)))  # Down
    if col > 0:
        neighbors.append((grid[row, col - 1], (row, col-1)))  # Left
    if col < cols - 1:
        neighbors.append((grid[row, col + 1], (row, col+1)))  # Right
        
    # Diagonal
    if row > 0 and col > 0:
        neighbors.append((grid[row - 1, col-1], (row-1, col-1)))  # Up-left
    if row > 0 and col < cols - 1:
        neighbors.append((grid[row - 1, col+1], (row-1, col+1)))  # Up-Right
    if row < rows-1 and col > 0:
        neighbors.append((grid[row + 1, col - 1], (row+1, col-1)))  # Down-Left
    if row < rows - 1 and col < cols - 1:
        neighbors.append((grid[row+1, col+1], (row+1, col+1)))   # Down-Right

    return neighbors

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # First pass: Check for fully surrounded 5s
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5:
                neighbors = get_neighbors(output_grid, row, col)
                orthogonal_neighbors = []
                # check orthogonal neighbors
                if row > 0:
                    orthogonal_neighbors.append(output_grid[row - 1, col])
                if col > 0:
                    orthogonal_neighbors.append(output_grid[row, col-1])
                if row < rows - 1:
                    orthogonal_neighbors.append(output_grid[row+1, col])
                if col < cols - 1:
                    orthogonal_neighbors.append(output_grid[row, col+1])
                
                if all(n == 8 for n in orthogonal_neighbors):
                    output_grid[row, col] = 8

    # Second pass: Iterate through the grid and check for any 8 neighbor, replace 5 with 8.
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5:
                neighbors = get_neighbors(output_grid, row, col)
                if any(n[0] == 8 for n in neighbors):
                    output_grid[row, col] = 8

    return output_grid