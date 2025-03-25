```python
"""
Iterate through each cell of the input grid. For each cell, examine its eight neighbors.
If a cell's color is *not* part of a contiguous region of the same color (i.e., connected to two or more others of same color), change its color to orange (7) in the output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in the grid."""
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            new_row, new_col = row + i, col + j
            if 0 <= new_row < rows and 0 <= new_col < cols:
                neighbors.append((new_row, new_col))
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            current_color = input_grid[row][col]
            neighbors = get_neighbors(input_grid, row, col)
            
            same_color_neighbors = 0
            for neighbor_row, neighbor_col in neighbors:
                if input_grid[neighbor_row][neighbor_col] == current_color:
                    same_color_neighbors += 1

            if same_color_neighbors < 2 :
                output_grid[row][col] = 7
            
    return output_grid
```