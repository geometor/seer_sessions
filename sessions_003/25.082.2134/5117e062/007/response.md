```python
"""
1.  **Identify Objects:** Find all contiguous objects in the input grid.
2.  **Find the "L" Object:** Locate the "L"-shaped object (color 0, three pixels, two with one neighbor, one with two).
3.  **Identify the Enclosed Object:** Find the object enclosed by the "L" object (any color other than 0, adjacent to L-object).
4.  **Create Output Grid:** Construct a 3x3 output grid.
5.  **Fill Output Grid:** Fill with the color of the enclosed object.
6.  **Overlay L-Shape:** Determine orientation (top-left, top-right, bottom-left, bottom-right).
7.  **Place "L" Pixels:** Overlay the "L" shape (color 0) based on orientation.
8.  **If no enclosed object, output a grid full of zeros.**
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r][c], current_object)
                if current_object:
                    objects.append((grid[r][c], current_object))
    return objects

def find_l_object(objects):
    """Finds the L-shaped object (color 0, three pixels, correct neighbor counts)."""
    for color, obj in objects:
        if color == 0 and len(obj) == 3:
            neighbors = 0
            neighbor_counts = {}
            for r, c in obj:
                neighbor_counts[(r,c)] = 0

            for r, c in obj:
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in obj:
                        neighbor_counts[(r,c)] += 1

            one_neighbor_count = 0
            two_neighbor_count = 0
            for count in neighbor_counts.values():
                if count == 1:
                    one_neighbor_count += 1
                elif count == 2:
                    two_neighbor_count += 1

            if one_neighbor_count == 2 and two_neighbor_count == 1:
                return obj
    return None

def get_neighbors(grid, r, c):
    """Gets the neighbors of a cell, including diagonals."""
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors


def find_enclosed_object(grid, objects, l_object):
    """Finds the object enclosed by the L-shaped object. Considers direct adjacency to L."""
    if not l_object:
        return None, None

    for color, obj in objects:
        if color == 0:  # Skip the L-object itself
            continue

        enclosed = False
        for r, c in obj:
            neighbors = get_neighbors(grid, r, c)
            for nr, nc in neighbors:
                if (nr, nc) in l_object:
                    enclosed = True  # At least one neighbor is part of L
                    break
            if enclosed: # if one pixel of the object is next to l, the whole object is enclosed
                break

        if enclosed:
            return color, obj

    return None, None


def determine_orientation(l_object):
    """Determines the orientation of the L shape."""
    rows, cols = zip(*l_object)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Count pixels in each row and column of the bounding box
    row_counts = [0] * (max_r - min_r + 1)
    col_counts = [0] * (max_c - min_c + 1)

    for r, c in l_object:
      row_counts[r - min_r] += 1
      col_counts[c - min_c] += 1

    # Determine orientation based on counts:
    if row_counts[0] > 0 and row_counts[-1] == 0 and col_counts[0] > 0 and col_counts[-1] == 0:
        return "top-left" #standard L
    elif row_counts[0] > 0 and row_counts[-1] == 0 and col_counts[0] == 0 and col_counts[-1] > 0:
        return "top-right" # reverse L
    elif row_counts[0] == 0 and row_counts[-1] > 0 and col_counts[0] > 0 and col_counts[-1] == 0:
         return "bottom-left" # flipped
    else:
        return 'bottom-right'


def transform(input_grid):
    """Transforms the input grid according to the rules."""

    grid = np.array(input_grid)

    # 1. Object Identification
    objects = find_objects(grid)
    l_object = find_l_object(objects)
    enclosed_color, enclosed_object = find_enclosed_object(grid, objects, l_object)

    # If no enclosed object, return all zeros (as per instructions, if this happens)
    if enclosed_color is None:
      return [[0,0,0],[0,0,0],[0,0,0]]

    # 2. Output Construction
    output_grid = np.full((3, 3), enclosed_color)

    # 3. Overlay "L" Shape
    orientation = determine_orientation(l_object)

    if orientation == "top-left":
        output_grid[0, 0] = 0
        output_grid[1, 0] = 0
        output_grid[0, 1] = 0
    elif orientation == "top-right":
        output_grid[0, 2] = 0
        output_grid[0, 1] = 0
        output_grid[1, 2] = 0
    elif orientation == "bottom-left":
        output_grid[2, 0] = 0
        output_grid[1, 0] = 0
        output_grid[2, 1] = 0
    elif orientation == "bottom-right":
        output_grid[2, 2] = 0
        output_grid[2, 1] = 0
        output_grid[1, 2] = 0

    return output_grid.tolist()
```
