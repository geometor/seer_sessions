"""
The transformation rule identifies the presence of any single-pixel object within the input grid. If such an object exists, the entire column containing that single-pixel object in the input grid is filled with the color of that pixel in the output grid. The transformation replicates this for all single pixels in the input grid.
"""

import numpy as np

def get_objects(grid: np.ndarray) -> list:
    """
    Identifies contiguous objects (regions of the same color) within a grid.
    Returns a list of object masks.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

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
                color = grid[row, col]
                current_object = []
                dfs(row, col, color, current_object)
                if current_object:
                    mask = np.zeros_like(grid, dtype=bool)
                    for r, c in current_object:
                        mask[r, c] = True
                    objects.append(mask)
    return objects
def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find single-pixel objects
    objects = get_objects(input_grid)
    single_pixel_objects = [obj for obj in objects if np.sum(obj) == 1]

    # change output pixels
    for obj_mask in single_pixel_objects:
        # Get the row and column of the single pixel
        row, col = np.where(obj_mask)
        row, col = row[0], col[0]

        # Get the color of the pixel
        color = input_grid[row, col]

        # Fill the entire column with that color
        output_grid[:, col] = color
    return output_grid