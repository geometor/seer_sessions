```python
"""
1.  **Initialization:** Start with a count of 0.  Create an empty "visited" set to track pixels that have been processed.
2.  **Iterate:** Loop through each pixel in the input grid.
3.  **Check Visited and Zero:** For the current pixel:
    *   If the pixel has already been visited, skip to the next pixel.
    *   If the pixel's value is 0 (white/background), skip to the next pixel.
4.  **Object Found:** If the pixel is not visited and not zero, increment the object count.
5.  **Depth-First Search (DFS):** Perform a DFS starting from the current pixel:
    *   Mark the current pixel as visited.
    *   Recursively visit all 8-connected neighbors (up, down, left, right, and diagonals).
    *   During the DFS, *only* visit neighbors that have the *same* color as the starting pixel and have not been visited.
6.  **Continue Iteration:** After the DFS completes (meaning one entire connected object has been explored), continue the outer loop iteration from step 2.
7.  **Output:** After iterating through all pixels, output the final object count. This count represents the number of distinct, non-zero, connected regions in the grid.
"""

import numpy as np

def count_distinct_objects(grid):
    """Counts distinct objects in the grid."""
    visited = set()
    count = 0

    def is_valid(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def dfs(r, c, color):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, color)


    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if (r,c) not in visited and grid[r,c]!=0:
                count += 1
                dfs(r,c, grid[r,c])
    return count

def transform(input_grid):
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # Count distinct objects using the helper function
    object_count = count_distinct_objects(grid)

    return object_count
```