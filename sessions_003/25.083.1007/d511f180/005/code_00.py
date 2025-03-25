"""
Replaces gray (5) pixels with azure (8) pixels if the gray pixel has any azure neighbor, including diagonally, and extends the replacement to contiguously connected gray pixels. The replacement process is iterative and happens in "waves".
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighboring pixel coordinates (including diagonals).
    """
    rows, cols = grid.shape
    neighbors = []

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors.append((new_row, new_col))
    return neighbors

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    while True:
        pixels_to_replace = []
        # Iterate through grid, using original values
        for row in range(rows):
            for col in range(cols):
                if input_grid[row, col] == 5: # Check *original* value
                    neighbors = get_neighbors(input_grid, row, col)
                    for neighbor_row, neighbor_col in neighbors:
                        if input_grid[neighbor_row, neighbor_col] == 8: #check *original* values
                            pixels_to_replace.append((row, col))
                            break  # move to next cell

        # If no pixels to replace, exit loop
        if not pixels_to_replace:
            break
        
        # Replace marked pixels
        for row, col in pixels_to_replace:
            output_grid[row, col] = 8

        # update the input_grid for the next wave
        input_grid = np.copy(output_grid)

    return output_grid