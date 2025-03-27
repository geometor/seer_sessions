"""
The input grid is replicated nine times in a 3x3 grid arrangement. The center tile is the input grid directly, each of its horizontal and vertical neighbors are a single reflection of the tile (vertical or horizontal respectively). The diagonal neighbors of the center tile are the input tile reflected along both horizontal and vertical axis.
"""

import numpy as np

def mirror_horizontal(grid):
    return np.flip(grid, axis=1)

def mirror_vertical(grid):
    return np.flip(grid, axis=0)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((9, 9), dtype=int)
    input_grid = np.array(input_grid)

    # Place the original input grid in the center
    output_grid[3:6, 3:6] = input_grid

    # Top Left (mirrored vertically then horizontally)
    output_grid[0:3, 0:3] = mirror_horizontal(mirror_vertical(input_grid))
    # Top Center (mirrored vertically)
    output_grid[0:3, 3:6] = mirror_vertical(input_grid)
    # Top Right (mirrored vertically then horizontally)
    output_grid[0:3, 6:9] = mirror_horizontal(mirror_vertical(input_grid))

    # Left Center (mirrored horizontally)
    output_grid[3:6, 0:3] = mirror_horizontal(input_grid)
    # Right Center (mirrored horizontally)
    output_grid[3:6, 6:9] = mirror_horizontal(input_grid)

    # Bottom Left (mirrored horizontally then vertically)
    output_grid[6:9, 0:3] = mirror_horizontal(mirror_vertical(input_grid))
    # Bottom Center (mirrored vertically)
    output_grid[6:9, 3:6] = mirror_vertical(input_grid)
    # Bottom Right (mirrored horizontally then vertically)
    output_grid[6:9, 6:9] = mirror_horizontal(mirror_vertical(input_grid))
    

    return output_grid.tolist()