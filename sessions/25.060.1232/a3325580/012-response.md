# a3325580 • 012 • refine_coder

---
```python
"""
1. Identify Valid Objects: Examine the input grid. Identify contiguous regions (objects) of the same color. An object is considered "valid" if all of the following apply:
    *   It has the shape of a "3x3 block missing corners".
    *   It does not only touch background pixels (color 0).
    *   It does not contain any pixels on an edge.
2. Determine Output Dimensions: Count the number of *valid* colored objects identified in step 1. The output grid will have a height of 5 and a width equal to this count. If no valid colors are found, the output grid is 5x0.
3. Construct Output Grid: Create an output grid with the dimensions determined in step 2.
4. Populate Output Grid: For each *valid* color, create a column in the output grid. Fill the entire column (all 5 rows) with that color. The order of the columns should correspond to the order in which the valid objects were identified.
"""

import numpy as np

def get_objects(grid):
    """
    Find contiguous objects in the grid.
    Returns a dictionary of objects keyed by color.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(row, col, color, obj):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] != color:
            return
        visited.add((row, col))
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)

    return objects

def is_on_edge(grid, cell):
    """
    Check if given cell are on the edge of the grid
    """
    rows, cols = grid.shape
    r, c = cell
    return r == 0 or r == rows - 1 or c == 0 or c == cols - 1


def neighbours_only_zero(grid, object_pixels):
    """
    Checks all pixels to see if it only has zero or edge neighbours.
    """

    rows, cols = grid.shape
    for r,c in object_pixels:
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
          if grid[nr,nc]!=0 and grid[nr,nc]!=grid[r,c]:
            return False
    return True

def is_3x3_missing_corners(object_pixels):
    """
    Checks if the object has a 3x3 shape with missing corners.
    """
    if len(object_pixels) != 5:
        return False

    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    if max_row - min_row > 2 or max_col - min_col > 2:
        return False

    # Count pixels in each row and column within bounding box.
    row_counts = [0] * 3
    col_counts = [0] * 3

    for r, c in object_pixels:
        row_counts[r - min_row] += 1
        col_counts[c - min_col] += 1
    # check for 3x3 block shape
    if (row_counts == [1,3,1] and col_counts == [1,3,1] ):
      return True
    return False

def transform(input_grid):
    # Find objects in the input grid.
    objects = get_objects(input_grid)

    # Identify target colors (those that form shapes, not isolated, and don't just have 0 neighbours).
    target_colors = []
    for color, object_list in objects.items():
        for obj_pixels in object_list:
           if (is_3x3_missing_corners(obj_pixels) and
                not neighbours_only_zero(input_grid,obj_pixels) and
                not all(is_on_edge(input_grid, cell) for cell in obj_pixels)):
                target_colors.append(color)
                break  # Go to check next color

    # Construct output grid (5xN).
    output_grid = np.zeros((5, len(target_colors)), dtype=int)

    # Populate columns with target colors.
    for i, color in enumerate(target_colors):
        output_grid[:, i] = color

    return output_grid
```
