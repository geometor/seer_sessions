"""
Transforms an input grid by copying '5's and generating a checkerboard pattern of '1's and '5's around them, based on Manhattan distance.
"""

import numpy as np

def manhattan_distance(x1, y1, x2, y2):
    """Calculates the Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def transform(input_grid):
    """
    Transforms the input grid based on the location of '5's and a checkerboard pattern.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Copy Gray Pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                output_grid[r, c] = 5

    # 2. Checkerboard Expansion
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] != 5:  # Skip if already gray
                min_dist = float('inf')
                for r2 in range(rows):
                    for c2 in range(cols):
                        if input_grid[r2, c2] == 5:
                            dist = manhattan_distance(r, c, r2, c2)
                            min_dist = min(min_dist, dist)

                if min_dist != float('inf'):  # Ensure a '5' was found
                    if min_dist % 2 == 1:
                        output_grid[r,c] = 1
                    # removed setting even distances to 5, since 0 should be the default.

    return output_grid.tolist()