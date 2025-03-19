# 54d82841 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Magenta Shapes:** Locate all contiguous blocks (shapes) of magenta (6) pixels within the input grid. Note the range of columns containing each of these objects.
2. **Bottom Row Modification**: For the bottom row only, examine the locations where the column above contains a pixel belonging to one of the shapes identified in step one. In these columns, change the pixel color to yellow (4).
3.  **Preserve Other Pixels:** All other pixels in the grid remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous objects of a specific color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                object_coords = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    object_coords.append((curr_r, curr_c))

                    # Check adjacent cells
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < rows and 0 <= new_c < cols and \
                           grid[new_r, new_c] == color and not visited[new_r, new_c]:
                            stack.append((new_r, new_c))
                            visited[new_r, new_c] = True
                objects.append(object_coords)

    return objects

def get_column_range(object_coords):
    # Get min and max column from an object
    columns = [c for _, c in object_coords]
     # Return as a set
    return set(columns)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find magenta objects
    magenta_objects = find_objects(input_grid, 6)

    # Get the column range for all magenta objects
    magenta_columns = set()
    for obj in magenta_objects:
      magenta_columns.update(get_column_range(obj))

    # Modify the bottom row based on magenta columns
    for c in range(cols):
        if c in magenta_columns:
            output_grid[rows - 1, c] = 4

    return output_grid
```
