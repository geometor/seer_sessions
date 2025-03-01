"""
1.  **Identify the largest rectangle in the input grid.**
2.  **Change the color of this rectangle to green.**
3.  **Translate the rectangle one unit down and one unit to the right.**
4.  **All other objects in the input are removed.**
"""

import numpy as np

def find_largest_rectangle(grid):
    """Finds the largest rectangle in a grid."""
    max_area = 0
    max_rect = None
    rows, cols = grid.shape
    for r1 in range(rows):
        for c1 in range(cols):
            for r2 in range(r1, rows):
                for c2 in range(c1, cols):
                    if np.all(grid[r1:r2+1, c1:c2+1] == grid[r1, c1]):  # Check if it's a rectangle of a single color
                        area = (r2 - r1 + 1) * (c2 - c1 + 1)
                        if area > max_area:
                            max_area = area
                            max_rect = (r1, c1, r2, c2)
    return max_rect

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int) # Initialize with background color (0)

    # change output pixels
    # 1. Find the largest rectangle
    rectangle = find_largest_rectangle(input_grid)

    if rectangle:
        r1, c1, r2, c2 = rectangle

        # 2. & 3. Change the color and translate
        new_r1, new_c1 = r1 + 1, c1 + 1
        new_r2, new_c2 = r2 + 1, c2 + 1

        # Check bounds for new translated rectangle, and place it if within bounds
        if new_r2 < rows and new_c2 < cols:
          output_grid[new_r1:new_r2+1, new_c1:new_c2+1] = 3  # set to green (3)

    # 4. all other pixels are zero due to initialization
    return output_grid