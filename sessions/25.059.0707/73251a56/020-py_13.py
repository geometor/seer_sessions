"""
Removes white pixels (0) from within shapes, replacing them with the shape's color. The background color is determined as the most frequent color on the grid's edges.  Shapes are contiguous regions of non-background color.
"""

import numpy as np
from collections import Counter

def find_background_color(grid):
    """Finds the most frequent color on the edges of the grid."""
    edge_pixels = []
    rows, cols = grid.shape
    edge_pixels.extend(grid[0, :])  # Top row
    edge_pixels.extend(grid[rows - 1, :])  # Bottom row
    edge_pixels.extend(grid[:, 0])  # Left column
    edge_pixels.extend(grid[:, cols - 1])  # Right column
    color_counts = Counter(edge_pixels)
    return color_counts.most_common(1)[0][0]

def find_all_shapes(grid, background_color):
    """Finds all contiguous non-background shapes."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shapes = []

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, shape_color, current_shape):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != shape_color:
            return
        visited[r, c] = True
        current_shape.append((r, c))
        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, shape_color, current_shape)
        dfs(r - 1, c, shape_color, current_shape)
        dfs(r, c + 1, shape_color, current_shape)
        dfs(r, c - 1, shape_color, current_shape)


    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != background_color and not visited[r,c]:
              shape_color = grid[r,c]
              current_shape = []
              dfs(r, c, shape_color, current_shape)
              shapes.append((shape_color, current_shape))

    return shapes

def transform(input_grid):
    """
    Removes white (0) pixels from within shapes and replaces them with the shape's color.

    Args:
        input_grid: The input grid as a 2D numpy array.

    Returns:
        The transformed grid as a 2D numpy array.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # 1. Identify the background color.
    background_color = find_background_color(input_grid)

    # 2. Identify all shapes.
    shapes = find_all_shapes(input_grid, background_color)

    # 3. Replace white pixels inside each shape with the shape's color.
    for shape_color, shape_pixels in shapes:
        for r, c in shape_pixels:
            if input_grid[r, c] == 0:  # Check against the *input* grid
                output_grid[r, c] = shape_color

    return output_grid