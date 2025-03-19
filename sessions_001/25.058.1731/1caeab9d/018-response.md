# 1caeab9d • 018 • refine_coder

---
```python
"""
1. **Identify Objects:** Find all distinct rectangular regions of uniform color within the input grid, ignoring the background color (0/white).
2. **Find Empty Space Above:** For each object, scan upwards from the top of the object until an empty row (all white/0 pixels) is found, or the top of the grid is reached.
3. **Translate Vertically:** Move each identified object upwards. The bottom row of the object should be one row below the empty row found in step 2. If no empty row is found above, the object is placed at the top of the grid.
4. **Output:** Create an output grid of the same dimensions as the input grid, initially filled with the background color (0). Place the translated objects onto this grid at their new positions.

"""

import numpy as np

def find_objects(grid):
    # Find rectangular blocks of uniform color (excluding 0/white)
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                color = grid[r, c]
                # Explore the connected region
                stack = [(r, c)]
                visited[r, c] = True
                min_row, max_row = r, r
                min_col, max_col = c, c

                while stack:
                    curr_row, curr_col = stack.pop()
                    min_row = min(min_row, curr_row)
                    max_row = max(max_row, curr_row)
                    min_col = min(min_col, curr_col)
                    max_col = max(max_col, curr_col)

                    # Check neighbors (up, down, left, right)
                    neighbors = []
                    if curr_row > 0:
                        neighbors.append((curr_row - 1, curr_col))
                    if curr_row < rows - 1:
                        neighbors.append((curr_row + 1, curr_col))
                    if curr_col > 0:
                        neighbors.append((curr_row, curr_col - 1))
                    if curr_col < cols - 1:
                        neighbors.append((curr_row, curr_col + 1))

                    for nr, nc in neighbors:
                        if not visited[nr, nc] and grid[nr, nc] == color:
                            stack.append((nr, nc))
                            visited[nr, nc] = True
                objects.append({
                    'color': color,
                    'min_row': min_row,
                    'max_row': max_row,
                    'min_col': min_col,
                    'max_col': max_col,
                    'height': max_row - min_row + 1,
                    'width' : max_col - min_col + 1
                })
    return objects

def find_empty_row_above(grid, obj):
    # Find the first empty row above the object
    for r in range(obj['min_row'] - 1, -1, -1):
        if np.all(grid[r, :] == 0):
            return r
    return -1  # Return -1 if no empty row is found (place at top)

def transform(input_grid):
    # Initialize output_grid as all zeros
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Move each object to the target row
    for obj in objects:
        # Find the empty row above
        empty_row = find_empty_row_above(input_grid, obj)

        # Calculate target row (one row below the empty row)
        target_row = empty_row

        # Calculate object dimensions and position
        obj_height = obj['height']
        start_col = obj['min_col']
        end_col = obj['max_col']

        # Place the object in the output grid
        for c in range(start_col, end_col + 1):
            for r in range(obj_height):
                output_grid[target_row - obj_height + 1 + r, c] = obj['color']


    return output_grid
```
