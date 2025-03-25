"""
1.  **Identify Horizontal Line:** Scan the input grid to find a single horizontal line. This line must be of a uniform, non-zero color and extend across the entire width of the grid. Note the line's row index and color.

2.  **Object Identification:** Locate all distinct objects in the input grid. An object is a contiguous group of pixels of the same color. Exclude pixels belonging to the horizontal line found in step 1, as well as background pixels (color 0).

3.  **Mirror Objects:** For each object, mirror its position vertically across the horizontal line identified in step 1.  The mirrored row index is calculated as `2 * horizontal_line_row - original_row`. The column index stays the same.

4.  **Recolor Objects:** Change the color of all mirrored objects to be the same as the horizontal line's color.

5. **Determine Output Grid**
    * calculate a bounding box that contains all the mirrored objects from all the previous steps
    * if any of the mirrored object extend past row 0, add a shift to all objects so that the minimum row is 0
    * the output dimensions are determined by (max_row - min_row +1, max_col - min_col +1)
    * Create an output grid filled with background pixels

6.  **Populate Output Grid**: Place each mirrored and recolored object onto the output grid.
   *  Adjust object positions using the following offsets:
        *   row_offset = - min_row_of_bounding_box
        *   col_offset = - min_col_of_bounding_box

7.  **Final Output:** Return the created output grid. The horizontal line itself is *not* part of the output; only the mirrored and recolored objects are included.
"""

import numpy as np

def find_horizontal_line(grid):
    """Finds the horizontal line and its color."""
    rows, cols = grid.shape
    for r in range(rows):
        first_val = grid[r, 0]
        if first_val == 0:  # Skip lines that start with 0
            continue
        if np.all(grid[r, :] == first_val):
            return r, first_val
    return None, None

def find_objects(grid, exclude_row, exclude_color):
    """Finds objects, excluding a row and color."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(r, c, color, obj_pixels):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or
                grid[r, c] != color or r == exclude_row):
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0 and grid[r, c] != exclude_color:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                objects.append(obj_pixels)
    return objects

def mirror_object(obj_pixels, horizontal_line_row):
    """Mirrors object pixels vertically across the horizontal line."""
    mirrored_pixels = []
    for r, c in obj_pixels:
        mirrored_r = 2 * horizontal_line_row - r
        mirrored_pixels.append((mirrored_r, c))
    return mirrored_pixels

def get_bounding_box(mirrored_objects):
    """Calculates the bounding box of a list of mirrored objects."""
    if not mirrored_objects:
        return None

    min_row = min(px[0] for obj in mirrored_objects for px in obj)
    max_row = max(px[0] for obj in mirrored_objects for px in obj)
    min_col = min(px[1] for obj in mirrored_objects for px in obj)
    max_col = max(px[1] for obj in mirrored_objects for px in obj)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Horizontal Line
    horizontal_line_row, horizontal_line_color = find_horizontal_line(input_grid)

    # 2. Object Identification
    objects = find_objects(input_grid, horizontal_line_row, horizontal_line_color)

    # 3. Mirror Objects & 4. Recolor Objects
    mirrored_objects = []
    for obj in objects:
        mirrored_pixels = mirror_object(obj, horizontal_line_row)
        mirrored_objects.append([(r, c, horizontal_line_color) for r, c in mirrored_pixels])

    # 5. Determine Output Grid
    bbox = get_bounding_box(mirrored_objects)
    if not bbox:
      return np.zeros((0,0), dtype=int).tolist()

    min_row, max_row, min_col, max_col = bbox

    # Handle negative rows and calculate output grid size
    row_shift = 0
    if min_row < 0:
        row_shift = -min_row

    output_rows = max_row + row_shift + 1
    output_cols = max_col - min_col + 1
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # 6. Populate Output Grid
    for obj in mirrored_objects:
      for r, c, color in obj:
        adjusted_r = r + row_shift
        adjusted_c = c-min_col
        if adjusted_r >=0 and adjusted_r < output_rows and adjusted_c >= 0 and adjusted_c < output_cols:
              output_grid[adjusted_r, adjusted_c] = color

    # 7. Final Output
    return output_grid.tolist()