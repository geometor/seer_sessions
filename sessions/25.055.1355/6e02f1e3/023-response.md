# 6e02f1e3 • 023 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous blocks of the same color in the input grid.
2.  **Find Smallest Green Object:** among all the identified objects, locate the smallest green color object. Size is determined by the total number of cells/pixels in the object.
3. **Color Smallest:** If a smallest object is not found, find the largest green object. Change all pixels in the smallest/largest green object to gray.
4.  **Fill remaining:** Replace all other colors other than gray color to black.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, object_pixels):
        """Depth-first search to find contiguous pixels of the same color."""
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
    """Transforms the input grid according to the defined rules."""
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all objects in the input grid.
    objects = find_objects(input_grid)
    
    # Find the smallest green object.
    green_objects = [obj for obj in objects if obj["color"] == 3]
    smallest_green_object = None
    if green_objects:
        smallest_green_object = min(green_objects, key=lambda obj: len(obj["pixels"]), default=None)

    # If no smallest green object, find the largest
    if smallest_green_object is None and green_objects:
        largest_green_object = max(green_objects, key=lambda obj: len(obj["pixels"]))
        smallest_green_object = largest_green_object # Rename for consistency


    # Apply transformation rules
    for obj in objects:
      if obj is smallest_green_object:
          for row, col in obj["pixels"]:
            output_grid[row,col] = 5
      else:
          for row, col in obj["pixels"]:
            if output_grid[row,col] != 5: #prevent overwrite
              output_grid[row, col] = 0

    return output_grid
```
