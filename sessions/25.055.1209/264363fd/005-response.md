# 264363fd • 005 • refine_coder

---
```python
"""
1.  **Identify Blue Objects:** Locate all contiguous regions of blue (color 1) pixels. These are considered individual objects.
2.  **Create Inner Border:** For each blue object, determine its inner border. The inner border consists of the pixels immediately adjacent to the outer boundary of the object, *within* the object itself.
3. **Color Inner Border (Filled Objects):** If a blue object is a fully filled shape (e.g. complete rectangle, square), then color all pixels of its inner border *red*, *unless* that border is a only single pixel wide.
4. **Color Inner Border (L-shapes and U-shapes i.e., single-pixel border sections):** If a section of the border is only a single pixel wide, color the pixel *green* only if it connects perpendicular borders. Color a single pixel border red, if it does not connect two borders.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                stack = [(r, c)]
                while stack:
                    curr_r, curr_c = stack.pop()
                    if 0 <= curr_r < rows and 0 <= curr_c < cols and grid[curr_r, curr_c] == color and not visited[curr_r, curr_c]:
                        visited[curr_r, curr_c] = True
                        obj.append((curr_r, curr_c))
                        stack.extend([(curr_r + 1, curr_c), (curr_r - 1, curr_c),
                                      (curr_r, curr_c + 1), (curr_r, curr_c - 1)])
                objects.append(obj)
    return objects

def get_inner_border(obj, grid):
    """Calculates the inner border of an object."""
    rows, cols = grid.shape
    inner_border = set()
    obj_set = set(obj)

    for r, c in obj:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in obj_set:
                inner_border.add((r,c)) # the inner border are those pixels IN the object adjacent to the outside
                break # only need to find ONE neighbor outside to know it is on a border
    return list(inner_border)

def is_connecting_corner(grid, r, c, obj):
    """
    Checks if a pixel at (r, c) on a single-pixel-wide border
    connects perpendicular borders within the object.

    Returns True if (r, c) is a connecting corner, and False otherwise.
    """
    rows, cols = grid.shape
    obj_set = set(obj)
    neighbors = []

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr,nc) in obj_set:
            neighbors.append((dr, dc))

    # Check if there are at least two neighbors and they are perpendicular
    if len(neighbors) >= 2:
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                dr1, dc1 = neighbors[i]
                dr2, dc2 = neighbors[j]
                if dr1 * dr2 + dc1 * dc2 == 0:  # Dot product is 0 for perpendicular vectors
                    return True

    return False
  
def is_single_pixel_wide(grid, r, c, obj):
    """
    Checks if the pixel at (r,c) is part of a single-pixel wide section of the
    object's border.  This considers both horizontal and vertical single-pixel
    wide sections.
    """
    rows, cols = grid.shape
    obj_set = set(obj)
    horizontal_count = 0
    vertical_count = 0

     # Check horizontal neighbors
    for dc in [-1, 1]:
        nc = c + dc
        if 0 <= nc < cols and (r, nc) in obj_set:
            horizontal_count += 1

    # Check vertical neighbors
    for dr in [-1, 1]:
        nr = r + dr
        if 0 <= nr < rows and (nr, c) in obj_set:
            vertical_count += 1

    return horizontal_count == 0 or vertical_count == 0
    

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    blue_objects = find_objects(input_grid, 1)

    for obj in blue_objects:
        inner_border = get_inner_border(obj, input_grid)
        is_filled = len(inner_border) < len(obj) # filled object has a border less than total size

        for r, c in inner_border:
            if is_filled:
                # filled object - color inner border red, unless it is single pixel width
                if is_single_pixel_wide(input_grid, r, c, obj):
                    if is_connecting_corner(input_grid, r, c, obj):
                        output_grid[r,c] = 3 # green
                    else:
                        output_grid[r,c] = 2 #red
                else:
                    output_grid[r, c] = 2  # Red
            else:
                # not filled, so it IS a single-pixel border
                if is_connecting_corner(input_grid, r, c, obj):
                    output_grid[r,c] = 3 # green
                else:
                    output_grid[r,c] = 2 # red
    return output_grid
```
