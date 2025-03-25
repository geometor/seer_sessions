"""
The transformation rule is not a simple, single operation. It involves identifying objects, their relative positions, and performing one of a set of transformations, *possibly* based on initial visual features. Here's a revised natural language program:

1. **Object Identification:** Identify contiguous regions of the same color as distinct objects.
2. **Transformation Selection:**
    *   If the input contains maroon and white, and the maroon object fills most of the image: Swap the colors of the maroon and white objects, and then perform a reflection where the maroon object is on the bottom. It could be one of many reflections, either across the anti-diagonal or a combination of horizontal, vertical, or both.
    *   If the input contains magenta and white, perform a partial reflection across the horizontal axis.  It is *not* a full reflection.
    *   If the input contains white and maroon, and the white object is in the top-left: Reflect across the anti-diagonal.
    * If the input contains red and white objects, perform a 90-degree counter-clockwise rotation.
3. **Apply Transformation:** Perform the selected transformation on the identified objects.
"""

import numpy as np

def get_objects(grid):
    """Identifies contiguous regions of the same color as distinct objects."""
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                obj = []
                dfs(r, c, grid[r][c], obj)
                objects.append((grid[r][c], obj))  # Store color and coordinates
    return objects

def reflect_anti_diagonal(grid):
    """Reflects a grid across its anti-diagonal."""
    n = len(grid)
    new_grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_grid[i][j] = grid[n - 1 - j][n - 1 - i]
    return new_grid

def swap_colors(grid, color1, color2):
    """Swaps two colors in a grid."""
    new_grid = []
    for row in grid:
        new_row = [color2 if x == color1 else (color1 if x == color2 else x) for x in row]
        new_grid.append(new_row)
    return new_grid

def reflect_horizontal(grid):
    """Reflects a grid horizontally."""
    return [row[::-1] for row in grid]

def rotate_counter_clockwise(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    n = len(grid)
    new_grid = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_grid[i][j] = grid[j][n - 1 - i]
    return new_grid
    
def partial_horizontal_reflection(grid, objects):
    """Performs a partial horizontal reflection, modifying only magenta and white."""
    new_grid = [row[:] for row in grid]  # Create a deep copy
    rows = len(grid)
    
    for color, obj_coords in objects:
      if color == 6 or color == 0: #magenta or white
        for r,c in obj_coords:
          new_grid[r][cols - 1 -c] = grid[r][c]

    return new_grid

def transform(input_grid):
    # initialize output_grid
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    objects = get_objects(input_grid)


    if 9 in set(input_array.flatten()) and 0 in set(input_array.flatten()) :
      # Swap colors and anti-diagonal

        output_grid = swap_colors(input_grid, 9, 0)

        if input_array[0,0] == 9:
           output_grid = reflect_anti_diagonal(output_grid)
        else:
           output_grid = reflect_anti_diagonal(input_grid)

    elif 6 in set(input_array.flatten()) and 0 in set(input_array.flatten()) :
        # Partial horizontal reflection
        output_grid = partial_horizontal_reflection(input_grid, objects)
    elif 2 in set(input_array.flatten()) and 0 in set(input_array.flatten()):
      # rotate counter clockwise
        output_grid = rotate_counter_clockwise(input_grid)

    else:
      output_grid = input_grid

    return output_grid