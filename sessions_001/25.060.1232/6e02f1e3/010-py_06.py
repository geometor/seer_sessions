"""
The input grid is transformed into an output grid of the same dimensions. 
Each cell in the input grid is examined. If a cell has two or more diagonally 
adjacent neighbors with colors different from itself, the corresponding 
cell in the output grid is set to gray (5). Otherwise, the corresponding 
cell in the output grid is set to white (0).
"""

import numpy as np

def get_diagonal_neighbors(grid, row, col):
    # Helper function to get the colors of diagonally adjacent neighbors
    rows, cols = grid.shape
    neighbors = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            if 0 <= row + i < rows and 0 <= col + j < cols:
                neighbors.append(grid[row + i, col + j])
    return neighbors

def transform(input_grid):
    # Initialize output_grid with the same dimensions, filled with white (0)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each cell of the input_grid
    for row in range(rows):
        for col in range(cols):
            # Get the colors of the diagonally adjacent neighbors
            diagonal_neighbors = get_diagonal_neighbors(input_grid, row, col)
            
            # Count the number of diagonal neighbors with different colors
            current_color = input_grid[row, col]
            different_color_count = 0
            for neighbor_color in diagonal_neighbors:
                if neighbor_color != current_color:
                    different_color_count += 1

            # Apply the transformation rule
            if different_color_count >= 2:
                output_grid[row, col] = 5  # Set to gray (5)
            else:
                output_grid[row, col] = 0  # Set to white (0)

    return output_grid