"""
1.  **Delimiter Identification:** Find the row in the input grid where all cells have the value '4'. This row acts as a delimiter.
2.  **Top Section Extraction:** Consider only the section of the input grid *above* the delimiter row as the active region.
3.  **Contiguous Regions:** Identify contiguous regions of '1's in the active (top) section.  Adjacency is horizontal or vertical.
4.  **Transformation within regions:** Transform all 1s to 3s
    Transform all *interior* 0's in the active section to '3'.
    Transform all *edge* 0's to '3'

**Interior/Edge definition:**

-   An "interior" 0 is a 0 cell where *all* valid neighbors (up, down, left, right) within the active section are either a '1' or a '3', after the initial transformation
-   An "edge" 0 is a 0 where any valid neighbors are also 0
"""

import numpy as np

def find_delimiter_row(grid, delimiter_value=4):
    """Finds the row index that acts as a delimiter."""
    for i, row in enumerate(grid):
        if np.all(row == delimiter_value):
            return i
    return -1

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_interior_zero(grid, row, col):
    """Checks if a '0' cell is an interior zero."""
    if grid[row, col] != 0:
        return False

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r,c] == 0:
            return False
    return True

def is_edge_zero(grid,row,col):
    """Checks if a '0' is an edge zero"""
    if grid[row,col] != 0:
        return False
    
    neighbors = get_neighbors(grid,row,col)
    if not neighbors:
        return False
    for r,c in neighbors:
      if grid[r,c] == 0:
          return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    grid = np.array(input_grid)
    delimiter_row_index = find_delimiter_row(grid)
    top_grid = grid[:delimiter_row_index]
    output_grid = np.copy(top_grid)

    # Initially transform all 1s to 3s
    for r in range(top_grid.shape[0]):
      for c in range(top_grid.shape[1]):
        if top_grid[r,c] == 1:
          output_grid[r,c] = 3
        
    # Transform interior and edge 0s to 3
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            # if is_interior_zero(output_grid, r, c) or is_edge_zero(output_grid,r,c):
            if output_grid[r,c] == 0:
                output_grid[r,c] = 3

    return output_grid.tolist()