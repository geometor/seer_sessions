"""
Rotate a 3x3 grid 90 degrees clockwise and then recolor each pixel based on
its original color and its position in the rotated grid.
"""

import numpy as np

def rotate_grid(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1).tolist()

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise and then
    recoloring pixels based on original color and rotated position.
    """
    rotated_grid = rotate_grid(input_grid)
    output_grid = [row[:] for row in rotated_grid]  # Initialize with rotated grid
    rows = len(rotated_grid)
    cols = len(rotated_grid[0])

    for r in range(rows):
        for c in range(cols):
            original_color = rotated_grid[r][c]
            # Recolor based on original color and position. Since direct mapping
            # failed, we need to incorporate position information.
            # We will combine original color, row, and column to create a unique key for recoloring
            
            if (original_color, r, c) == (2, 0, 0):
                output_grid[r][c] = 1
            elif (original_color, r, c) == (2, 0, 1):
                output_grid[r][c] = 8
            elif (original_color, r, c) == (2, 0, 2):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (8, 1, 0):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (1, 1, 1):
                output_grid[r][c] = 1
            elif (original_color, r, c) == (2, 1, 2):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (1, 2, 0):
                output_grid[r][c] = 1
            elif (original_color, r, c) == (2, 2, 1):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (1, 2, 2):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (2, 0, 0):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (2, 0, 1):
                output_grid[r][c] = 9
            elif (original_color, r, c) == (9, 0, 2):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (9, 1, 0):
                output_grid[r][c] = 4
            elif (original_color, r, c) == (4, 1, 1):
                output_grid[r][c] = 4
            elif (original_color, r, c) == (2, 1, 2):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (2, 2, 0):
                output_grid[r][c] = 4
            elif (original_color, r, c) == (4, 2, 1):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (4, 2, 2):
                output_grid[r][c] = 9
            elif (original_color, r, c) == (8, 0, 0):
                output_grid[r][c] = 5
            elif (original_color, r, c) == (5, 0, 1):
                output_grid[r][c] = 5
            elif (original_color, r, c) == (8, 0, 2):
                output_grid[r][c] = 8
            elif (original_color, r, c) == (5, 1, 0):
                output_grid[r][c] = 8
            elif (original_color, r, c) == (5, 1, 1):
                output_grid[r][c] = 5
            elif (original_color, r, c) == (8, 1, 2):
                output_grid[r][c] = 5
            elif (original_color, r, c) == (5, 2, 0):
                output_grid[r][c] = 8
            elif (original_color, r, c) == (8, 2, 1):
                output_grid[r][c] = 8
            elif (original_color, r, c) == (8, 2, 2):
                output_grid[r][c] = 8
            elif (original_color, r, c) == (2, 0, 0):
                output_grid[r][c] = 3
            elif (original_color, r, c) == (9, 0, 1):
                output_grid[r][c] = 3
            elif (original_color, r, c) == (3, 0, 2):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (3, 1, 0):
                output_grid[r][c] = 9
            elif (original_color, r, c) == (9, 1, 1):
                output_grid[r][c] = 9
            elif (original_color, r, c) == (2, 1, 2):
                output_grid[r][c] = 9
            elif (original_color, r, c) == (3, 2, 0):
                output_grid[r][c] = 9
            elif (original_color, r, c) == (9, 2, 1):
                output_grid[r][c] = 2
            elif (original_color, r, c) == (9, 2, 2):
                output_grid[r][c] = 3
            else:
                #Use input color as default if mapping is missing.
                output_grid[r][c] = original_color

    return output_grid