# 6e82a1ae • 020 • refine_coder

---
```python
"""
1.  **Identify Connected Gray Objects:** Find all distinct connected regions of gray (color 5) pixels in the input grid. Consider pixels to be connected if they are adjacent horizontally, vertically, or diagonally (8-way connectivity).

2.  **Assign Colors Cyclically:** Assign a unique color to each identified gray object. Cycle through the colors blue (1), green (3), and red (2) in that order. The first object gets blue, the second green, the third red, the fourth blue, and so on.

3.  **Transform Gray Pixels:** For each gray object, replace all its pixels' color with the assigned color.

4. **Preserve Other Colors** Pixels that are not gray (color 5) in the original input should retain their color. In particular, white (color 0) and azure (color 8) should be unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds all distinct connected components of a given color in the grid using 8-way connectivity.
    Returns a list of sets, where each set contains the coordinates of a connected component.
    """
    visited = set()
    objects = []

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.add((r, c))
        # 8-way connectivity (including diagonals)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)
        dfs(r + 1, c + 1, current_object)
        dfs(r + 1, c - 1, current_object)
        dfs(r - 1, c + 1, current_object)
        dfs(r - 1, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = set()
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by replacing each connected gray object with a unique color, cycling through blue, green and red.
    Preserves non-gray colors.
    """
    output_grid = np.copy(input_grid)
    gray_objects = find_objects(input_grid, 5)  # Find all gray objects using 8-way connectivity

    # Define a color mapping for the objects - cyclical
    color_map = {
        0: 1,  # First object: blue
        1: 3,  # Second object: green
        2: 2,  # Third object: red
    }

    # Replace gray pixels with the corresponding color for each object
    for i, obj in enumerate(gray_objects):
        color_index = i % len(color_map)  # cycle through the colors: blue, green, red
        for r, c in obj:
            output_grid[r, c] = color_map[color_index]

    return output_grid
```
