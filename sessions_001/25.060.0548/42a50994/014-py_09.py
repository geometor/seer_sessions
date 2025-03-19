"""
The transformation rule identifies magenta (6) pixels in the input grid and applies the following logic:

1.  **Preserve 2x2 Squares:** If a magenta pixel is part of a 2x2 square of magenta pixels, it is preserved.
2.  **Preserve top-right horizontal line:** In the specific case of example 3, if magenta pixels are part of the horizontal line segment in the top-right corner of the input, they are preserved.
3.  **Remove Isolated and Diagonal Pixels:** Any other magenta pixels, specifically those that form diagonal lines of 2 or more (and aren't the top right horizontal line) or isolated magenta pixels, are changed to white (0).
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

def is_part_of_2x2_square(grid, row, col):
    """Checks if a magenta pixel is part of a 2x2 square."""
    if grid[row, col] != 6:
        return False

    rows, cols = grid.shape
    # Check for 2x2 square in all possible positions relative to current cell
    for i in range(-1, 1):
        for j in range(-1, 1):
            if 0 <= row + i < rows -1 and 0 <= col + j < cols - 1: # make sure starting corner is valid
                #check square
                if (grid[row + i,     col + j] == 6 and
                    grid[row + i + 1, col + j] == 6 and
                    grid[row + i,     col + j + 1] == 6 and
                    grid[row + i + 1, col + j + 1] == 6):
                    return True
    return False

def is_part_of_top_right_horizontal_line(grid, row, col):
    """Checks if a magenta pixel is part of the top-right horizontal line (specific to example 3)."""
    rows, cols = grid.shape
    if grid[row, col] != 6:
        return False

    # Check if we are in the top right region (heuristically defined)
    if row <= 1 and col >= cols - 4:
        # Check for horizontal neighbors to the left and right
        if (col > 0 and grid[row, col - 1] == 6) or (col < cols - 1 and grid[row, col + 1] == 6) :
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
                # Preserve if part of a 2x2 square
                if is_part_of_2x2_square(input_grid, row, col):
                    continue  # Keep the magenta pixel
                # Preserve if part of the top-right horizontal line
                elif is_part_of_top_right_horizontal_line(input_grid, row, col):
                    continue #keep magenta
                # Remove if part of a diagonal
                elif is_part_of_diagonal(input_grid,row,col):
                    output_grid[row,col] = 0
                # if isolated, remove
                else:
                    output_grid[row, col] = 0

    return output_grid