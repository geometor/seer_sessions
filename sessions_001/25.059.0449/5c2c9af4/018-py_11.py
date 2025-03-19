"""
The transformation identifies green pixels in the input grid and connects them. If two green pixels are directly adjacent (horizontally or vertically), the space between them is filled with green pixels. If two green pixels are diagonally adjacent, a green pixel is added to form a 2x2 green square.
"""

import numpy as np

def transform(input_grid):
    """
    Connects green pixels in the input grid.
    """
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Find green pixels
    green_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                green_pixels.append((r, c))

    # Connect adjacent and diagonal green pixels
    for i in range(len(green_pixels)):
        for j in range(i + 1, len(green_pixels)):
            r1, c1 = green_pixels[i]
            r2, c2 = green_pixels[j]

            # Check for horizontal adjacency
            if r1 == r2 and abs(c1 - c2) == 1:
                output_grid[r1, min(c1, c2) + 1:max(c1,c2)] = 3

            # Check for vertical adjacency
            if c1 == c2 and abs(r1 - r2) == 1:
                for r in range(min(r1, r2) + 1, max(r1,r2)):
                    output_grid[r,c1] = 3

            # Check for diagonal adjacency
            if abs(r1 - r2) == 1 and abs(c1-c2) == 1:
                output_grid[r1,c2] = 3
                output_grid[r2,c1] = 3

    return output_grid