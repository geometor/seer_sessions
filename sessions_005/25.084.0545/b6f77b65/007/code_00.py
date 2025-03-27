"""
1.  **Identify Objects:** Find all contiguous regions of non-zero pixels. Record color, top-left position, shape (width and height), and pixel coordinates.

2.  **Check Row 5:** Check if Row 5 (index 4, or last row if height < 5) of the *input* has non-zero pixels.

3.  **Conditional Object Removal/Duplication:**
    *   **If Row 5 has non-zero pixels:** Remove objects with top-left row < 4.
    *   **If Row 5 has only zero pixels:** Duplicate and shift objects with top-left row < 4 to row 5 and below.

4.  **Place Remaining Objects:**
    *   Create an empty output grid.
    *   Find empty spaces (contiguous zeros) in the output grid.
    *   Iterate over remaining objects (original order).
    *   Place each object in the first fitting empty space (top-left), without overlapping.

5.  **Output:** Return the filled output grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid and records their properties."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                min_row = min(p[0] for p in obj_pixels)
                min_col = min(p[1] for p in obj_pixels)
                max_row = max(p[0] for p in obj_pixels)
                max_col = max(p[1] for p in obj_pixels)
                objects.append({
                    'color': grid[r, c],
                    'initial_position': (min_row, min_col),
                    'shape': (max_row - min_row + 1, max_col - min_col + 1),
                    'pixels': obj_pixels
                })
    return objects

def find_empty_spaces(grid):
    """Finds contiguous blocks of zeros (empty spaces)."""
    rows, cols = grid.shape
    empty_spaces = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_space):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != 0):
            return
        visited[r, c] = True
        current_space.append((r, c))
        dfs(r + 1, c, current_space)
        dfs(r - 1, c, current_space)
        dfs(r, c + 1, current_space)
        dfs(r, c - 1, current_space)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] == 0:
                current_space = []
                dfs(r, c, current_space)
                if current_space:
                    min_row = min(p[0] for p in current_space)
                    min_col = min(p[1] for p in current_space)
                    max_row = max(p[0] for p in current_space)
                    max_col = max(p[1] for p in current_space)
                    empty_spaces.append(((min_row, min_col), (max_row - min_row + 1, max_col - min_col + 1)))
    return empty_spaces

def can_place(grid, obj_shape, start_row, start_col):
    """Checks if an object of given shape can be placed at start_row, start_col."""
    rows, cols = grid.shape
    obj_height, obj_width = obj_shape
    if start_row + obj_height > rows or start_col + obj_width > cols:
        return False
    for r in range(obj_height):
        for c in range(obj_width):
            if grid[start_row + r, start_col + c] != 0:
                return False
    return True

def place_object(grid, obj_pixels, color, start_row, start_col):
    """Places an object onto the grid."""
    for r, c in obj_pixels:
        new_r, new_c = start_row + (r - obj_pixels[0][0]), start_col + (c - obj_pixels[0][1])
        grid[new_r, new_c] = color

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Check Row 5
    row_5_index = min(4, rows - 1)
    row_5_has_non_zero = np.any(input_grid[row_5_index, :] != 0)

    # 3. Conditional Object Removal/Duplication
    remaining_objects = []
    if row_5_has_non_zero:
        remaining_objects = [obj for obj in objects if obj['initial_position'][0] >= row_5_index]
    else:
        # Duplicate and shift objects above row 5
        objects_above_row_5 = [obj for obj in objects if obj['initial_position'][0] < row_5_index]
        row_index = row_5_index
        for obj in objects_above_row_5:
           obj_height = obj['shape'][0]
           if row_index + obj_height <= rows:  # Check if it fits
              place_object(output_grid, obj['pixels'], obj['color'], row_index, obj['initial_position'][1])
              row_index += obj_height

        remaining_objects = objects_above_row_5 + [obj for obj in objects if obj['initial_position'][0] >= row_5_index] # keep objects above for placement

    # 4. Place Remaining Objects
    empty_spaces = find_empty_spaces(output_grid)
    empty_space_index = 0

    for obj in remaining_objects:

        placed = False
        while empty_space_index < len(empty_spaces) and not placed:
            (start_row, start_col), (space_rows, space_cols) = empty_spaces[empty_space_index]
            if can_place(output_grid, obj['shape'], start_row, start_col):
                place_object(output_grid, obj['pixels'], obj['color'], start_row, start_col)
                placed = True
            else:
                empty_space_index += 1

    return output_grid.tolist()