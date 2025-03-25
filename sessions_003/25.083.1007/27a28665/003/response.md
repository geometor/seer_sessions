```python
"""
1.  **Identify Pixels:** Examine each pixel in the input grid.
2.  **Define Objects:**  An object is defined as a group of one or more connected pixels of the *same* color.
    *   Pixels are considered connected if they are adjacent horizontally, vertically, or diagonally.
    *   Pixels of different colors are *never* considered part of the same object, even if adjacent.
    *   Two groups of pixels with the same color that are *not* connected are considered separate objects.
3.  **Count Objects:** Count the number of distinct objects in the grid, following the definition above.
4.  **Output Count:** Output the integer count representing the total number of objects found.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    """
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def dfs(r, c, current_object, color):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))

        # Check all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_object, color)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in visited and grid[r][c] != 0:
                current_object = []
                color = grid[r][c]
                dfs(r, c, current_object, color)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # Find objects
    objects = find_objects(grid)
    
    # Count how many objects
    count = len(objects)

    # Return the count
    return count
```