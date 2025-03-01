# 39e1d7f9 • 020 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions (objects) of the same color in the input grid.
2.  **Filter Objects:** Select only the 3x3 objects.
3. **Identify Transform Group**: Within the filtered objects, identify sets of 3x3 objects of color 2 (red) or 4 (yellow), that are stacked vertically.
4.  **Conditional Swap:** Within each identified group of vertically stacked 3x3 objects, swap colors 2 (red) and 4 (yellow).
    *   Change all pixels of color 2 within those objects to color 4.
    *   Change all pixels of color 4 within those objects to color 2.
5.  **Retain Other Pixels:** All other pixels in the grid that are not part of the identified and transformed group remain unchanged.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous regions of the same color."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_coords):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_coords.append((r, c))
        dfs(r + 1, c, color, obj_coords)
        dfs(r - 1, c, color, obj_coords)
        dfs(r, c + 1, color, obj_coords)
        dfs(r, c - 1, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                color = grid[r, c]
                obj_coords = []
                dfs(r, c, color, obj_coords)
                objects.append((color, obj_coords))
    return objects

def is_3x3(obj_coords):
    """Checks if an object is 3x3."""
    rows, cols = zip(*obj_coords)
    return (max(rows) - min(rows) + 1) == 3 and (max(cols) - min(cols) + 1) == 3

def are_vertically_stacked(obj1_coords, obj2_coords):
    """Checks if two 3x3 objects are vertically stacked."""
    min_row1, min_col1 = min(obj1_coords), min(obj1_coords, key=lambda x: x[1])[1]
    min_row2, min_col2 = min(obj2_coords), min(obj2_coords, key=lambda x: x[1])[1]

    if min_col1 == min_col2:
        if abs(min_row1 - min_row2) == 3:
            return True
    return False

def find_stacked_groups(objects):
    """
    Finds groups of vertically stacked 3x3 objects of colors 2 or 4.
    """
    groups = []
    processed = [False] * len(objects)

    for i in range(len(objects)):
        if processed[i]:
            continue

        color1, coords1 = objects[i]
        if not (is_3x3(coords1) and color1 in (2, 4)):
          processed[i] = True
          continue

        group = [(color1, coords1)]
        processed[i] = True

        for j in range(len(objects)):
            if i != j and not processed[j]:
                color2, coords2 = objects[j]
                if not (is_3x3(coords2) and color2 in (2, 4)):
                  processed[j] = True
                  continue

                # Check if coords2 is stacked with any object in the current group
                for _, existing_coords in group:
                    if are_vertically_stacked(existing_coords, coords2):
                        group.append((color2, coords2))
                        processed[j] = True
                        break  # Move to the next object after adding to the group
        
        #only add groups with more than one object
        if len(group) > 1:          
          groups.append(group)

    return groups


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all objects
    objects = find_objects(input_grid)

    # Find stacked groups of 3x3 objects with colors 2 or 4
    stacked_groups = find_stacked_groups(objects)

    # Perform swaps within each stacked group
    for group in stacked_groups:
        for color, coords in group:
            for r, c in coords:
                if color == 2:
                    output_grid[r, c] = 4
                elif color == 4:
                    output_grid[r, c] = 2

    return output_grid
```
