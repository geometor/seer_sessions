"""
1.  **Top-Left Region:** Any yellow pixel (4) within the top-left 3x6 region of the grid is changed to blue (1).

2.  **Blue Region Adjacency:** Any yellow pixel (4) that is *directly* adjacent (up, down, left or right) to a blue region (1) that has a size of at least 2x2. The shape could be larger than 2x2.

3.  **All Other Yellow Pixels:** Any yellow pixel (4) not meeting condition 1 or 2, remains Yellow.
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=False):
    """Gets the neighbors of a pixel, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (abs(i) + abs(j) != 1):
                continue
            neighbor_row, neighbor_col = row + i, col + j
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                neighbors.append((neighbor_row, neighbor_col))
    return neighbors

def is_part_of_blue_region(grid, row, col):
    """Checks if a blue pixel is part of a 2x2 or larger blue region."""
    if grid[row, col] != 1:
        return False

    rows, cols = grid.shape

    # Check for 2x2 regions around the current pixel
    for r_start in range(max(0, row - 1), min(rows - 1, row + 1)):
        for c_start in range(max(0, col - 1), min(cols - 1, col + 1)):
            is_region = True
            for i in range(2):
                for j in range(2):
                    if grid[r_start + i, c_start + j] != 1:
                        is_region = False
                        break
                if not is_region:
                    break
            if is_region:
                return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for row in range(rows):
        for col in range(cols):
            #top left region special case
            if row < 3 and col < 6:
                if output_grid[row,col] == 4:
                   output_grid[row, col] = 1

            # Check for adjacency to a blue region
            elif output_grid[row, col] == 4:
                neighbors = get_neighbors(output_grid, row, col)
                for n_row, n_col in neighbors:
                    if is_part_of_blue_region(output_grid, n_row, n_col):
                        output_grid[row,col] = 1
                        break # Once changed, no need to check other neighbors

    return output_grid