"""
The transformation rule can be described as follows:

1.  **Identify the Object:** Find the contiguous block of pixels with color 5 (gray) in the input grid. This represents the target object.
2.  **Outline the Object:** Replace the outer boundary pixels of the gray object with color 8 (azure). An outer boundary pixel is any pixel of the object that is adjacent (up, down, left, or right) to a pixel that is *not* part of the object.
3.  **Inner Fill:** All pixels that are part of the object, but *not* part of the outline, are considered inner pixels.
    * if the object has more than 1 row: the pixels *adjacent* to the outline, *inside* the shape, also become azure.
    * the remaining inner pixels are set to color 2 (red).
"""

import numpy as np

def get_object(grid, color):
    """
    Finds the coordinates of a contiguous object of a specified color.
    """
    object_coords = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                dfs(r, c)
                return object_coords  # Return after finding the first object
    return []


def get_outer_pixels(grid, object_coords):
    """
    Determines the outer boundary pixels of an object.
    """
    
    rows, cols = grid.shape
    outer_pixels = set()
    for r,c in object_coords:
        for dr, dc in [(0,1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols and (nr, nc) in object_coords):
                outer_pixels.add((r,c))
                break # move onto next pixel
    return list(outer_pixels)

def get_inner_pixels(object_coords, outer_pixels):
    """
    Gets the inner pixels of an object
    """
    return list(set(object_coords) - set(outer_pixels))

def get_adjacent_inner_pixels(grid, object_coords, outer_pixels):
    """
    Finds inner pixels adjacent to the outer pixels.
    """
    rows, cols = grid.shape
    inner_pixels = get_inner_pixels(object_coords, outer_pixels)
    adjacent_inner_pixels = set()

    for r, c in inner_pixels:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in outer_pixels:
                adjacent_inner_pixels.add((r,c))
                break # important - once we find it, go to the next one
    return list(adjacent_inner_pixels)
    

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify the Object
    object_coords = get_object(input_grid, 5)
    if not object_coords:
        return output_grid.tolist()

    # 2. Outer Replacement (Outline)
    outer_pixels = get_outer_pixels(input_grid, object_coords)
    for r, c in outer_pixels:
        output_grid[r, c] = 8

    # 3. Inner Fill
    
    adjacent_inner = get_adjacent_inner_pixels(input_grid, object_coords, outer_pixels)
    for r,c in adjacent_inner:
        output_grid[r,c] = 8
    
    inner_pixels = get_inner_pixels(object_coords, outer_pixels)
    remaining_inner_pixels = list(set(inner_pixels) - set(adjacent_inner))

    for r, c in remaining_inner_pixels:
      output_grid[r,c] = 2

    return output_grid.tolist()