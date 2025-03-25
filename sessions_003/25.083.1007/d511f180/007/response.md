```python
"""
Replaces gray (5) pixels with the color of a non-gray, non-azure neighbor if that neighbor *does* have an azure neighbor. The replacement is iterative.
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=False):
    """
    Returns a list of neighboring pixel coordinates.
    """
    rows, cols = grid.shape
    neighbors = []

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            if not include_diagonal and (abs(dr) + abs(dc) != 1):
                continue # skip diagonals
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors.append((new_row, new_col))
    return neighbors

def has_azure_neighbor(grid, row, col):
    """
    Checks if a cell has any azure (8) neighbors, including diagonals.
    """
    neighbors = get_neighbors(grid, row, col, include_diagonal=True)
    for r, c in neighbors:
        if grid[r, c] == 8:
            return True
    return False

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    while True:
        pixels_to_replace = []
        replacement_colors = []
        # Iterate through grid, using original values
        for row in range(rows):
            for col in range(cols):
                if input_grid[row, col] == 5: # Check *original* value
                    if has_azure_neighbor(input_grid, row, col):
                        output_grid[row,col] = 8
                        continue

                    neighbors = get_neighbors(input_grid, row, col)
                    for neighbor_row, neighbor_col in neighbors:
                         if input_grid[neighbor_row, neighbor_col] != 5 and input_grid[neighbor_row, neighbor_col] != 8:
                            #check neighbors of neighbor
                            if has_azure_neighbor(input_grid, neighbor_row, neighbor_col):
                                pixels_to_replace.append((row, col))
                                replacement_colors.append(input_grid[neighbor_row,neighbor_col])
                                break # inner loop


        # If no pixels to replace, exit loop
        if not pixels_to_replace:
            break
        
        # Replace marked pixels
        for (row, col), color in zip(pixels_to_replace, replacement_colors):
            output_grid[row, col] = color

        # update the input_grid for the next wave
        input_grid = np.copy(output_grid)

    return output_grid
```