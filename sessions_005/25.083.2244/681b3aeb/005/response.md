```python
"""
1.  **Identify Objects:** Find all contiguous blocks of non-zero pixels. Each block is an object.
2.  **Object Properties:** Determine the shape and color of each object.
3.  **Tiling:** The transformation involves arranging the objects in a tiled manner to create the output grid. Objects are arranged without overlapping, like puzzle pieces. The target grid dimension is 3x3 for all training examples.
4. Determine the object that goes on the top left: The object with most number of pixels gets placed on the top-left of the grid.
5. Place remaining objects: For each remaining object, iterate over their pixels, and fill them to the output grid at the corresponding indexes. If the index does not exist, extend the output grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous blocks of non-zero pixels as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(obj_pixels)
    return objects

def get_object_shape(grid, obj_pixels):
    rows, cols = zip(*obj_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    shape = []
    for r in range(min_row, max_row + 1):
        row_shape = []
        for c in range(min_col, max_col + 1):
            if (r, c) in obj_pixels:
                row_shape.append(grid[r,c])
            else:
                row_shape.append(0)
        shape.append(row_shape)

    return np.array(shape)

def transform(input_grid):
    # Find objects
    objects = find_objects(input_grid)

    # Group objects by shape and color
    patterns = {}
    for obj_pixels in objects:
        shape = get_object_shape(input_grid, obj_pixels).tolist()
        color = input_grid[obj_pixels[0]]
        key = (tuple(map(tuple, shape)), color)  # Convert shape to tuple of tuples
        if key not in patterns:
            patterns[key] = []
        patterns[key].append(obj_pixels)

    # Sort the objects, such the largest object comes first
    sorted_patterns = sorted(patterns.items(), key=lambda item: (len(item[1]), -len(item[0][0])), reverse=True )

    # initialize the output grid with the first pattern
    (shape, color), _ = sorted_patterns[0]
    output_grid = np.array(shape)

    # iterate through the rest of the patterns to tile
    for (shape, color), _ in sorted_patterns[1:]:
        pattern = np.array(shape)
        rows, cols = pattern.shape

        # Create a new grid that can accommodate both.
        new_rows = max(output_grid.shape[0], rows)
        new_cols = max(output_grid.shape[1], cols)
        new_grid = np.zeros((new_rows, new_cols), dtype=int)

        # Copy the existing output grid
        for r in range(output_grid.shape[0]):
          for c in range(output_grid.shape[1]):
            new_grid[r,c] = output_grid[r,c]

        # Add new shape
        for r in range(rows):
            for c in range(cols):
                if pattern[r,c] != 0:
                  new_grid[r,c] = pattern[r,c]
        output_grid = new_grid

    return output_grid
```