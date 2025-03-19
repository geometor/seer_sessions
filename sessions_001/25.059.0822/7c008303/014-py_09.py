"""
The transformation extracts all blue, red, and yellow objects from the input grid and places them into the output grid. The output grid's size is determined by a bounding box around the selected objects, with a one-pixel black border added on all sides. Objects of other colors are ignored.
"""

import numpy as np

def find_objects(grid, colors):
    """Find objects of specified colors in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] in colors:
                obj = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    obj.append((curr_r, curr_c))

                    neighbors = [
                        (curr_r - 1, curr_c),
                        (curr_r + 1, curr_c),
                        (curr_r, curr_c - 1),
                        (curr_r, curr_c + 1),
                    ]
                    for nr, nc in neighbors:
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and not visited[nr, nc]
                            and grid[nr, nc] == grid[r, c]
                        ):
                            stack.append((nr, nc))
                            visited[nr, nc] = True
                objects.append(obj)
    return objects

def get_bounding_box(objects):
    """Calculates the bounding box for a list of objects."""
    if not objects:
        return (0, 0, 0, 0)

    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for obj in objects:
        for r, c in obj:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)

    return (min_r, min_c, max_r, max_c)

def transform(input_grid):
    input_grid = np.array(input_grid)

    # 1. Identify Objects: Find all blue, red, and yellow objects.
    blue_objects = find_objects(input_grid, [1])
    red_objects = find_objects(input_grid, [2])
    yellow_objects = find_objects(input_grid, [4])

    # 2. Select Objects: All blue, red and yellow
    selected_objects = blue_objects + red_objects + yellow_objects

    # 3. Determine Output Size: bounding box + 1 padding on all sides
    min_r, min_c, max_r, max_c = get_bounding_box(selected_objects)
    output_rows = max_r - min_r + 3
    output_cols = max_c - min_c + 3

    # 4. Create Output Grid: Initialize with black (0).
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # 5. Place Objects: Copy objects to output grid, adjust for padding.
    row_offset = 1 - min_r
    col_offset = 1 - min_c

    for obj in blue_objects:
        for r, c in obj:
            output_grid[r + row_offset, c + col_offset] = 1
    for obj in red_objects:
        for r, c in obj:
            output_grid[r + row_offset, c + col_offset] = 2
    for obj in yellow_objects:
        for r, c in obj:
            output_grid[r + row_offset, c + col_offset] = 4

    return output_grid