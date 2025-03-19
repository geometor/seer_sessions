"""
1.  **Identify Azure Pixels:** Locate all pixels with the value '8' (azure) within the input grid.

2.  **Analyze Connectivity:** Determine connected regions of azure pixels. Pixels are considered connected if they are adjacent horizontally or vertically.

3.  **Conditional Removal**:
    *   Iterate over azure pixels.

    *   If an azure pixel is a part of the perimeter, remove this unless it has a neighbor that is part of the same perimeter.

    *   Remove "island" azure pixels that does not have azure neighbors

4.  **Output:** Generate the modified grid, where the selected azure pixels have been replaced with '0' (white).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def is_island(grid, row, col, color):
    """Checks if a pixel is an 'island' (no neighbors of the same color)."""
    if grid[row,col] != color:
        return False

    for nr, nc in get_neighbors(grid, row, col):
        if grid[nr, nc] == color:
            return False  # Has a neighbor of the same color
    return True

def is_perimeter(grid, row, col, color):
    """Checks if a given cell is a perimeter of the given color"""
    if grid[row, col] != color:
      return False

    rows, cols = grid.shape
    if row == 0 or row == rows-1 or col == 0 or col == cols - 1:
        return True
    
    for nr, nc in get_neighbors(grid, row, col):
        if grid[nr, nc] != color:
            return True

    return False


def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    azure = 8

    # Iterate over all azure pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == azure:
                # Remove island pixels.
                if is_island(output_grid, r, c, azure):
                    output_grid[r, c] = 0

                # Remove perimeter unless it is connected to neighbor
                elif is_perimeter(output_grid, r, c, azure):
                    neighbor_count = 0
                    for nr, nc in get_neighbors(output_grid, r, c):
                        if is_perimeter(output_grid, nr, nc, azure) and output_grid[nr, nc] == azure :
                            neighbor_count += 1
                    if neighbor_count == 0:
                        output_grid[r,c] = 0

    return output_grid