"""
The transformation rule is to isolate and extract the largest yellow shape from the input grid.
"""

import numpy as np

def find_shapes(grid):
    # Find all contiguous shapes in a grid
    shapes = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, shape_color, current_shape):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != shape_color:
            return
        visited.add((r, c))
        current_shape.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, shape_color, current_shape)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                shape_color = grid[r, c]
                if shape_color != 0: # don't care about blank
                   current_shape = []
                   dfs(r, c, shape_color, current_shape)
                   shapes.append((shape_color, current_shape))
    return shapes

def extract_shape(grid, shape_pixels):
    # Extract a shape defined by its pixels
    min_r = min(r for r, c in shape_pixels)
    max_r = max(r for r, c in shape_pixels)
    min_c = min(c for r, c in shape_pixels)
    max_c = max(c for r, c in shape_pixels)
    extracted_grid = grid[min_r:max_r + 1, min_c:max_c + 1]
    return extracted_grid

def transform(input_grid):
    # Find all shapes in the input grid
    shapes = find_shapes(input_grid)

    # Find yellow shape
    yellow_shapes = [shape for color, shape in shapes if color == 4]

    #select yellow shape
    target_shape_pixels = []
    if (len(yellow_shapes) > 0):
        target_shape_pixels = yellow_shapes[0]  # just select the first one

    if (len(target_shape_pixels) == 0):
        # return zero grid since no yellow
        return np.zeros((1,1), dtype=int)


    # Extract the target shape
    output_grid = extract_shape(input_grid, target_shape_pixels)

    return output_grid