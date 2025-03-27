"""
1.  **Identify Objects:** Identify all contiguous, non-zero colored regions in the input grid as distinct objects. Record their color, initial position (top-left corner), and shape.

2.  **Examine Row 5:** Determine if Row 5 of the input grid contains any non-zero pixels.

3.  **Conditional Object Removal/Duplication:**
    *   **If Row 5 has non-zero pixels:** Remove all objects that are entirely *above* row 5 in the input grid.
    *  **If and only if Row 5 is all zeros:** Duplicate all of the objects from above row 5 to row 5 downwards, until row 5 is filled with non-zero entries.

4.  **Move and Merge (Objects at or below Row 5):**
     * Iterate through the objects that were originally located at or below Row 5 in the input grid, preserving their original order (row-major order: top-to-bottom, then left-to-right).

5. **Fill available space:**
    * Find empty spaces, defined as runs of zeros.
    * For each object identified in step 4:
      *   Place it in the first available empty space in the output grid that can accommodate its shape, starting from the top-left corner (0,0) and proceeding in row-major order.
      * Do not split objects.

6. **Output:** The filled output array.
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
                    'shape': 'contiguous' # for this task all objects are contiguous
                })
    return objects

def find_empty_spaces(grid):
    """
    Finds contiguous blocks of zeros (empty spaces) in the grid.
    Returns a list of tuples, where each tuple contains the (row, col) of
    the top-left corner of the empty space, and its size (rows, cols).
    """
    rows, cols = grid.shape
    empty_spaces = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_space):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != 0):
            return
        visited[r, c] = True
        current_space.append((r,c))
        dfs(r + 1, c, current_space)
        dfs(r - 1, c, current_space)
        dfs(r, c + 1, current_space)
        dfs(r, c - 1, current_space)

    for r in range(rows):
        for c in range(cols):
            if not visited[r,c] and grid[r,c] == 0:
                current_space = []
                dfs(r, c, current_space)
                if current_space:
                    # calculate size of empty space
                    min_row = min(p[0] for p in current_space)
                    min_col = min(p[1] for p in current_space)
                    max_row = max(p[0] for p in current_space)
                    max_col = max(p[1] for p in current_space)

                    empty_spaces.append(((min_row, min_col), (max_row - min_row + 1, max_col - min_col + 1)))
    return empty_spaces

def can_place(grid, object_pixels, start_row, start_col):
    """Checks if an object can be placed at the given location without overlapping."""
    rows, cols = grid.shape
    for r, c in object_pixels:
        new_r, new_c = start_row + (r-object_pixels[0][0]), start_col + (c - object_pixels[0][1]) # offset based on topleft
        if (new_r < 0 or new_r >= rows or new_c < 0 or new_c >= cols or
                grid[new_r, new_c] != 0):
            return False
    return True

def place_object(grid, object_pixels, color, start_row, start_col):
    """Places the object onto the grid at the specified location."""
    for r, c in object_pixels:
        new_r, new_c = start_row + (r - object_pixels[0][0]), start_col + (c - object_pixels[0][1])  # offset based on topleft
        grid[new_r, new_c] = color

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Examine Row 5
    row_5_has_non_zero = np.any(input_grid[min(4, rows-1), :] != 0)  # min handles edge case

    # 3. Conditional Object Removal / Duplication
    objects_above_row_5 = [obj for obj in objects if obj['initial_position'][0] < min(5,rows)]
    objects_at_or_below_row_5 = [obj for obj in objects if obj['initial_position'][0] >= min(5,rows)]
    
    if row_5_has_non_zero:
      pass # objects above row 5 removed by not adding to output
    else:
        # Duplicate objects above row 5
        row_index = min(4, rows-1)
        
        while row_index < rows and not np.any(output_grid[row_index,:] != 0):
          for obj in objects_above_row_5:
            fill_row = row_index
            fill_col = 0
            for r, c in obj['pixels']:
              if fill_row < rows:
                output_grid[fill_row,fill_col] = obj['color']
                fill_col += 1
                if fill_col == cols:
                    fill_col = 0
                    fill_row += 1


            row_index += (max(r for r, c in obj['pixels']) - min(r for r, c in obj['pixels'])) + 1
          
            

    # 4 & 5. Move and Merge (Objects at or below Row 5) and place remaining from above
    
    
    empty_spaces = find_empty_spaces(output_grid)
    empty_space_index = 0

    
    for obj in objects_at_or_below_row_5:
      placed = False
      while empty_space_index < len(empty_spaces) and not placed:
            (start_row, start_col), (space_rows, space_cols) = empty_spaces[empty_space_index]
            if can_place(output_grid, obj['pixels'], start_row, start_col):
                place_object(output_grid, obj['pixels'], obj['color'], start_row, start_col)
                placed = True

                # update empty spaces
                new_empty_spaces = find_empty_spaces(output_grid)
                empty_spaces = new_empty_spaces
                empty_space_index = 0 # start from the beginning to fill any gaps made by the placement

            else:
                empty_space_index += 1

      if not placed:
        # no more space, drop the object, in theory this should not occur based
        # on the problem definition.
        pass


    return output_grid.tolist()