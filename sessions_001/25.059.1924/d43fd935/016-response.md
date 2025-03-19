# d43fd935 • 016 • refine_coder

---
```python
"""
1.  **Copy Green:** The 2x2 block of green (3) pixels is copied directly from the input to the output grid, maintaining its position.

2.  **Mirror Orange:** The object formed by orange (7) pixels is mirrored across the main diagonal (y=x). This means the pixel at (r, c) in the input becomes the pixel at (c, r) in the output.

3.  **Mirror Azure:** The object formed by azure (8) pixels is mirrored vertically. The vertical line of reflection is the center of the azure object. The reflection *only* fills cells that are *not* occupied by an azure (8) pixel in the *input* grid. If the reflected azure pixel would overlap with any other existing object, the other object takes priority, including the mirrored orange object.
"""

import numpy as np

def get_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Copy green blocks (color 3)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 3:
                output_grid[r,c] = 3

    # Mirror orange (color 7)
    orange_objects = get_objects(input_grid, 7)
    for obj in orange_objects:
        for r, c in obj:
            output_grid[c, r] = 7

    # Mirror azure (color 8)
    azure_objects = get_objects(input_grid, 8)
    for obj in azure_objects:
        # Find the center of the object for mirroring
        coords = np.array(obj)
        min_c = np.min(coords[:, 1])
        max_c = np.max(coords[:, 1])
        center_c = (min_c + max_c) / 2

        for r, c in obj:
            # reflect across the center axis
            mirrored_c = int(2 * center_c - c)
            if 0 <= mirrored_c < cols:
                # Crucial change: Check the *input* grid for existing azure
                if input_grid[r, mirrored_c] != 8:
                    # if the cell is not 8 in input, fill, but orange takes precedence if there
                    if output_grid[r, mirrored_c] == 0:
                        output_grid[r, mirrored_c] = 8

    return output_grid
```

