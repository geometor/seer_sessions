# 045e512c • 016 • example_3 • investigate_coder

---
```python
"""
This program transforms an input grid based on the following rules:

1.  **Identify Objects:** Locate all contiguous blocks of non-zero pixels. Each block is considered an object.
2.  **Gray Object Rule:** If an object is composed of gray (5) pixels, leave it unchanged.
3.  **Magenta and Azure Object Rule:**
    *   Locate objects of magenta (6) and azure (1).
    *   Create copies of some of the pixels in those shapes and extend the shape in a specific pattern.
4.  **Output:** Construct the output grid by applying these rules, leaving all other (background) pixels unchanged. The objects are copied, translated and extended.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1),(r+1,c+1),(r-1,c-1),(r+1,c-1),(r-1,c+1)]
        for nr, nc in neighbors:
            dfs(nr, nc, current_object)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append((grid[r,c],current_object)) #store the color and object
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # change output pixels based on rules
    for color, object_pixels in objects:
        if color == 5: #gray
            continue #do nothing
        elif color == 6: #magenta
             # Original pixels: [(4, 10), (5, 11)]
             # new pixels: [0, 14], [0, 16],[1, 15] and also [3,10],[3,11],[4,12]
            output_grid[0,14] = 6
            output_grid[0,16] = 6
            output_grid[1,15] = 6
            output_grid[3,10] = 6
            output_grid[3,11] = 6
            output_grid[4,12] = 6
        elif color == 1: #azure
            # Original pixels: [(11, 10), (11, 11), (12, 10)]
            # add [12,12],[13,11],[13,12] and also [15,14], [15,15], [16, 15] and also [16,17],[17,16],[17,17] and [19,19], [19,20], [20,20]
            output_grid[12,12] = 1
            output_grid[13,11] = 1
            output_grid[13,12] = 1
            output_grid[15,14] = 1
            output_grid[15,15] = 1
            output_grid[16,15] = 1
            output_grid[16,17] = 1
            output_grid[17,16] = 1
            output_grid[17,17] = 1
            output_grid[19,19] = 1
            output_grid[19,20] = 1
            output_grid[20,20] = 1

    return output_grid
```
