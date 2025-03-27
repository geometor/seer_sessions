"""
1.  **Identify Objects:** Scan the input grid to identify distinct objects. An object is a contiguous block of pixels with the same non-zero color.
2.  **Identify Patterns:** Group objects with the same shape and colors.
3.  **Combine patterns:** Combine patterns to form the output image.
    The patterns seem to get combined in such a way to form a consistent grid. The largest dimensions of a pattern dictates overall size along one dimension. The other patterns fill in.
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

    # Combine patterns to create output grid
    combined_pattern = []

    sorted_patterns = sorted(patterns.items(), key=lambda item: (len(item[1]), -len(item[0][0])), reverse=True )


    for (shape, color), _ in sorted_patterns: #key is (shape,color)
      combined_pattern.append(np.array(shape))

    #find the biggest dimension
    max_rows = 0
    max_cols = 0

    for pattern in combined_pattern:
      if pattern.shape[0] > max_rows:
        max_rows = pattern.shape[0]
      if pattern.shape[1] > max_cols:
          max_cols = pattern.shape[1]

    output_grid = np.zeros((max_rows,max_cols),dtype=int)

    for pattern_part in combined_pattern:
      rows, cols = pattern_part.shape

      for r in range(rows):
          for c in range(cols):
              if pattern_part[r,c] !=0:
                output_grid[r,c] = pattern_part[r,c]


    return output_grid