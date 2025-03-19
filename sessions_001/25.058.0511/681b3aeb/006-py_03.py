"""
1.  **Conceptual 3x3 Grid:** Conceptually divide the input grid into a 3x3 grid of equally sized regions. This division is not strictly based on exact pixel counts but rather a conceptual mapping.

2.  **Identify Colored Objects:** Identify all contiguous regions (objects) of non-white (non-zero) pixels within the input grid. Each object will have a single color.

3.  **Map Objects to Output:** For each identified object, determine which of the nine conceptual regions its *center of mass* or *representative point* (e.g., the top-leftmost pixel of the object, or average coordinate) falls within.

4.  **Populate Output:** Create a 3x3 output grid. For each of the nine regions, if an object's representative point falls within that region, place the object's color in the corresponding cell of the output grid. If multiple objects fall within the same region, prioritize according to a consistent rule. Since the provided examples show no overlaps in colors, use a first come approach. If no object falls within a region, the output cell remains 0 (white).
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        """Depth-first search to find connected components."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj_coords = []
                dfs(row, col, grid[row, col], obj_coords)
                objects.append({
                    'color': grid[row, col],
                    'coords': obj_coords
                })
    return objects

def get_representative_point(obj):
    """Gets the top-leftmost pixel of an object as its representative point."""
    return obj['coords'][0]

def transform(input_grid):
    # Initialize output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify colored objects
    objects = find_objects(input_grid)

    # Get input grid dimensions
    height, width = input_grid.shape

    # Calculate region boundaries (conceptual 3x3 grid)
    row_thirds = height / 3
    col_thirds = width / 3

    # Map objects to output grid
    for obj in objects:
        # Get representative point (top-leftmost pixel)
        row, col = get_representative_point(obj)

        # Determine the conceptual region (0-2 for rows and cols)
        region_row = min(int(row / row_thirds), 2)
        region_col = min(int(col / col_thirds), 2)

        # Populate output grid (first-come, first-served)
        if output_grid[region_row, region_col] == 0:
            output_grid[region_row, region_col] = obj['color']

    return output_grid