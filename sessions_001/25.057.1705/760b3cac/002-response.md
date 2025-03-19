# 760b3cac • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all contiguous blocks of pixels of the same color. These are the objects.
2.  **Preserve Yellow:** The yellow (4) object remains unchanged between the input and output.
3.  **Copy Azure:** The original azure objects are copied from the input.
4. **Extend the Azure objects** For each column that contains azure (8) pixels, add azure colored pixels above the original azure area, filling to the top edge of the grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects of the same color in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if object_pixels:
                    objects.append({"color": color, "pixels": object_pixels})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)
    
    # Identify azure objects
    azure_objects = [obj for obj in objects if obj['color'] == 8]

    # Extend azure objects upwards
    for obj in azure_objects:
        columns = set([pixel[1] for pixel in obj['pixels']])
        for col in columns:
            #find top most pixel
            top_row = min([pixel[0] for pixel in obj['pixels'] if pixel[1] == col])
            for row in range(top_row):
                output_grid[row,col] = 8

    return output_grid
```
