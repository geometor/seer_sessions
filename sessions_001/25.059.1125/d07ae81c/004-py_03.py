"""
The transformation rule distinguishes between "special pixels" (those not having the majority color) and "background pixels" (those having the majority color). Special pixels maintain their color. Background pixels are transformed based on the presence of specific colors among their immediate neighbors. Gray(5) and Magenta(6) are unchanged. If azure (8) is present, change to azure(8). Specific color interactions occur between 1, 4, and 8. Alternating fills occur in vertically striped patterns involving colors 3, 6, and 8.
"""

import numpy as np

def get_special_pixels(grid):
    """
    Identifies "special" pixels (those not of the majority color).
    """
    values, counts = np.unique(grid, return_counts=True)
    majority_color = values[np.argmax(counts)]
    special_pixels = {}
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != majority_color:
                special_pixels[(r, c)] = grid[r, c]
    return special_pixels, majority_color

def get_neighbors(grid, r, c):
    """Gets the 8 neighbors (including diagonals) of a pixel."""
    neighbors = {}
    for i in range(max(0, r - 1), min(grid.shape[0], r + 2)):
        for j in range(max(0, c - 1), min(grid.shape[1], c + 2)):
            if (i, j) != (r, c):
                neighbors[(i, j)] = grid[i, j]
    return neighbors

def is_vertically_striped(grid, special_pixels, colors):
    """Checks if special pixels form vertical stripes with given colors."""

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r,c) in special_pixels and grid[r,c] == colors[0]:
              if c > 0 and grid[r,c-1] == colors[1]:
                return True
              if c < grid.shape[1] -1 and grid[r,c+1] == colors[1]:
                return True
    return False
    

def transform(input_grid):
    grid = np.array(input_grid)
    output_grid = np.copy(grid)
    special_pixels, majority_color = get_special_pixels(grid)

    # Special pixel mapping (maintain color)
    special_pixel_mapping = {
        1: 1, 2: 2, 3: 3, 4: 4, 8: 8, 5:5, 6:6
    }

    for (r, c), color in special_pixels.items():
        output_grid[r, c] = special_pixel_mapping.get(color, color)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == majority_color:
                neighbors = get_neighbors(grid, r, c)
                neighbor_colors = list(neighbors.values())
                neighbor_special_pixels = [(nr, nc) for (nr, nc) in neighbors if (nr,nc) in special_pixels]

                if 5 in [grid[nr,nc] for (nr,nc) in neighbor_special_pixels] or 6 in [grid[nr,nc] for (nr,nc) in neighbor_special_pixels]:
                    continue

                if 8 in neighbor_colors:
                    output_grid[r, c] = 8
                    continue

                # check vertical stripes for alternating fill
                if is_vertically_striped(grid, special_pixels, [3,8]):
                  if c > 0 and grid[r,c-1] == 8 and (r,c-1) in special_pixels:
                    output_grid[r,c] = 3
                    continue
                elif is_vertically_striped(grid, special_pixels, [8,3]):
                  if c>0 and grid[r,c-1] == 3 and (r,c-1) in special_pixels:
                    output_grid[r,c] = 6
                    continue
                elif is_vertically_striped(grid, special_pixels, [3,0]):
                  if c>0 and grid[r,c-1] == 3 and (r,c-1) in special_pixels:
                    output_grid[r,c] = 6
                    continue
                
                # Special interaction between 1 and 8
                if 1 in neighbor_colors:
                    output_grid[r,c] = 8
                    continue
                

    return output_grid.tolist()