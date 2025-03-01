"""
1.  **Identify Objects:** Find all blue "cross" shaped objects in the input grid. A cross is defined as a 3x3 block of pixels where the center pixel and its four immediate neighbors (up, down, left, right) are blue (value 1), and the corner pixels of this 3x3 area can be any color.

2.  **Check Condition:** Iterate through each pair of identified blue crosses. For each pair, determine if they "share a corner". Two crosses share a corner if the centers of two crosses are diagonally adjacent, meaning that the absolute difference of their x coordinates is 1 and the absolute difference of their y coordinates is also 1.

3.  **Transform:** If and only if two blue crosses share a corner, replace *both* of the blue crosses with red crosses. A cross is replaced by changing the color of its center pixel and its four arm pixels to red (value 2).
4. **Otherwise:** Keep the original input grid.
"""

import numpy as np

def find_crosses(grid):
    """
    Identifies centers of 3x3 crosses (plus signs) of a specific color in the grid.
    """
    cross_centers = []
    rows, cols = grid.shape
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if (grid[r, c] == 1 and
                grid[r-1, c] == 1 and
                grid[r+1, c] == 1 and
                grid[r, c-1] == 1 and
                grid[r, c+1] == 1):
                cross_centers.append((r, c))
    return cross_centers

def is_corner_shared(center1, center2):
    """
    Checks if two crosses share a corner (centers are diagonally adjacent).
    """
    x1, y1 = center1
    x2, y2 = center2
    return abs(x1 - x2) == 1 and abs(y1 - y2) == 1

def transform(input_grid):
    """
    Transforms the input grid by replacing corner-sharing blue crosses with red crosses.
    """
    output_grid = np.copy(input_grid)

    # Find all blue crosses
    blue_cross_centers = find_crosses(input_grid)

    # Create a set of centers to be replaced
    centers_to_replace = set()

    # Check for corner-sharing crosses and mark them for replacement
    for i, center1 in enumerate(blue_cross_centers):
        for j, center2 in enumerate(blue_cross_centers):
            if i != j and is_corner_shared(center1, center2):
                centers_to_replace.add(center1)
                centers_to_replace.add(center2)

    # Perform the replacement
    for r, c in centers_to_replace:
        output_grid[r, c] = 2
        output_grid[r-1, c] = 2
        output_grid[r+1, c] = 2
        output_grid[r, c-1] = 2
        output_grid[r, c+1] = 2

    return output_grid