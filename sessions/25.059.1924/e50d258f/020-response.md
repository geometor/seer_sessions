# e50d258f • 020 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions (objects) of non-black (non-zero) pixels in the input grid.  A contiguous region is defined as a group of pixels of the same color that are connected horizontally, vertically, or diagonally.
2.  **Determine Bounding Box:** For the object found, identify the smallest rectangle (bounding box) that completely encloses the object. This is done by finding the minimum and maximum row and column indices of all pixels belonging to the object.
3.  **Crop:** Extract the rectangular region defined by the bounding box from the input grid. This cropped region is the output. If no objects are found the result will be an empty array.
"""

import numpy as np

def find_objects(grid):
    # Find all contiguous regions of non-black pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return []

        visited[r, c] = True
        region = [(r, c)]

        # Explore adjacent cells (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                region.extend(dfs(r + dr, c + dc, color))

        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                region = dfs(r, c, color)
                if region:
                    objects.append(region)

    return objects

def get_bounding_box(object_pixels):
    # Get bounding box of a set of pixels
    min_row = min(p[0] for p in object_pixels)
    max_row = max(p[0] for p in object_pixels)
    min_col = min(p[1] for p in object_pixels)
    max_col = max(p[1] for p in object_pixels)
    return (min_row, min_col), (max_row, max_col)

def crop_grid(grid, top_left, bottom_right):
    # Crop the grid based on top_left, bottom_right
    return grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1]

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    # Handle no objects case
    if not objects:
        return np.array([]).tolist() #return empty if no objects found.

    # Get combined object pixels
    combined_pixels = []
    for obj in objects:
      combined_pixels.extend(obj)

    # Determine bounding box
    top_left, bottom_right = get_bounding_box(combined_pixels)

    # Crop the grid
    cropped_grid = crop_grid(input_grid, top_left, bottom_right)

    return cropped_grid.tolist()
```
