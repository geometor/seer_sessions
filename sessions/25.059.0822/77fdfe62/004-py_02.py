"""
The input grid is transformed into a smaller output grid by extracting the corner pixels of distinct objects within the input grid.
Objects are contiguous regions of the same color. Corner pixels of these objects are identified and their colors are placed into corresponding
quadrants in the output grid, maintaining relative positioning. Empty regions in the input result in empty (white, 0) cells in the output.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def find_corners(object_coords):
    """
    Finds the corner pixels of an object.
    Returns a dictionary with keys 'tl', 'tr', 'bl', 'br' representing top-left, top-right, bottom-left, and bottom-right corners.
    """
    min_row = min(r for r, _ in object_coords)
    max_row = max(r for r, _ in object_coords)
    min_col = min(c for _, c in object_coords)
    max_col = max(c for _, c in object_coords)

    corners = {
        'tl': (min_row, min_col),
        'tr': (min_row, max_col),
        'bl': (max_row, min_col),
        'br': (max_row, max_col),
    }
    return corners


def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows // 2, input_cols // 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Find distinct objects
    objects = find_objects(input_grid)

    # Find corners for each object
    for obj in objects:
        corners = find_corners(obj)

        # Place corner colors into output grid
        for corner_type, (r, c) in corners.items():
            color = input_grid[r, c]

            # Determine quadrant in output grid
            if corner_type == 'tl':
                out_r, out_c = r // 2, c // 2

            elif corner_type == 'tr':
                out_r, out_c = r // 2 , (c - output_cols) //2 + output_cols//2

            elif corner_type == 'bl':
                out_r, out_c = (r- output_rows) // 2 + output_rows//2, c // 2

            elif corner_type == 'br':
                out_r, out_c = (r- output_rows)// 2 + output_rows//2 , (c - output_cols) //2 + output_cols//2

            if 0 <= out_r < output_rows and 0 <= out_c < output_cols:
                output_grid[out_r, out_c] = color

    return output_grid