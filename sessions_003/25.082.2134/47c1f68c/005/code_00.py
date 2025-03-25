"""
1.  **Identify Horizontal Line:** Find the single horizontal line of a uniform, non-zero color that spans the entire width of the input grid. Record the row index and color of this line.
2.  **Identify Objects:**  Identify all contiguous shapes (objects) in the input grid. An object is a group of connected pixels of the same color. Exclude pixels that are part of the horizontal line found in step 1, and also exclude background pixels (color 0).
3.  **Mirror Objects:** For each object found in step 2, mirror its position *vertically* across the horizontal line identified in step 1.  The mirrored position's row index will change, but the column index will remain the same.
4.  **Recolor Objects:** Change the color of all mirrored objects to the color of the horizontal line (from step 1).
5.  **Create Output Grid:** Create a new grid, initially filled with 0s. The size of this grid should be the smallest possible rectangle that can contain *all* the mirrored objects. The horizontal line itself is *not* included in the output, only the mirrored objects.
6. **Blank Horizontal Line** Ensure that all pixels from the original horizontal line from the input grid are set to color 0 (white).
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

def get_bounding_box(objects):
    """Calculates the bounding box of a list of objects."""
    if not objects:
        return None  # Handle empty object list
    min_row = min(px[0] for obj in objects for px in obj)
    max_row = max(px[0] for obj in objects for px in obj)
    min_col = min(px[1] for obj in objects for px in obj)
    max_col = max(px[1] for obj in objects for px in obj)
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Find the horizontal line and its color
    horizontal_line_row, horizontal_line_color = find_horizontal_line(input_grid)

    # Find objects, excluding the horizontal line and background
    objects = find_objects(input_grid, horizontal_line_row, horizontal_line_color)

    # Mirror and recolor objects
    mirrored_objects = []
    for obj in objects:
        mirrored_pixels = mirror_object(obj, horizontal_line_row)
        mirrored_objects.append([(r, c, horizontal_line_color) for r, c in mirrored_pixels])

    # Calculate bounding box for the *mirrored* objects
    output_bbox = get_bounding_box(mirrored_objects)
    if output_bbox is None:  # Handle cases with no objects
       return np.zeros((0, 0), dtype=int).tolist()

    min_row, max_row, min_col, max_col = output_bbox
    
    # adjust rows if they extend past 0
    if min_row < 0:
       max_row = max_row - min_row
       min_row = 0

    # Create output grid based on bounding box
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)

    # Place mirrored objects into the output grid, adjusting for the new origin
    for obj in mirrored_objects:
        for r, c, color in obj:
            if r >= 0:  # only place if row is not negative from mirroring
               output_grid[r - min_row, c - min_col] = color

    return output_grid.tolist()