```python
"""
1.  **Initialization:**
    *   Set a counter `count` to 0.
    *   Create an empty set `visited` to store the coordinates of pixels that have been processed.

2.  **Iteration:**
    *   Loop through each pixel in the input grid. Let the current pixel's row be `r` and column be `c`.

3.  **Check and Skip:**
    *   If the pixel at `(r, c)` is in the `visited` set, skip to the next pixel.
    *   If the color of the pixel at `(r, c)` is 0 (background), skip to the next pixel.

4.  **Object Detection and Counting:**
    *   If the pixel at `(r, c)` is not in `visited` and its color is not 0, increment the `count`.

5.  **4-Connected Depth-First Search (DFS):**
    *   Start a DFS from the current pixel `(r, c)`:
        *   Add `(r, c)` to the `visited` set.
        *   Recursively visit the 4 neighbors (up, down, left, right) of the current pixel.
        *   For each neighbor `(nr, nc)`:
            *   If `(nr, nc)` is within the grid boundaries,
            *   and `(nr, nc)` is not in the `visited` set,
            *   and the color of the pixel at `(nr, nc)` is the same as the color of the initial pixel at `(r, c)`,
            *   then recursively call DFS on `(nr, nc)`.

6.  **Output:** After iterating through all pixels, the value of `count` represents the total number of distinct objects (4-connected regions of non-zero color) in the input grid. Return `count`.
"""

import numpy as np

def transform(input_grid):
    grid = np.array(input_grid)
    visited = set()
    count = 0

    def is_valid(r, c):
        return 0 <= r < len(grid) and 0 <= c < len(grid[0])

    def dfs(r, c, color):
        # Add current pixel to visited set
        visited.add((r, c))

        # Define 4-connected neighbors (up, down, left, right)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

        for nr, nc in neighbors:
            if (is_valid(nr, nc) and
                (nr, nc) not in visited and
                grid[nr, nc] == color):
                dfs(nr, nc, color)

    # Iterate through each pixel in the grid
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            # If pixel is not visited and is not background (0)
            if (r, c) not in visited and grid[r, c] != 0:
                # Increment count and start DFS
                count += 1
                dfs(r, c, grid[r, c])

    return count
```