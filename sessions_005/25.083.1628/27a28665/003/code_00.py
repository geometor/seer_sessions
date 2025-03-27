"""
The transformation identifies a specific checkerboard-like pattern in the input 3x3 grid. The input grid always consists of two colors: 0 and a non-zero color. The non-zero color is the "dominant" color, appearing five times.

1.  **Identify the Dominant Color:** Find the color that appears five times in the grid (the "dominant color").
2.  **Determine Output Based on Dominant Color:**
    *   If the dominant color occupies the center, and forms a checkerboard, then
        *   If the dominant color is 8 or 5, the output is 2.
    *   If the dominant color is 1 or 8, and if the top left cell is 0, the output is 3.
    *   If the dominant color is 4 or 5, and forms a "L" shape then output is 1.
    *  If the dominant color is 5, and it touches all borders, but the corners are zero, the output is 6
"""

import numpy as np
from scipy.ndimage import label

def get_dominant_color(grid):
    """Finds the color that appears five times (dominant color)."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    for color, count in zip(unique_colors, counts):
        if count == 5:
            return color
    return None  # Should not happen given the problem constraints

def transform(input_grid):
    """Transforms the input grid based on the dominant color and pattern."""
    grid = np.array(input_grid)
    dominant_color = get_dominant_color(grid)

    # Check for perfect checkerboard pattern (dominant color in center and corners)
    if grid[1, 1] == dominant_color and grid[0, 0] == dominant_color and grid[0, 2] == dominant_color and grid[2, 0] == dominant_color and grid[2, 2] == dominant_color:
        if dominant_color in (8, 5):
            return 2

    # Check for L shape or corner shape pattern where top-left is 0
    if grid[0,0] == 0 and grid[1,1] == dominant_color:
        if dominant_color in (1, 8) :
            return 3

    if grid[1,1] == dominant_color:
        if dominant_color in (4,5):
            return 1

    # Check for 5 touching all sides except corners
    labeled_grid, num_objects = label(grid)

    if dominant_color == 5:
        if np.all(grid[0, 1] == 5) and \
        np.all(grid[1, 0] == 5) and \
        np.all(grid[1, 2] == 5) and \
        np.all(grid[2, 1] == 5) and \
        np.all(grid[0,0] == 0) and np.all(grid[0,2] == 0) and np.all(grid[2,0] == 0) and np.all(grid[2,2] == 0):
            return 6

    return 0 # Default return. Should ideally never reach here based on observed patterns