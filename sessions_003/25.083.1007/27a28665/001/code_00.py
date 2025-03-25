"""
1.  **Identify Objects:** The input is a 3x3 grid. Consider contiguous blocks of the *same* color as separate objects. Diagonally connected is considered contiguos, and a single non-zero cell is contiguous to itself.
2.  **Count Objects:** count how many discrete objects are present in the input.
3. **Output count:** output the single integer count of the objects.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    """
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))

        # Check all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_object)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r, c) not in visited and grid[r][c] != 0:
                current_object = []
                dfs(r, c, current_object)
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