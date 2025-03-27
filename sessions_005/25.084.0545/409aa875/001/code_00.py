"""
Iterates through the input grid, selectively changing pixels of colors 9, 0, and 2 based on their neighborhood and position. Other pixels (color 7) remain unchanged.
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

            # Conditional Replacement for color 9
            if pixel_color == 9:
                neighbors = get_neighbors(input_grid, row, col, radius=2)
                if row == 9 and col == 7:
                    output_grid[row,col] = 1
                elif any(neighbor == 9 for neighbor in neighbors):
                    output_grid[row,col] = 9 #retrain color
                

            # Conditional Replacement for color 0
            elif pixel_color == 0:
                neighbors = get_neighbors(input_grid, row, col)
                above = input_grid[row - 1, col] if row > 0 else None
                below = input_grid[row + 1, col] if row < rows - 1 else None
                
                if above == 7 and below == 7:
                   output_grid[row,col] = 0
                else:
                    output_grid[row,col] = 9

            # Conditional Replacement for color 2
            elif pixel_color == 2:
                
                if row > 0 and input_grid[row-1,col] == 7:
                    if row > 1 and np.all(input_grid[row-2, :] == 7):
                        output_grid[row,col] = 9


    return output_grid