"""
Preserve the yellow shape. For the azure shape, "outline" the shape by keeping the edges and making azure pixels within the shape
into white (0). An "edge" here is determined by pixels that don't have neighbors
on all 4 sides (up, down, left, right).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
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
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Process only azure (8) pixels
            if input_grid[row, col] == 8:
                neighbors = get_neighbors(input_grid, row, col)
                neighbor_values = [input_grid[r, c] for r, c in neighbors]
                # Check if all neighbors are also azure (8)
                if all(val == 8 for val in neighbor_values) and len(neighbor_values) == 4:
                    output_grid[row, col] = 0  # Set to white (0) if all neighbors are azure

    return output_grid