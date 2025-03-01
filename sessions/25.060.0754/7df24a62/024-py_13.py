"""
1.  **Top-Left Region Rule:** Any yellow pixel (4) located within the top-left 3x6 region of the grid is changed to blue (1).

2.  **Blue Square Expansion Rule:** Any yellow pixel (4) that is adjacent to a blue (1) square region (of size at least 2x2), and where changing that yellow pixel to blue (1) would result in the blue region becoming a larger rectangle with dimensions of at least 2x3, 3x2 or 3x3, is changed to blue (1).

3.  **Isolated Yellow Pixel Rule:** Any yellow pixel (4) that does not meet conditions of either rule 1 or rule 2 above remains yellow (4).
"""

import numpy as np

def get_neighbors(grid, row, col, include_diagonal=True):
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

def check_expansion(grid, row, col):
    """
    Checks if changing a yellow pixel to blue would expand an existing blue square.
    Assumes that there is at least one 2x2 square that has one of it adjacent cells yellow
    """
    if grid[row, col] != 4:
        return False
    rows, cols = grid.shape
    
    # Create a temporary grid for testing
    temp_grid = np.copy(grid)
    temp_grid[row, col] = 1

    #now that this cell is blue, check if this forms a large square that contains the original position
    for size_x in range(2,4):
      for size_y in range(2,4):
        for r_start in range(max(0, row - size_x + 1), min(rows-size_x+1,row+ 1)):
            for c_start in range(max(0, col - size_y + 1), min(cols-size_y+1,col+ 1)):
                is_square = True
                for i in range(size_x):
                  for j in range(size_y):
                    if not (0 <= r_start+i < rows and 0 <= c_start+j < cols and temp_grid[r_start + i, c_start + j] == 1):
                      is_square = False
                      break
                  if not is_square:
                    break

                if is_square:
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

            # Check the expansion condition for other yellow pixels
            elif output_grid[row, col] == 4:
                if check_expansion(input_grid, row, col):
                        output_grid[row, col] = 1
                

    return output_grid