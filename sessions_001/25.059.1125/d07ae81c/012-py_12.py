"""
1. **Identify Seed Pixels:** Locate all pixels of color 8 (azure) and the single pixel that is color 2(red) in the input grid.

2. **Propagate Azure:** For each azure pixel, perform a flood-fill operation, replacing adjacent blue (1) pixels with azure, but only once per seed pixel, and not diagonally.

3. **Propagate Red:** For *each* blue (1) pixel adjacent to the initially identified single input red (2) pixel perform a flood-fill of red (2)s, and replace adjacent blue(1) pixel, but only once per seed pixel. Extend this to include diagonals.
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def flood_fill_adjacent(grid, start_row, start_col, replacement_color, target_color, diagonal):
    """Performs a flood fill, replacing only directly adjacent pixels."""
    rows, cols = grid.shape
    queue = [(start_row, start_col)]
    visited = set()

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited:
            continue
        visited.add((row, col))

        if grid[row, col] == target_color:
           grid[row,col] = replacement_color


        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        if diagonal:
            neighbors.extend([(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)])

        for r, c in neighbors:
            if 0 <= r < rows and 0 <= c < cols: # and grid[r,c] == target_color
               if (r,c) not in visited: # and grid[r, c] == target_color:
                    queue.append((r,c))


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find seed pixels
    azure_pixels = get_pixels_by_color(input_grid, 8)
    red_pixels = get_pixels_by_color(input_grid, 2)
    if len(red_pixels) > 0:
      single_red_pixel = red_pixels[0]  # Assuming there's only one
    else:
       return output_grid # safeguard
    
    # Propagate Azure
    for row, col in azure_pixels:
        flood_fill_adjacent(output_grid, row, col, 8, 1, diagonal=False)

    # Propagate Red from immediate neighbours of the intial red
    initial_red_neighbors = []

    r,c = single_red_pixel
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                 (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
        
    for nr, nc in neighbors:
        if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr,nc] == 1:
            initial_red_neighbors.append((nr,nc)) # collect intial blue neighbours
    
    for row, col in initial_red_neighbors:
        flood_fill_adjacent(output_grid, row, col, 2, 1, diagonal=True)

    return output_grid