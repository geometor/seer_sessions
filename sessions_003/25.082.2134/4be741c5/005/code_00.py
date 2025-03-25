"""
Identifies the unique colors in the input grid based on the largest connected component of each color, and outputs them in a single column in order of their first appearance in the input grid.
"""

import numpy as np

def get_largest_connected_component(grid, color):
    """
    Finds the largest connected component of a given color in the grid.
    Uses Depth First Search (DFS).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    max_component = []

    def dfs(row, col, current_component):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return

        visited[row, col] = True
        current_component.append((row, col))

        # Explore adjacent cells
        dfs(row + 1, col, current_component)
        dfs(row - 1, col, current_component)
        dfs(row, col + 1, current_component)
        dfs(row, col - 1, current_component)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_component = []
                dfs(r, c, current_component)
                if len(current_component) > len(max_component):
                    max_component = current_component

    return max_component

def transform(input_grid):
    # Convert input grid to numpy array
    grid = np.array(input_grid)
    rows, cols = grid.shape
    
    # Find unique colors and their order of first appearance, considering only the largest components
    unique_colors = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r,c]
            if color not in unique_colors:
                component = get_largest_connected_component(grid, color)
                if any([(r,c) in component for r in range(rows) for c in range(cols)]):
                    unique_colors.append(color)

    # Create output grid (N x 1)
    output_grid = np.zeros((len(unique_colors), 1), dtype=int)

    # Fill output grid with ordered unique colors
    for i, color in enumerate(unique_colors):
        output_grid[i, 0] = color

    return output_grid.tolist()