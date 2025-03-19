"""
1.  **Identify the Red Shape:** Locate all pixels with the value 2 (red). These pixels form a connected, cross-like, or branching structure.

2.  **Identify the White Region to be Transformed** Find a region of white pixels (0) which is located "under", or within a closed boundary of, the red structure.

3. **Fill with Blue:** Change the color of the identified white region to blue (1)

4.  **Conditional Red to Azure:** Any red pixel (2) which is one pixel away (8-connectivity or diagonal) of the blue region in the horizontal or diagonal direction is turned to azure (8).
"""

import numpy as np

def find_connected_components(grid, color):
    """Finds connected components of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(r, c, current_component):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_component.append((r, c))
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(r + dr, c + dc, current_component)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_component = []
                dfs(r, c, current_component)
                components.append(current_component)
    return components

def is_adjacent(grid, r, c, color):
    """Checks if a cell is adjacent to a cell of a given color."""

    for dr in [-1,0,1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc
            if( 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == color):
                return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = input_grid.copy()
    red_components = find_connected_components(input_grid, 2)
    if not red_components: #handle edge case of missing components
        return output_grid
        
    red_shape = red_components[0]

    # Find min and max row of the red shape
    min_red_row = min(r for r, c in red_shape)
    max_red_row = max(r for r, c in red_shape)


    # Fill white region below red shape with blue (1)
    for r in range(max_red_row + 1, output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] == 0:
                output_grid[r,c] = 1

    #convert some red to azure
    for r, c in red_shape:
        if is_adjacent(output_grid, r,c, 1):
            output_grid[r,c] = 8

    return output_grid