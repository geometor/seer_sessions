"""
1.  **Identify Azure Regions:** Find all contiguous regions of azure (8) pixels. Consider each of these regions as a single "object."
2.  **Locate Potential Extensions:** For each azure region, find all empty (0) cells that are directly adjacent (up, down, left, or right – *not* diagonally) to any azure pixel in that region.
3. **Conditional Blue Fill:** For any cell identified as a candidate, fill it with a blue (1) pixel if the azure pixel it is adjacent to also has another azure pixel that is directly adjacent to *it*.
4.  **Result:** The output grid is the same as the input grid, except for the blue pixels added according to the rule above. No azure pixels are changed or removed.
"""

import numpy as np

def get_neighbors(grid, row, col, color=None):
    """Returns the coordinates of the neighbors of a cell, optionally filtering by color."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))

    if color is not None:
        neighbors = [(r, c) for r, c in neighbors if grid[r, c] == color]
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is azure (8)
            if input_grid[r, c] == 8:
                # Get the neighbors of the current azure pixel
                neighbors = get_neighbors(input_grid, r, c)
                # Check each neighbor
                for nr, nc in neighbors:
                    # If the neighbor is empty (0), check condition for adding blue.
                    if input_grid[nr, nc] == 0:
                        #check if the current azure has another azure neighbor.
                        azure_neighbors = get_neighbors(input_grid, r, c, color=8)
                        if len(azure_neighbors) > 0:
                            output_grid[nr, nc] = 1


    return output_grid