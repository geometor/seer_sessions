# 4612dd53 • 007 • refine_coder

---
```python
"""
Transforms white pixels to red based on their position relative to blue objects. White pixels inside a blue object or diagonally adjacent to multiple blue pixels are changed to red.
"""

import numpy as np

def find_blue_objects(grid):
    """Finds contiguous regions of blue (1) pixels."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != 1:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_inside(r, c, object_coords, grid):
    """Checks if a white pixel is inside a blue object."""
    rows, cols = len(grid), len(grid[0])
    min_r = min(coord[0] for coord in object_coords)
    max_r = max(coord[0] for coord in object_coords)
    min_c = min(coord[1] for coord in object_coords)
    max_c = max(coord[1] for coord in object_coords)

    if not (min_r <= r <= max_r and min_c <= c <= max_c):
        return False

    # Check if the cell is within the bounding box and not on the outer edge
    if r == min_r or r == max_r or c == min_c or c == max_c:
      return False
    
    return True



def count_adjacent_blue_pixels(r, c, grid):
    """Counts blue pixels adjacent (orthogonally and diagonally) to (r, c)."""
    count = 0
    rows, cols = len(grid), len(grid[0])
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                count += 1
    return count

def transform(input_grid):
    # Initialize output_grid with a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = len(input_grid), len(input_grid[0])

    # Find blue objects
    blue_objects = find_blue_objects(input_grid)

    # Iterate through all cells
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:  # Consider only white cells
                for obj_coords in blue_objects:
                    # Inside check
                    if is_inside(r, c, obj_coords, input_grid):
                        output_grid[r][c] = 2
                        break  # If inside, no need to check other conditions

                    # Diagonal and adjacent check
                    adjacent_blue_count = count_adjacent_blue_pixels(r, c, input_grid)
                    if adjacent_blue_count >= 2 :
                        output_grid[r][c] = 2 # color red
                        break


    return output_grid
```
