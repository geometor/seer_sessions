# 36fdfd69 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Red Corners:** Scan the input grid and locate all "corners" formed by red (2) pixels. A corner exists where two red pixels are diagonally adjacent.
2.  **Overlay Yellow:** For each red corner, place a yellow (4) pixel at the location of the diagonal intersection of the two red pixels forming the corner.
3.  **Preserve Other Pixels:** All other pixels (green and black) from the input grid remain unchanged in the output grid.
"""

import numpy as np

def find_red_corners(grid):
    """Finds diagonally adjacent red pixels."""
    red_corners = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 2:
                # Check for diagonal neighbors
                if r + 1 < grid.shape[0] and c + 1 < grid.shape[1] and grid[r + 1, c + 1] == 2:
                    red_corners.append(((r, c), (r + 1, c + 1)))
                if r - 1 >= 0 and c + 1 < grid.shape[1] and grid[r - 1, c + 1] == 2:
                    red_corners.append(((r, c), (r - 1, c + 1)))
                if r + 1 < grid.shape[0] and c - 1 >= 0 and grid[r + 1, c - 1] == 2:
                    red_corners.append(((r, c), (r + 1, c - 1)))
                if r - 1 >= 0 and c - 1 >= 0 and grid[r - 1, c - 1] == 2:
                    red_corners.append(((r, c), (r - 1, c - 1)))
    return red_corners

def get_intersection(corner_pair):
    """Calculates the intersection point of a diagonal corner pair."""
    (r1, c1), (r2, c2) = corner_pair
    # Determine the intersection based on relative positions
    if r1 < r2 and c1 < c2:
       return (r1+1,c1)
    if r1 > r2 and c1 < c2:
        return (r1-1, c1)
    if r1 < r2 and c1 > c2:
        return (r1+1,c1)
    if r1 > r2 and c1 > c2:
        return (r1-1, c1)

    return None

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)  # Initialize with the input grid
    red_corners = find_red_corners(input_grid)
    intersections = []
    for pair in red_corners:
       intersections.append(get_intersection(pair))
    # remove duplicates
    intersections = list(set(intersections))
    for x in intersections:
       if x:
          output_grid[x] = 4

    return output_grid
```
