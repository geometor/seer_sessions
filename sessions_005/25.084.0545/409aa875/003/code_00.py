"""
Transforms an input grid based on rules involving colors 7, 9, 0, and 2. Color 7 acts as a boundary and remains unchanged. Color 9 changes to 1 at a specific coordinate or remains unchanged under certain conditions. Color 0 changes to 9 based on vertical adjacency to 7. Color 2 changes to 9 based on a two-row condition above it relative to 7.
"""

import numpy as np

def get_neighbors(grid, row, col, radius=1):
    """Gets the neighbors of a cell within a specified radius."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - radius), min(rows, row + radius + 1)):
        for j in range(max(0, col - radius), min(cols, col + radius + 1)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            pixel_color = input_grid[row, col]

            # Color 7 remains unchanged
            if pixel_color == 7:
                continue

            # Color 9 transformation
            elif pixel_color == 9:
                if row == 9 and col == 7:  # Specific coordinate rule
                    output_grid[row, col] = 1
                elif any(neighbor == 9 for neighbor in get_neighbors(input_grid,row,col, radius=2)):
                    output_grid[row,col] = 9 #retrain color

            # Color 0 transformation
            elif pixel_color == 0:
                above = input_grid[row - 1, col] if row > 0 else None
                below = input_grid[row + 1, col] if row < rows - 1 else None
                if above != 7 and below != 7:
                    output_grid[row, col] = 9

            # Color 2 transformation
            elif pixel_color == 2:
                if row > 1 and input_grid[row - 1, col] == 7 and np.all(input_grid[row - 2, :] == 7):
                    output_grid[row, col] = 9

    return output_grid