# 6b9890af • 004 • refine_coder

---
```python
"""
1.  **Identify Objects:** Examine the input grid and identify all distinct, contiguous colored regions (objects). Do not include white (0) pixels as separate objects.
2. **Identify Internal Objects:** Identify objects inside the grid.
3.  **Draw Bounding Box:** Calculate the minimum bounding box that encloses all the internal objects.
4. **Create Red Border:** Create an output grid equal to the size of the bounding box. Fill this rectangle's outline with red color (2).
5. **Copy internal colors**: Transfer the internal objects into the output grid within the red border, maintaining original relative positions.
"""

import numpy as np

def find_objects(grid):
    """Finds distinct colored objects in the grid."""
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
            if not visited[row, col] and grid[row, col] != 0:
                object_pixels = []
                dfs(row, col, grid[row, col], object_pixels)
                objects.append(
                    {"color": grid[row, col], "pixels": object_pixels}
                )
    return objects

def create_bounding_box(objects):
    """Creates a bounding box around all objects."""
    if not objects:
        return None, None, None, None

    all_pixels = []
    for obj in objects:
        all_pixels.extend(obj["pixels"])

    min_row = min(pixel[0] for pixel in all_pixels)
    max_row = max(pixel[0] for pixel in all_pixels)
    min_col = min(pixel[1] for pixel in all_pixels)
    max_col = max(pixel[1] for pixel in all_pixels)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find distinct objects
    objects = find_objects(input_grid)

    # Define bounding box
    min_row, max_row, min_col, max_col = create_bounding_box(objects)
    
    if min_row is None:
        return np.array([[0]]) # Return a default 1x1 grid if no objects are found

    # Create output grid based on bounding box dimensions
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_grid = np.zeros((height, width), dtype=int)

    # Create red border
    for row in range(height):
        for col in range(width):
            if row == 0 or row == height - 1 or col == 0 or col == width - 1:
                output_grid[row, col] = 2

    # Transfer internal object pixels
    for obj in objects:
        for row, col in obj["pixels"]:
            new_row = row - min_row
            new_col = col - min_col
            # Ensure pixels are within the border
            if 0 < new_row < height - 1 and 0 < new_col < width - 1:
                output_grid[new_row, new_col] = obj["color"]
    return output_grid
```
