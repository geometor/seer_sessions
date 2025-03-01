"""
The transformation identifies non-azure (8) pixels as "seeds".  For each azure pixel, it finds the nearest seed pixel.  The color of the azure pixel is then changed based on its Manhattan distance to that seed, alternating between two colors in a chessboard-like pattern.  The two alternating colors are determined by the color of the seed.  Some seed colors do not trigger a transformation.
"""

import numpy as np

def manhattan_distance(x1, y1, x2, y2):
    """Calculates the Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def find_nearest_seed(grid, x, y):
    """Finds the nearest non-azure seed pixel and its distance."""
    min_dist = float('inf')
    nearest_seed = None
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] != 8:
                dist = manhattan_distance(x, y, i, j)
                if dist < min_dist:
                    min_dist = dist
                    nearest_seed = (i, j)
    return nearest_seed, min_dist

def transform(input_grid):
    """Transforms the input grid according to the rules described above."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            # Process only azure pixels
            if input_grid[r, c] == 8:
                # Find the nearest seed and its distance
                nearest_seed, dist = find_nearest_seed(input_grid, r, c)

                if nearest_seed:
                    seed_color = input_grid[nearest_seed]
                    
                    # Apply transformation based on seed color and distance
                    if seed_color == 3: # Green seed
                        if dist % 2 == 1: # odd
                            output_grid[r,c] = 3
                        else: # even
                            output_grid[r, c] = 2
                    elif seed_color == 4:  # Yellow seed
                        if dist % 2 == 1:  # odd
                            output_grid[r, c] = 4
                        else:  # even
                            output_grid[r, c] = 1

    return output_grid