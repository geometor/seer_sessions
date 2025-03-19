"""
1. **Identify Azure Columns:** Find all columns in the input grid that contain at least one azure (8) pixel.
2. **Diagonal Check:** If all azure pixels are on a diagonal line (where row index + column index = constant), move each azure pixel to the main diagonal (where row index = column index). The position of the red pixels is disregarded.
3. **Column Extension (if not diagonal):** If the azure pixels are *not* on a diagonal, and are all in the same column:
    *   Find the lowest row index containing an azure pixel in the identified column.
    *   Add one additional azure pixel immediately below.
    * If adding below will exceed the bounds, do nothing.
    * Ignore the red pixels.
"""

import numpy as np

def find_azure_columns(grid):
    """Finds the columns containing azure (8) pixels."""
    azure_columns = []
    for j in range(grid.shape[1]):
        for i in range(grid.shape[0]):
            if grid[i, j] == 8:
                azure_columns.append(j)
                break  # Move to the next column once an azure pixel is found
    return azure_columns

def is_diagonal(grid):
    """Checks if all azure pixels are on a diagonal line."""
    azure_coords = np.argwhere(grid == 8)
    if len(azure_coords) == 0:
        return False
    
    first_sum = azure_coords[0][0] + azure_coords[0][1]
    for i, j in azure_coords:
        if i + j != first_sum:
            return False
    return True

def move_to_main_diagonal(grid):
    """Moves all azure pixels to the main diagonal."""
    rows, cols = grid.shape
    output_grid = np.zeros_like(grid)  # Start with a blank grid of the same size
    azure_coords = np.argwhere(grid == 8)
    
    for i, j in azure_coords:
        new_index = min(i,rows-1, cols -1) #ensure within bounds
        output_grid[new_index, new_index] = 8
    return output_grid
        

def extend_column(grid, azure_columns):
    """Extends the azure pixels in the specified column by one."""
    output_grid = np.copy(grid)
    rows, _ = grid.shape

    for col in azure_columns:
        azure_indices = [i for i in range(rows) if grid[i, col] == 8]
        if azure_indices:
            lowest_row = max(azure_indices)
            if lowest_row + 1 < rows:
                output_grid[lowest_row + 1, col] = 8
    return output_grid

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    azure_columns = find_azure_columns(input_grid)

    if is_diagonal(input_grid):
        output_grid = move_to_main_diagonal(input_grid)
    elif len(set(azure_columns)) <= 1 : #all in the same column
        output_grid = extend_column(input_grid, azure_columns)
    else: #other cases, return input
        output_grid = np.copy(input_grid)

    return output_grid