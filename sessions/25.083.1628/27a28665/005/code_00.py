"""
1.  **Identify the Dominant Color:** Determine the color that appears exactly five times within the 3x3 input grid.

2.  **Apply Transformation Rules Based on Dominant Color and Pattern:**

    *   **Rule 1 (Checkerboard):** If the dominant color occupies the center cell AND all four corner cells, then:
        *   If the dominant color is 8 or 5, the output is 2.

    *   **Rule 2 (Corner Shape with 0):** If the top-left cell is 0, and the dominant color is 1 or 8, then the output is 3.

    *   **Rule 3 (5 Touching Borders):** If the dominant color is 5, AND the dominant color occupies all border cells *except* the corners (all corners are 0), the output is 6.

    * **Rule 4 (Center not dominant):** If the center pixel is not the dominant color the output is 1.

    *   **Rule 5 (Default):** In all other cases, there appears to be no consistent rule. Return 0.  (This needs further investigation with more examples, but it's the best we can do for now).
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

    # Rule 1: Checkerboard
    if grid[1, 1] == dominant_color and grid[0, 0] == dominant_color and grid[0, 2] == dominant_color and grid[2, 0] == dominant_color and grid[2, 2] == dominant_color:
        if dominant_color in (8, 5):
            return 2

    # Rule 2: Corner Shape with 0
    if grid[0, 0] == 0 and dominant_color in (1, 8):
        return 3

    # Rule 3: 5 Touching Borders
    if dominant_color == 5:
        if np.all(grid[0, 1] == 5) and \
           np.all(grid[1, 0] == 5) and \
           np.all(grid[1, 2] == 5) and \
           np.all(grid[2, 1] == 5) and \
           np.all(grid[0, 0] == 0) and np.all(grid[0, 2] == 0) and np.all(grid[2, 0] == 0) and np.all(grid[2, 2] == 0):
            return 6

    # Rule 4: If center is not the dominant color
    if grid[1,1] != dominant_color:
        return 1
    
    # Rule 5: Default
    return 0