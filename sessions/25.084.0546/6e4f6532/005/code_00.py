"""
The transformation identifies large background objects (color 5 in Example 1, color 1 in Example 2) and applies complex, position-dependent color changes within their bounding boxes.  The exact transformation logic is still unclear, but it differs between examples. Frame objects (colors 1, 2, 4, and 7) are generally preserved. Smaller, enclosed objects have inconsistent behavior.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color in the grid.
    Returns a list of objects, each represented as a dictionary.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, object_coords):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        object_coords.append((row, col))
        dfs(row + 1, col, color, object_coords)
        dfs(row - 1, col, color, object_coords)
        dfs(row, col + 1, color, object_coords)
        dfs(row, col - 1, color, object_coords)

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                object_coords = []
                dfs(row, col, grid[row, col], object_coords)
                if object_coords:
                    objects.append({
                        "color": grid[row, col],
                        "coords": object_coords,
                    })
    return objects

def get_bounding_box(coords):
    """
    Returns the bounding box of a list of coordinates.
    """
    min_row = min(c[0] for c in coords)
    max_row = max(c[0] for c in coords)
    min_col = min(c[1] for c in coords)
    max_col = max(c[1] for c in coords)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    input_objects = find_objects(input_grid)

    for obj in input_objects:
        bbox = get_bounding_box(obj['coords'])
        min_row, min_col, max_row, max_col = bbox
        height = max_row - min_row + 1
        width = max_col - min_col + 1

        if obj['color'] == 5 and height > 5 and width > 5:  # Example 1 Gray Background
            # Apply a simplified transformation - a placeholder for the complex logic
            for r in range(min_row + 2, max_row -1):
                for c in range(min_col + 2, max_col - 1):
                    output_grid[r, c] = 8  # Fill with gray (8)

            output_grid[min_row+2, max_col-2] = 2

        elif obj['color'] == 1 and height > 5 and width > 5: # Example 2, Blue background
             # Apply a different simplified transformation - a placeholder for the complex logic
            for r in range(min_row + 2, max_row-1):
                for c in range(min_col + 2, max_col -1):
                    output_grid[r, c] = 8  # Fill with gray (8)

            output_grid[min_row + 2, min_col + 2] = 4

    return output_grid.tolist()