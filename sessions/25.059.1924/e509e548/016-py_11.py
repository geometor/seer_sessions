"""
The transformation rule is as follows:

1. Locate all green (3) pixels in the input grid.
2. Transform by position: 
    - Replace green pixels with magenta (6) if in the top left
    - Replace green pixels with blue (1) if bottom left or top right.
    - Replace green pixels with red (2) if bottom right
"""

import numpy as np

def get_connected_components(grid, color):
    """
    Finds connected components of a specific color in the grid.
    Uses a simple flood-fill algorithm.
    """
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def flood_fill(row, col, component):
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
        component.append((row, col))
        flood_fill(row + 1, col, component)
        flood_fill(row - 1, col, component)
        flood_fill(row, col + 1, component)
        flood_fill(row, col - 1, component)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                component = []
                flood_fill(row, col, component)
                components.append(component)
    return components

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find connected components of green pixels
    green_components = get_connected_components(input_grid, 3)

    # Iterate over each component and determine replacement color based on position.

    for component in green_components:
       
        # Find bounding box.
        min_row = min(component, key=lambda p: p[0])[0]
        max_row = max(component, key=lambda p: p[0])[0]
        min_col = min(component, key=lambda p: p[1])[1]
        max_col = max(component, key=lambda p: p[1])[1]
        
        center_row = (min_row + max_row) / 2
        center_col = (min_col + max_col) / 2

        # Determine the section based on the overall bounding box of green.
        overall_min_row = min([c[0] for comp in green_components for c in comp])
        overall_max_row = max([c[0] for comp in green_components for c in comp])
        overall_min_col = min([c[1] for comp in green_components for c in comp])
        overall_max_col = max([c[1] for comp in green_components for c in comp])

        overall_center_row = (overall_min_row + overall_max_row) / 2
        overall_center_col = (overall_min_col + overall_max_col) / 2
        
        
        for row, col in component:
            if row <= overall_center_row and col <= overall_center_col :
                output_grid[row, col] = 6
            elif (row > overall_center_row and col <= overall_center_col) or (row <= overall_center_row and col > overall_center_col) :
                output_grid[row, col] = 1
            else: # row > overall_center_row and col > overall_center_col:
                output_grid[row, col] = 2

    return output_grid