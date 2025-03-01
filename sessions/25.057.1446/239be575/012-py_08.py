"""
Scales down objects in a grid by a factor of 3, preserving their colors and relative positions.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in the grid using bounding boxes.
    Returns a list of objects, where each object is a dictionary containing:
        'bounding_box': (min_row, min_col, max_row, max_col)
        'color': color of the object
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                current_object = []
                color = grid[row, col]
                dfs(row, col, color, current_object)
                if current_object:
                    min_row = min(p[0] for p in current_object)
                    min_col = min(p[1] for p in current_object)
                    max_row = max(p[0] for p in current_object)
                    max_col = max(p[1] for p in current_object)
                    objects.append({
                        'bounding_box': (min_row, min_col, max_row, max_col),
                        'color': color
                    })
    return objects

def scale_bounding_box(bounding_box, scale_factor):
    """Scales down a bounding box by a given factor."""
    min_row, min_col, max_row, max_col = bounding_box
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    scaled_width = max(1, int(width / scale_factor))  # Ensure at least 1
    scaled_height = max(1, int(height / scale_factor)) # Ensure at least 1
    return scaled_width, scaled_height


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects
    objects = get_objects(input_grid)

    # Scale factor
    scale_factor = 3

    # Scale and position objects
    for obj in objects:
        # Scale bounding box
        scaled_width, scaled_height = scale_bounding_box(obj['bounding_box'], scale_factor)

        # Determine top-left position of scaled object in the output grid.
        min_row, min_col, _, _ = obj['bounding_box']
        output_row = int(min_row / scale_factor)
        output_col = int(min_col / scale_factor)
        
        # Fill scaled object in output grid
        for r in range(scaled_height):
          for c in range(scaled_width):
            if output_row + r < output_grid.shape[0] and output_col + c < output_grid.shape[1]:
              output_grid[output_row + r, output_col + c] = obj['color']

    return output_grid