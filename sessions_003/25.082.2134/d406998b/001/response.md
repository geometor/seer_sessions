```python
"""
The transformation rule is as follows:

1. Identify Objects: Recognize contiguous blocks of gray (5) pixels as distinct objects. These can be single pixels or groups of adjacent gray pixels.
2. Horizontal Selection: consider the horizontal and vertical components of the gray objects independently.
3. Horizontal Selection: for each horizontal gray block, begin on the left, consider this position "odd".
4. Horizontal Selection: Change the "odd" gray pixels to green.
5. Vertical Selection: for each vertical gray block, begin at the top, consider this position "even".
6. Vertical Selection: Change the "even" gray pixels to green.
7. Other Pixels: Leave all other pixels (those not gray) unchanged.
"""

import numpy as np

def get_objects(grid, color=5):
    # Find contiguous blocks of the specified color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects


def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Get gray (5) objects
    gray_objects = get_objects(output_grid, color=5)
    
    # apply horizontal and vertical selection
    for obj in gray_objects:
        # sort by x position (horizontal)
        horizontal = sorted(obj, key=lambda x: x[1])
        for i in range(len(horizontal)):
          if i%2==0: # odd
            r,c = horizontal[i]
            output_grid[r,c]=3
        # sort by y position (vertical)
        vertical = sorted(obj, key=lambda x: x[0])
        for i in range(len(vertical)):
          if i%2==1: # even
            r,c = vertical[i]
            output_grid[r,c]=3

    return output_grid
```