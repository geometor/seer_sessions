"""
The transformation identifies connected components of green pixels. Single-pixel components are recolored blue, while multi-pixel components are recolored magenta.  The background remains unchanged.
"""

import numpy as np

def find_connected_components(grid, color):
    """
    Finds connected components of a specific color in a grid.

    Args:
        grid: The input grid (2D numpy array).
        color: The color to find connected components of.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a connected component.
    """
    visited = set()
    components = []

    def dfs(row, col, current_component):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_component.add((row, col))
        # Check adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_component)
        dfs(row - 1, col, current_component)
        dfs(row, col + 1, current_component)
        dfs(row, col - 1, current_component)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_component = set()
                dfs(row, col, current_component)
                components.append(current_component)
    return components

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    green_components = find_connected_components(input_grid, 3)  # Find green components

    for component in green_components:
        if len(component) == 1:
            # Single pixel component, change to blue (1)
            row, col = list(component)[0]
            output_grid[row, col] = 1
        else:
            # Multiple pixels, change to magenta (6)
            for row, col in component:
                output_grid[row, col] = 6
    return output_grid