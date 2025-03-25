"""
1.  **Object Identification:** Identify all distinct objects in the input grid. An object is a contiguous group of pixels of the same non-zero color.

2.  **Bounding Box:** Determine the bounding box for each object.

3. **Output Grid**: Create a 3x3 output grid.

4.  **Relative Positioning and Wrapping:** For each object in the input, map its pixels to the output grid, maintaining relative positions and shape from input.
  Calculate an offset for each object based on the bounding box, and map to the corresponding cell in the output grid.
      The relative positions are defined as `output_row = input_row % 3` and `output_col = input_col % 3`.

5. **Populate Output Grid:** Apply this mapping to place each object from the input to the output grid, retaining each object's shape and color. If multiple objects map to the same output cell, the last object mapped overwrites previous ones.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                objects.append({
                    'color': grid[r, c],
                    'coords': obj_coords
                })
    return objects

def transform(input_grid):
    # Initialize a 3x3 output grid with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Iterate through each object and its coordinates
    for obj in objects:
        for row, col in obj['coords']:
            # Calculate the corresponding output row and column using modulo 3
            output_row = row % 3
            output_col = col % 3
            # Set the output grid cell to the object's color
            output_grid[output_row, output_col] = obj['color']

    return output_grid