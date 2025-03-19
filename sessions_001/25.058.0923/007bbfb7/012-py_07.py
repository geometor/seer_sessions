"""
Expands the input grid by a factor of 3. Isolated yellow (4) pixels in the input grid become 3x3 blocks of yellow pixels in the output. Adjacent yellow pixels in the input expand to form connected rectangular regions in the output. Black (0) pixels remain black.
"""

import numpy as np

def get_neighbors(grid, r, c, include_diagonal=False):
    """Gets the neighbors of a cell, optionally including diagonals."""
    height, width = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if not include_diagonal and (abs(i) + abs(j) != 1):
                continue

            nr, nc = r + i, c + j
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def is_isolated(grid, r, c):
    """Checks if a yellow pixel is isolated (surrounded by black)."""
    if grid[r, c] != 4:
        return False
    neighbors = get_neighbors(grid, r, c, include_diagonal=True)
    for nr, nc in neighbors:
        if grid[nr, nc] == 4:
            return False
    return True
def expand_yellow_block(output_grid, r, c):
  """Expands isolated yellow pixels to 3x3"""
  for i in range(3):
    for j in range(3):
      output_grid[r*3 + i, c*3 + j] = 4

def transform(input_grid):
    """
    Expands the input grid by a factor of 3 and replicates/positions colored pixels.
    """
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 3, input_width * 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input grid to find yellow pixels.
    for r in range(input_height):
        for c in range(input_width):
            if input_grid[r, c] == 4:
                # Check if the yellow pixel is isolated.
                if is_isolated(input_grid, r, c):
                  expand_yellow_block(output_grid, r,c)
                else:
                    # expand and merge with adjacent areas
                    expand_yellow_block(output_grid, r, c)


    return output_grid