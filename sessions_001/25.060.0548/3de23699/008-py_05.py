"""
1.  **Identify Corner Markers:** Locate the four yellow pixels (color 4) in the input grid. These pixels act as corner markers, defining the vertices of a conceptual rectangle.

2.  **Define Conceptual Rectangle:** Determine the full extent of the rectangle implied by the four yellow corner markers.  This rectangle's sides will be parallel to the grid axes. The rectangle extends to the furthest row and column occupied by ANY of the yellow pixels, effectively forming the rectangle defined *by* those corners, not just *containing* them.

3. **Extract Subgrid**: Obtain the data inside the rectangle described in Step 2.

4.  **Replace Colors:** Within the extracted subgrid, change all pixels that are *not* yellow (color 4) to white (color 0).  Keep the yellow pixels unchanged.

5.  **Output:** The resulting subgrid, with color replacements, is the output.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def bounding_box(points):
    """Computes the bounding box of a set of points."""
    min_row = np.min(points[:, 0])
    max_row = np.max(points[:, 0])
    min_col = np.min(points[:, 1])
    max_col = np.max(points[:, 1])
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Find yellow pixels (color 4).
    yellow_pixels = find_pixels_by_color(input_grid, 4)

    # Determine the bounding box.
    (min_row, min_col), (max_row, max_col) = bounding_box(yellow_pixels)
    
    # Initialize output grid based on bounding box size
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = np.zeros((height, width), dtype=int)

    # Crop and translate, while changing color
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if input_grid[r,c] == 4:
                output_grid[r-min_row, c-min_col] = 4
            else:
                output_grid[r-min_row, c-min_col] = 0 # set to white


    return output_grid