"""
1.  **Identify Green Crosses:** Find all green pixels that are part of both a horizontal and a vertical line, forming a "cross" shape. These are the intersection points.
2.  **Locate Gray Marker:** Find the single gray pixel.
3.  **Conditional Removal:** If a gray pixel is directly adjacent (up, down, left or right) to a green cross intersection, remove the green pixel at the intersection point.
4.   **Output:** The resulting grid after applying the removal rule.
"""

import numpy as np

def find_green_crosses(grid):
    rows, cols = grid.shape
    crosses = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                # Check for horizontal and vertical neighbors
                horizontal = (c > 0 and grid[r, c-1] == 3) or (c < cols-1 and grid[r, c+1] == 3)
                vertical = (r > 0 and grid[r-1, c] == 3) or (r < rows-1 and grid[r+1, c] == 3)
                if horizontal and vertical:
                    crosses.append((r, c))
    return crosses

def find_gray_pixel(grid):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 5:
                return (r, c)
    return None

def is_adjacent(coord1, coord2):
    r1, c1 = coord1
    r2, c2 = coord2
    return (abs(r1 - r2) == 1 and c1 == c2) or (abs(c1 - c2) == 1 and r1 == r2)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find green crosses
    green_crosses = find_green_crosses(output_grid)

    # Find gray pixel
    gray_pixel = find_gray_pixel(output_grid)

    # Conditional removal
    if gray_pixel:
        for cross_r, cross_c in green_crosses:
            if is_adjacent((cross_r, cross_c), gray_pixel):
                output_grid[cross_r, cross_c] = 0

    return output_grid