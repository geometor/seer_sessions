"""
The program identifies connected components (objects) of non-zero pixels in the input grid. Each object's shape and size are preserved. The objects are then arranged in a specific order in the output. The objects are ordered according to their colors (blue, azure, green, red, yellow), then by their top-to-bottom, left-to-right position in the input grid. The output grid is 4x4, and objects are placed in a 2x2 arrangement: top-left, top-right, bottom-left, bottom-right.
"""

import numpy as np

def get_connected_components(grid):
    """
    Finds connected components of non-zero pixels in a grid.
    Returns a list of tuples: (color, [(row, col), ...])
    """
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(row, col, component):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] == 0):
            return
        visited[row, col] = True
        component.append((row, col))
        dfs(row + 1, col, component)
        dfs(row - 1, col, component)
        dfs(row, col + 1, component)
        dfs(row, col - 1, component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                component = []
                dfs(r, c, component)
                components.append((grid[r, c], component))
    return components

def get_top_left(component):
    """
    Returns the top-left corner coordinates (row, col) of a component.
    """
    min_row = min(r for r, c in component)
    min_col = min(c for r, c in component)
    return (min_row, min_col)

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    components = get_connected_components(input_grid)

    # Sort components based on color priority, then top-to-bottom, left-to-right.
    color_priority = {1: 0, 8: 1, 3: 2, 2: 3, 4:4}
    def get_priority(component_tuple):
        color = component_tuple[0]
        top_left = get_top_left(component_tuple[1])
        return (color_priority.get(color, 99), top_left[0], top_left[1])

    sorted_components = sorted(components, key=get_priority)

    output_grid = np.zeros((4, 4), dtype=int)
    output_positions = [(0, 0), (0, 2), (2, 0), (2, 2)]

    for i, (color, component) in enumerate(sorted_components):
        if i < 4:
            output_row, output_col = output_positions[i]
            input_row, input_col = get_top_left(component)

            for r, c in component:
                row_offset = r - input_row
                col_offset = c - input_col
                
                orow = output_row + row_offset
                ocol = output_col + col_offset

                if 0 <= orow < 4 and 0 <= ocol < 4:
                    output_grid[orow, ocol] = color
    return output_grid