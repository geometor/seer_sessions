"""
1.  **Copy:** The 2x2 green block is copied from the input to the output, maintaining its position relative to other objects.
2.  **Mirror Orange (7):** The shape formed by orange pixels (7) is mirrored across the main diagonal (y=x).
3.  **Mirror Azure (8):** The shape formed by azure pixels (8) is mirrored across a vertical line that bisects the azure shape, and does not include cells where a color 8 exists in the input.
"""

import numpy as np

def get_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects


def transform(input_grid):
    """Transforms the input grid according to the rules."""
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Copy green blocks (color 3) - assumes relative position means we can copy directly
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 3:
                output_grid[r,c] = 3

    # Mirror orange (color 7)
    orange_objects = get_objects(input_grid, 7)
    for obj in orange_objects:
        for r, c in obj:
            output_grid[c, r] = 7

    # Mirror azure (color 8)
    azure_objects = get_objects(input_grid, 8)
    for obj in azure_objects:
        # Find the center of the object for mirroring
        coords = np.array(obj)
        min_c = np.min(coords[:, 1])
        max_c = np.max(coords[:, 1])
        center_c = (min_c + max_c) / 2

        for r, c in obj:
            # reflect across the center axis
            mirrored_c = int(2 * center_c - c)
            if 0 <= mirrored_c < cols:
                # only fill if there was not already a color 8 there
                if input_grid[r, mirrored_c] != 8:
                    output_grid[r, mirrored_c] = 8

    return output_grid