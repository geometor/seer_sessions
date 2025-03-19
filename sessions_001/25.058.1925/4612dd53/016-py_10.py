"""
1.  **Copy:** The blue (1) pixels in the input grid are copied to the same positions in the output grid.
2.  **Border Detection:** Iterate through the input grid, find white color (0).
3. **Insert:** For each border, inset a red pixel (2).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row-1, col])
    if row < rows - 1:
        neighbors.append(grid[row+1, col])
    if col > 0:
        neighbors.append(grid[row, col-1])
    if col < cols - 1:
        neighbors.append(grid[row, col+1])
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)  # Start with a copy of the input

    rows, cols = input_grid.shape

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            # Find original color
            if input_grid[row, col] == 0:
                neighbors = get_neighbors(input_grid, row, col)
                for n in neighbors:
                    if n == 1:
                        output_grid[row,col] = 2
                        break
            
    return output_grid