```python
"""
1.  **Object Identification:** Identify all contiguous, non-zero colored regions (objects) in the input grid. Record their color, top-left corner position, and the pixels that define them.

2.  **Row 5 Check:** Examine Row 5 (index 4) of the *input* grid.

3.  **Conditional Action (Above Row 5):**
    *   **If Row 5 has *any* non-zero pixels:** Remove all objects whose top-left corner is *strictly above* Row 5 (row index < 4) from the output.
    * **If Row 5 has *only* zero pixels:** Duplicate the objects with their top-left pixels above row 5. Copy them from their original positions to row five and below until row 5 is filled.

4.  **Reposition Objects (At or Below Row 5):** Iterate through the objects whose top-left corners were originally at or below Row 5 in the input grid. Maintain their original order (top-to-bottom, left-to-right).

5.  **Placement:**
    * Find empty spaces in the output grid, defined as runs of contiguous zeros.
    * Place each of the remaining objects in the first available empty space in the output that fully accommodates the object, going from top left to right.
    * Objects must fit without changing shape.

6. **Output:** Return filled output grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
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
                # find top-left
                min_row = min(p[0] for p in obj_pixels)
                min_col = min(p[1] for p in obj_pixels)

                objects.append({
                    'color': grid[r, c],
                    'initial_position': (min_row, min_col),
                    'pixels': obj_pixels,
                    'shape': 'contiguous'
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

def can_place(grid, obj_pixels, start_row, start_col):
    """Checks if an object can be placed."""
    rows, cols = grid.shape
    for r, c in obj_pixels:
        new_r, new_c = start_row + (r - obj_pixels[0][0]), start_col + (c - obj_pixels[0][1])
        if (new_r < 0 or new_r >= rows or new_c < 0 or new_c >= cols or
                grid[new_r, new_c] != 0):
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

    # 1. Object Identification
    objects = find_objects(input_grid)

    # 2. Row 5 Check
    row_5_has_non_zero = np.any(input_grid[min(4, rows - 1), :] != 0)

    # 3. Conditional Action (Above Row 5)
    objects_above_row_5 = [obj for obj in objects if obj['initial_position'][0] < min(4, rows)]
    objects_at_or_below_row_5 = [obj for obj in objects if obj['initial_position'][0] >= min(4, rows)]

    if row_5_has_non_zero:
        # Remove objects above Row 5
        pass  # Don't add them to the output
    else:
        # Duplicate and shift objects above row 5
        row_index = min(4, rows - 1)
        for obj in objects_above_row_5:
            obj_height = max(r for r, _ in obj['pixels']) - min(r for r, _ in obj['pixels']) + 1
            if row_index + obj_height <= rows: # check if it fits
              place_object(output_grid, obj['pixels'], obj['color'], row_index, obj['initial_position'][1])
              row_index += obj_height

    # 4. Reposition Objects (At or Below Row 5) & 5. Placement

    empty_spaces = find_empty_spaces(output_grid)
    empty_space_index = 0

    for obj in objects_at_or_below_row_5:
        placed = False
        while empty_space_index < len(empty_spaces) and not placed:
            (start_row, start_col), (space_rows, space_cols) = empty_spaces[empty_space_index]
            if can_place(output_grid, obj['pixels'], start_row, start_col):
                place_object(output_grid, obj['pixels'], obj['color'], start_row, start_col)
                placed = True
                # Recalculate empty spaces
                empty_spaces = find_empty_spaces(output_grid)
                empty_space_index = 0  # Reset to start from top-left
            else:
                empty_space_index += 1

    return output_grid.tolist()
```