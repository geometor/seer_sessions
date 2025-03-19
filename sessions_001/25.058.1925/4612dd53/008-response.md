# 4612dd53 • 008 • refine_coder

---
```python
"""
The transformation identifies shapes created by blue objects. White cells
diagonally adjacent to blue pixels are changed to red.  Additionally, white pixels
above a line formed by connecting the two lowest blue pixels within an object are
also changed to red.
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

def is_diagonally_adjacent(r, c, object_coords):
    """Checks if a cell (r, c) is diagonally adjacent to any cell in object_coords."""
    for obj_r, obj_c in object_coords:
        if abs(r - obj_r) == 1 and abs(c - obj_c) == 1:
            return True
    return False

def find_lowest_blue_pixels(object_coords):
    """Finds the two lowest blue pixels within a single object."""
    # Sort by row index (descending) then by column index.
    sorted_coords = sorted(object_coords, key=lambda x: (x[0], x[1]), reverse=True)
    # If only one pixel, return it twice (line will have zero length)
    if len(sorted_coords) == 1:
        return sorted_coords[0], sorted_coords[0]

    # Get the two lowest distinct pixels
    lowest1 = sorted_coords[0]
    for pixel in sorted_coords[1:]:
        if pixel != lowest1:
            lowest2 = pixel
            break
        
    else:
        lowest2 = lowest1

    # lowest1 is guaranteed to be larger or equal, swap so that lowest1.r <= lowest2.r
    if lowest1[0] < lowest2[0] or (lowest1[0] == lowest2[0] and lowest1[1] > lowest2[1]):
        lowest1, lowest2 = lowest2, lowest1


    return lowest1, lowest2

def is_above_line(r, c, lowest1, lowest2):
    """Checks if a point (r, c) is above the line segment defined by p1 and p2.
    Handles edge cases for vertical and horizontal lines.
    """
    r1, c1 = lowest1
    r2, c2 = lowest2

    if r1 == r2: # Horizontal line
        return r < r1

    if c1 == c2: # vertical line
       return r < r1 and (c >= min(c1,c2) and c <= max(c1,c2)) # Check

    # Calculate the slope and y-intercept
    m = (r2 - r1) / (c2 - c1)
    b = r1 - m * c1

    # Check if the point is above the line
    line_y_at_c = m * c + b
    return r < line_y_at_c

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
                    # Check diagonal adjacency first.
                    if is_diagonally_adjacent(r, c, obj_coords):
                        output_grid[r][c] = 2
                        continue # move to next cell

                    # Check if inside using the "above the lowest line" definition.
                    lowest1, lowest2 = find_lowest_blue_pixels(obj_coords)

                    if is_above_line(r, c, lowest1, lowest2):
                         output_grid[r][c] = 2 # set to red


    return output_grid
```
