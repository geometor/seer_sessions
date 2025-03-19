# 681b3aeb • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Colored Regions:** Scan the input grid and identify contiguous regions of non-white (non-zero) pixels.  Consider each such region as a separate object.
2.  **Discard Background:** Ignore the white (0) pixels, treating them as background.
3.  **Extract Colors:** For each identified colored region, record its color value.
4. **Determine layout**: Record the top, left, bottom, and right most position of each non-zero color.
5.  **Construct Output:** Create a 3x3 output grid. Place the identified colors into the output grid, maintaining their relative positioning from the compressed bounding box formed in step 4. If multiple colors occupy the same relative space, arrange them as they are arranged in the input.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        """Depth-first search to find connected components."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                objects.append({
                    'color': grid[row, col],
                    'coords': obj_coords
                })
    return objects

def get_bounding_box(objects):
    """Calculates the bounding box encompassing all objects."""
    if not objects:
        return (0,0,0,0)

    min_row = min(min(coord[0] for coord in obj['coords']) for obj in objects)
    max_row = max(max(coord[0] for coord in obj['coords']) for obj in objects)
    min_col = min(min(coord[1] for coord in obj['coords']) for obj in objects)
    max_col = max(max(coord[1] for coord in obj['coords']) for obj in objects)

    return min_row, min_col, max_row, max_col


def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Find objects (contiguous non-zero regions)
    objects = find_objects(input_grid)

    # compute the bounding box
    min_row, min_col, max_row, max_col = get_bounding_box(objects)
    bounding_box_height = max_row - min_row + 1
    bounding_box_width = max_col - min_col + 1

    # Initialize output grid (3x3)
    output_grid = np.zeros((3, 3), dtype=int)

    # Place objects into output grid based on relative position
    for obj in objects:
      first = True
      for row, col in obj['coords']:
        # scale to the bounding box size, then quantize to 3x3
        rel_row = row - min_row
        rel_col = col - min_col

        y = int(rel_row * 3 / bounding_box_height)
        x = int(rel_col * 3 / bounding_box_width)

        if first:
            output_grid[y,x] = obj['color']
            prev_y, prev_x = y, x
            first = False
        # handle overlaps by preserving input grid layout.
        else:
            output_grid[y, x] = obj['color']
            dy, dx = y - prev_y, x-prev_x
            if dy != 0 and dx != 0 and output_grid[prev_y+dy, prev_x] == 0:
                output_grid[prev_y+dy, prev_x] = obj['color']
            elif dy != 0 and dx != 0 and output_grid[prev_y, prev_x+dx] == 0:
                output_grid[prev_y, prev_x + dx] = obj['color']


    return output_grid
```
