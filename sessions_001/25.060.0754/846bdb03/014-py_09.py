"""
Transforms the input grid by identifying objects of color 3 (green), 8 (azure), and 4 (yellow) and arranging them within a new grid.
The output grid's dimensions are determined by finding the top-most and bottom-most rows, and left-most and right-most columns, containing these colored objects.
Yellow (4) pixels mark the top-left and bottom-left corners of the new grid. The green (3) object is placed one column to the right of the top-left yellow pixel.
The azure (8) object is placed one row below the top-left yellow pixel.
"""

import numpy as np

def find_objects(grid, colors):
    """
    Finds objects of specified colors in the grid.
    Returns a dictionary where keys are colors and values are lists of object coordinates.
    """
    objects = {}
    for color in colors:
        objects[color] = []
        visited = np.zeros_like(grid, dtype=bool)
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color and not visited[r, c]:
                    object_coords = []
                    stack = [(r, c)]
                    while stack:
                        cr, cc = stack.pop()
                        if 0 <= cr < rows and 0 <= cc < cols and grid[cr, cc] == color and not visited[cr, cc]:
                            visited[cr, cc] = True
                            object_coords.append((cr, cc))
                            stack.extend([(cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)])
                    objects[color].append(object_coords)
    return objects

def get_bounding_rows_cols(objects):
    """
    Calculates the top-most and bottom-most rows, and left-most and right-most columns
    containing objects of colors 3, 4, and 8.
    Returns (min_row, max_row, min_col, max_col).
    """
    all_coords = []
    for color in [3, 4, 8]:
        if color in objects:
            for obj in objects[color]:
                all_coords.extend(obj)

    if not all_coords:
        return (0, 0, 0, 0)

    min_row = min(coord[0] for coord in all_coords)
    max_row = max(coord[0] for coord in all_coords)
    min_col = min(coord[1] for coord in all_coords)
    max_col = max(coord[1] for coord in all_coords)

    return (min_row, max_row, min_col, max_col)

def get_object_top_left(object_coords):
    """Returns the top-left coordinate of an object."""
    if not object_coords:
        return None
    min_row = min(coord[0] for coord in object_coords)
    min_col = min(coord[1] for coord in object_coords)
    return (min_row, min_col)

def transform(input_grid):
    # Find objects of interest (colors 3, 8, and 4)
    objects = find_objects(input_grid, [3, 8, 4])

    # Determine output grid boundaries
    min_row, max_row, min_col, max_col = get_bounding_rows_cols(objects)
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 2  # Plus two for the extra column

    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place yellow markers at the top-left and bottom-left corners
    output_grid[0, 0] = 4
    output_grid[output_height - 1, 0] = 4

    # Position green object (3)
    green_objects = objects.get(3, [])
    for obj in green_objects:
        obj_top_left = get_object_top_left(obj)
        if obj_top_left:
            row_offset = obj_top_left[0] - min_row
            col_offset = obj_top_left[1] - min_col
            for r, c in obj:
                out_r = r - row_offset
                out_c = c - col_offset + 1  # Shift one column right
                if 0 <= out_r < output_height and 0 <= out_c < output_width:
                    output_grid[out_r, out_c] = 3

    # Position azure object (8)
    azure_objects = objects.get(8, [])
    for obj in azure_objects:
        obj_top_left = get_object_top_left(obj)
        if obj_top_left:
            row_offset = obj_top_left[0] - min_row
            col_offset = obj_top_left[1] - min_col

            for r,c in obj:
              out_r = r - row_offset + 1 # Shift one row down
              out_c = c - col_offset
              if 0 <= out_r < output_height and 0 <= out_c < output_width:
                output_grid[out_r, out_c] = 8

    return output_grid