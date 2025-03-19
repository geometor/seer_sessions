"""
Extracts colored rectangular objects from the input grid, converts them to horizontal bars, and arranges them in a new grid, maintaining their colors and the number of non-zero pixels.
"""

import numpy as np

def _find_objects(grid):
    """Finds contiguous blocks of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def _dfs(row, col, color, obj_coords):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row, col] != color:
            return
        visited.add((row, col))
        obj_coords.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            _dfs(row + dr, col + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_coords = []
                _dfs(r, c, grid[r, c], obj_coords)
                if obj_coords:
                  min_r = min(coord[0] for coord in obj_coords)
                  min_c = min(coord[1] for coord in obj_coords)
                  max_r = max(coord[0] for coord in obj_coords)
                  max_c = max(coord[1] for coord in obj_coords)

                  objects.append({
                      'color': grid[r, c],
                      'coords': obj_coords,
                      'top_left':(min_r,min_c),
                      'rows': max_r-min_r+1,
                      'cols': max_c-min_c+1
                  })
    return objects


def transform(input_grid):
    # Find objects in the input grid
    objects = _find_objects(np.array(input_grid))

    # Initialize the output grid (4x4 based on the example)
    output_grid = np.zeros((4, 4), dtype=int)

    # Sort objects based on the provided example order: Azure, Red, Green, Blue
    # We determine order based on the top_left position of the original object
    objects.sort(key=lambda obj: (obj['top_left'][0], obj['top_left'][1]))

    # Place objects into the output grid
    row_start = 0
    col_start = 0

    for obj in objects:
        size = len(obj['coords'])

        # make the objects horizontal
        if obj['rows'] > obj['cols']: # vertical in the input
            for i in range(size):
                output_grid[row_start, col_start + i] = obj['color']
            row_start += 1

        elif obj['rows'] < obj['cols']: # Horizontal in input
             for i in range(size):
                output_grid[row_start, col_start + i] = obj['color']
             row_start += 1
        else: # square case in input
            for i in range(size):
                output_grid[row_start, col_start + i] = obj['color']
            row_start += 1

        if row_start > 3:
           col_start +=2
           row_start = 0

    return output_grid.tolist()