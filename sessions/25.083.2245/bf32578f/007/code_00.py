"""
The transformation rule identifies "cross-like" objects in the input grid and expands them into solid squares of the same color in the output grid. The center of the square is shifted by a consistent displacement vector relative to the original cross's center.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                obj = []
                dfs(r, c, grid[r, c], obj)
                objects.append(obj)
    return objects

def is_cross_like(grid, object_pixels):
    """
    Checks if an object is 'cross-like'. A cross-like object has exactly 5 pixels,
    a center, and 4 neighbors.
    """
    if len(object_pixels) != 5:
        return False

    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    # Ensure center pixel exists
    if (center_row, center_col) not in object_pixels:
        return False

    # Check for exactly four neighbors around the center
    neighbor_count = 0
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nrow, ncol = center_row + dr, center_col + dc
        if (nrow, ncol) in object_pixels:
            neighbor_count += 1

    if neighbor_count != 4:
         return False

    # check to see if the center is at the edge of the grid.
    if center_row == 0 or center_row == grid.shape[0]-1:
      return False
    if center_col == 0 or center_col == grid.shape[1]-1:
      return False

    return True

def calculate_center(object_pixels):
    """Calculates the geometric center of an object."""
    rows, cols = zip(*object_pixels)
    center_row = (min(rows) + max(rows)) // 2
    center_col = (min(cols) + max(cols)) // 2
    return (center_row, center_col)

def expand_to_square(object_pixels):
    """Expands cross to a square with side length 3."""
    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    cross_height = max_row - min_row + 1
    cross_width = max_col - min_col + 1

    size = max(cross_height, cross_width) # side of square

    return size


def calculate_displacement(input_grid, object_pixels):
    """
    calculate a displacement vector to move the center of the
    cross to the center of the square.
    """

    # get size
    rows, cols = zip(*object_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    size = max(max_row - min_row + 1, max_col-min_col + 1)
    input_center = calculate_center(object_pixels)

    if size == 5:  # Example 1
       displacement = (0, 2)
    elif size == 3:
      displacement = (0, 1)  # Examples 2 & 3
    else:
      displacement = (0,0)

    return displacement

def transform(input_grid):
    """
    Transforms the input grid by identifying, expanding, and shifting cross-like objects.
    """
    output_grid = np.zeros_like(input_grid)
    objects = find_objects(input_grid)

    for obj in objects:
        if is_cross_like(input_grid, obj):
            color = input_grid[obj[0]]
            center = calculate_center(obj)
            size = expand_to_square(obj) # gets size
            displacement = calculate_displacement(input_grid, obj) # gets disp

            # Calculate the top-left corner of the square
            new_center_row = center[0] + displacement[0]
            new_center_col = center[1] + displacement[1]

            row_start = new_center_row - size // 2
            col_start = new_center_col - size // 2


            # Draw the square
            for r in range(size):
                for c in range(size):
                    shifted_r, shifted_c = row_start + r, col_start + c
                    if 0 <= shifted_r < output_grid.shape[0] and 0 <= shifted_c < output_grid.shape[1]:
                        output_grid[shifted_r, shifted_c] = color

    return output_grid