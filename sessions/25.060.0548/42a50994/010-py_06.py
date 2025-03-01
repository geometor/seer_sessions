"""
The transformation rule identifies and removes magenta (6) pixels from the input grid based on their spatial relationships with neighboring magenta pixels. Magenta pixels that are part of diagonal lines of 3 or more, or part of a 2-pixel diagonal, are preserved. Other magenta pixels are changed to white (0).
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonals=True):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonals and (abs(i) + abs(j) != 1): #skip diag
                continue

            neighbor_row = row + i
            neighbor_col = col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def is_part_of_diagonal(grid, row, col):
    """Checks if a magenta pixel is part of a diagonal of 2 or more."""
    if grid[row, col] != 6:
        return False

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        if grid[r,c] == 6: # found magenta neighbor
            #check for diag - must be diff of 1
            if abs(row-r) + abs(col - c) == 2:
                return True

    return False

def is_part_of_long_diagonal(grid, row, col):
    """Checks if a magenta pixel is part of a diagonal of 3 or more."""
    if grid[row, col] != 6:
        return False
    
    rows, cols = grid.shape
    
    # Check diagonals in all four directions
    for row_direction, col_direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
        count = 1  # Count the current pixel
        # Extend in the positive direction
        r, c = row + row_direction, col + col_direction
        while 0 <= r < rows and 0 <= c < cols and grid[r, c] == 6:
            count += 1
            r += row_direction
            c += col_direction
        
        # Extend in the negative direction
        r, c = row - row_direction, col - col_direction
        while 0 <= r < rows and 0 <= c < cols and grid[r, c] == 6:
            count += 1
            r -= row_direction
            c -= col_direction
        
        if count >= 3:
            return True

    return False


def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is magenta
            if input_grid[row, col] == 6:
                # if isolated, or not part of group - remove it
                if not is_part_of_long_diagonal(input_grid, row, col) and not is_part_of_diagonal(input_grid, row, col):
                     output_grid[row, col] = 0
                #else keep

    return output_grid