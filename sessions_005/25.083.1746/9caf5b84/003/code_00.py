"""
Identify contiguous regions of the same color. Determine the outer border of each region.
Change the color of pixels on the outer border to orange (7).
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

def is_outer_border(grid, row, col, region_color):
    """Checks if a pixel is on the outer border of a contiguous region."""
    neighbors = get_neighbors(grid, row, col)
    same_color_neighbors = 0
    for neighbor_row, neighbor_col in neighbors:
        if grid[neighbor_row][neighbor_col] == region_color:
            same_color_neighbors += 1

    # Check if the cell has fewer than 2 same-color neighbors, making it a border
    if same_color_neighbors < 2 and same_color_neighbors > 0:
          return True
    
    if same_color_neighbors == 0:
          return False

    # Additional check to determine real borders and not parts of a big component
    if len(neighbors) < 8:
      return True

    #If has two or more neighbors and is not on the border
    return False

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])
    visited = set()

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            current_color = input_grid[row][col]
            if (row, col) not in visited:
                if is_outer_border(input_grid, row, col, current_color):
                      output_grid[row][col] = 7
                visited.add((row,col))
            
    return output_grid