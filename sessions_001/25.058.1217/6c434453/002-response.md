# 6c434453 • 002 • example_2 • investigate_coder

---
```python
"""
Iterates through each pixel of the input grid. Identifies blue (1) pixels.
Analyzes the neighborhood of each blue pixel:  If a blue pixel is part of a 3x3 cross (plus sign shape),
and the 'corner' of any adjacent cross shares the center, change the blue cross to a red cross.
Outputs the modified grid.
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
    Checks if two crosses share any corner.

    """

    x1, y1 = center1
    x2, y2 = center2

    #check condition for if corners are shared
    if abs(x1-x2) == 1 and abs(y1 - y2) == 1:
        return True

    return False

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find all blue crosses
    blue_cross_centers = find_crosses(input_grid)

    # Create a set of centers to be replaced
    centers_to_replace = set()

    # Check for neighboring crosses and mark for replacement
    for center1 in blue_cross_centers:
        for center2 in blue_cross_centers:
            if center1 != center2 and is_corner_shared(center1,center2) :
                centers_to_replace.add(center1)

    # Perform the replacement of the center and four arms
    for r, c in centers_to_replace:
        output_grid[r, c] = 2
        output_grid[r-1, c] = 2
        output_grid[r+1, c] = 2
        output_grid[r, c-1] = 2
        output_grid[r, c+1] = 2

    return output_grid
```
