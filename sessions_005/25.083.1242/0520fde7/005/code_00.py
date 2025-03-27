"""
The transformation identifies gray pixels (5) adjacent to blue pixels (1) in the input grid. It then creates a 3x3 output grid. For each gray pixel that's adjacent to a blue pixel, a red pixel (2) is placed in the output grid. The red pixel is placed at the center of the output (1,1). All other pixels in the output grid are white (0).
"""

import numpy as np

def get_neighbors(grid, r, c):
    """
    Find the neighbors around grid[r][c]
    """
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c, 'above')) # above
    if r < rows - 1:
        neighbors.append((r + 1, c, 'below')) # below
    if c > 0:
        neighbors.append((r, c - 1, 'left')) # left
    if c < cols - 1:
        neighbors.append((r, c + 1, 'right')) # right
    
    return neighbors

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Iterate through the input grid to find '5's
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                # Check neighbors of '5'
                neighbors = get_neighbors(input_grid, r, c)
                for nr, nc, _ in neighbors:
                    if input_grid[nr, nc] == 1:
                        #Place 2 at center
                        output_grid[1, 1] = 2
                        break # only one red per gray

    return output_grid.tolist()