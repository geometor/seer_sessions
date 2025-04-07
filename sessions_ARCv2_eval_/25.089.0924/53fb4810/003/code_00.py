import numpy as np
from collections import deque

"""
Transformation Rule:

1.  Identify all distinct blue (1) objects in the input grid.
2.  Determine the "lower" blue object based on the maximum row index of its pixels. If there's a tie in max row, use the one with the higher minimum row index.
3.  Find the top-most row index (`min_row_lower`) of the lower blue object.
4.  Find all columns occupied by blue pixels in this top-most row (`top_cols_lower`).
5.  Identify "source pixels": Iterate through rows `r` from 0 up to (`min_row_lower` - 1). For each column `c` in `top_cols_lower`, if the pixel `input_grid[r, c]` is not blue (1) and not the background color (azure 8), it is a source pixel. Store these source pixels with their color and coordinates.
6.  Initialize the output grid as a copy of the input grid.
7.  Remove the identified source pixels from the output grid (change their color to the background color, azure 8).
8.  Determine the target columns (`target_cols`) for the new vertical lines: These are the unique column indices of all identified source pixels.
9.  Determine the two primary colors for the lines (`color1`, `color2`):
    a.  Find the source pixel(s) with the maximum row index among all source pixels.
    b.  If there's a unique pixel at the maximum row, `color1` is its color.
    c.  If multiple pixels share the maximum row index, find the one among them with the minimum column index. `color1` is its color.
    d.  `color2` is the other distinct color found among the source pixels. (Assumes exactly two distinct source colors).
10. Determine the height (`height_line`) for the new vertical lines: `height_line = min_row_lower`.
11. Generate the new vertical lines in the output grid: For each `target_col` in `target_cols`:
    a.  Determine the starting color for this column's line: If `target_col` is even, the pattern starts with `color1`. If `target_col` is odd, the pattern starts with `color2`.
    b.  Iterate from `row = 0` up to `height_line - 1`.
    c.  Set the pixel `output_grid[row, target_col]` using an alternating pattern based on the row index and the starting color for the column. If the starting color is `c_start` and the other color is `c_other`, the pattern is `c_start` for even rows and `c_other` for odd rows.
12. Return the modified output grid.
"""

def find_objects(grid, color):
    """Finds all connected objects (pixels sharing an edge) of a given color."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r, min_c, max_c = r, r, c, c
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    # Check 4 neighbours (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_pixels:
                    objects.append({'pixels': obj_pixels, 'min_row': min_r, 'max_row': max_r, 'min_col': min_c, 'max_col': max_c})
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 8
    blue_color = 1

    # 1. Find blue objects
    blue_objects_info = find_objects(input_grid, blue_color)

    if len(blue_objects_info) != 2:
        # Assumption based on examples: there are always exactly two blue objects.
        # If not, return the original grid or handle error as appropriate.
        print("Warning: Expected 2 blue objects, found {}.".format(len(blue_objects_info)))
        return output_grid

    # 2. Determine the lower blue object
    obj1 = blue_objects_info[0]
    obj2 = blue_objects_info[1]

    if obj1['max_row'] > obj2['max_row']:
        lower_blue_obj_info = obj1
    elif obj2['max_row'] > obj1['max_row']:
        lower_blue_obj_info = obj2
    else:
        # Tie break using min_row (higher min_row means starts lower down)
        if obj1['min_row'] > obj2['min_row']:
            lower_blue_obj_info = obj1
        else:
            # Default to obj2 if min_rows are also equal (or obj2 has higher min_row)
            lower_blue_obj_info = obj2

    lower_blue_pixels = lower_blue_obj_info['pixels']

    # 3. Find the top-most row index of the lower blue object
    min_row_lower = lower_blue_obj_info['min_row']

    # 4. Find all columns occupied by blue pixels in this top-most row
    top_cols_lower = {c for r, c in lower_blue_pixels if r == min_row_lower}

    # 5. Identify source pixels
    source_pixels = [] # Store as {'color': color, 'row': r, 'col': c}
    source_colors = set()
    for r in range(min_row_lower): # Iterate rows above the blue object
        for c in top_cols_lower:   # Only check columns aligned with the top of the blue object
             pixel_color = input_grid[r, c]
             if pixel_color != blue_color and pixel_color != background_color:
                 source_pixels.append({'color': pixel_color, 'row': r, 'col': c})
                 source_colors.add(pixel_color)

    if not source_pixels:
        print("Warning: No source pixels found.")
        return output_grid # Or original grid?

    if len(source_colors) != 2:
        # Assumption based on examples: there are always exactly two source colors.
        print(f"Warning: Expected 2 source colors, found {len(source_colors)}.")
        # Fallback or error handling could be added here
        if not source_colors: return output_grid
        # If only one source color, maybe use it for both c1 and c2? Let's proceed cautiously.


    # 6. Initialize output grid (already done)

    # 7. Remove source pixels from the output grid
    for sp in source_pixels:
        output_grid[sp['row'], sp['col']] = background_color

    # 8. Determine target columns
    target_cols = sorted(list({sp['col'] for sp in source_pixels}))

    # 9. Determine the two primary colors (color1, color2)
    color1, color2 = -1, -1 # Default/error values
    if source_pixels:
        max_r_source = -1
        for sp in source_pixels:
            max_r_source = max(max_r_source, sp['row'])

        pixels_at_max_r = [sp for sp in source_pixels if sp['row'] == max_r_source]

        if len(pixels_at_max_r) == 1:
            color1 = pixels_at_max_r[0]['color']
        else:
            # Tie break using min column
            pixels_at_max_r.sort(key=lambda p: p['col'])
            color1 = pixels_at_max_r[0]['color']

        # Find the other color
        other_colors = [sp['color'] for sp in source_pixels if sp['color'] != color1]
        if other_colors:
            color2 = other_colors[0]
        elif len(source_colors) == 1: # Handle case where only one source color was found
             color2 = color1
        else:
             print("Error determining color2") # Should not happen if len(source_colors)==2

    # 10. Determine the height for the new vertical lines
    height_line = min_row_lower

    # 11. Generate the new vertical lines
    for target_col in target_cols:
        # Determine starting color based on column parity
        if target_col % 2 == 0: # Even column
            c_start = color1
            c_other = color2
        else: # Odd column
            c_start = color2
            c_other = color1

        # Fill the column with the alternating pattern
        for r in range(height_line):
            if r % 2 == 0: # Even row
                output_grid[r, target_col] = c_start
            else: # Odd row
                output_grid[r, target_col] = c_other

    return output_grid