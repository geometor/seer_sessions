```python
"""
Replaces gray (5) pixels with azure (8) pixels if the gray pixel has any azure neighbor, including diagonally, and extends the replacement to contiguously connected gray pixels.
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

    def replace_contiguous_gray(row, col):
        """
        Recursively replaces contiguous gray pixels with azure.
        """
        if output_grid[row, col] != 5:
            return

        output_grid[row, col] = 8
        neighbors = get_neighbors(output_grid, row, col)
        for neighbor_row, neighbor_col in neighbors:
            replace_contiguous_gray(neighbor_row, neighbor_col)

    # Iterate through the grid
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5:
                neighbors = get_neighbors(output_grid, row, col)
                for neighbor_row, neighbor_col in neighbors:
                    if output_grid[neighbor_row, neighbor_col] == 8:
                        replace_contiguous_gray(row, col)
                        break # move onto next cell after finding an 8 and replacing

    return output_grid
```