"""
1.  Identify Contiguous Shapes: Find all distinct, contiguous regions (shapes) of the same color within the input grid. A contiguous region is a group of pixels of the same color that are directly adjacent (up, down, left, or right – not diagonally).

2. Select shape(s):
   - if one shape is contained within another, select the inner shape
   - if no shapes are contained, select shape(s) by color. If only one shape of that color exists, it is the selection.

3.  Extract Selected Shape: Create the output grid by copying *only* the pixels of the selected shape(s). The output grid should be sized to perfectly fit the selected shape(s), with no extra rows or columns.
"""

import numpy as np

def find_shapes(grid):
    """Finds all contiguous shapes in a grid."""
    shapes = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_shape):
        if not is_valid(r, c) or grid[r][c] != color or (r, c) in visited:
            return

        visited.add((r, c))
        current_shape.append((r, c))

        # Check neighbors (up, down, left, right)
        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            dfs(nr, nc, color, current_shape)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_shape = []
                dfs(r, c, grid[r][c], current_shape)
                if current_shape:
                    shapes.append({
                        'color': grid[r][c],
                        'pixels': current_shape
                    })
    return shapes

def is_contained(inner_shape, outer_shape):
    """Checks if inner_shape is completely inside outer_shape."""
    inner_pixels = set(inner_shape['pixels'])
    outer_pixels = set(outer_shape['pixels'])
    return inner_pixels.issubset(outer_pixels) and len(inner_pixels) < len(outer_pixels)

def extract_shape(grid, shape):
    """Extracts a shape from the grid and returns it as a new grid."""
    min_r = min(p[0] for p in shape['pixels'])
    max_r = max(p[0] for p in shape['pixels'])
    min_c = min(p[1] for p in shape['pixels'])
    max_c = max(p[1] for p in shape['pixels'])

    output_grid = []
    for r in range(min_r, max_r + 1):
        row = []
        for c in range(min_c, max_c + 1):
            row.append(grid[r][c])
        output_grid.append(row)
    return output_grid

def transform(input_grid):
    # Find all contiguous shapes.
    shapes = find_shapes(input_grid)

    # Check for contained shapes.
    for i in range(len(shapes)):
        for j in range(len(shapes)):
            if i != j and is_contained(shapes[i], shapes[j]):
                return extract_shape(input_grid, shapes[i])

    # If no contained shapes, select by color (blue = 1 in this task).
    blue_shapes = [shape for shape in shapes if shape['color'] == 1]
    if len(blue_shapes) == 1:
        return extract_shape(input_grid, blue_shapes[0])

    return []