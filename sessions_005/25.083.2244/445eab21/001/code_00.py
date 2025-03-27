"""
1.  **Locate Target Object:** Examine the top half of the input grid. Find the largest contiguous block (object) of pixels that share the same non-black color.
2.  **Isolate Color:** Determine the color value of the target object identified in step 1.
3.  **Create Output:** Construct a 2x2 output grid. Fill all cells of this output grid with the color value identified in step 2.
4. Ignore the bottom half of the input.
"""

import numpy as np

def find_largest_object(grid):
    """Finds the largest contiguous object in a grid."""
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0
    max_color = 0

    def dfs(row, col, color):
        """Depth-first search to find contiguous regions."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return 0
        visited[row, col] = True
        return (
            1
            + dfs(row + 1, col, color)
            + dfs(row - 1, col, color)
            + dfs(row, col + 1, color)
            + dfs(row, col - 1, color)
        )

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] != 0:
                color = grid[i, j]
                size = dfs(i, j, color)
                if size > max_size:
                    max_size = size
                    max_color = color
    return max_color, max_size


def transform(input_grid):
    # Split the grid in half
    half_height = input_grid.shape[0] // 2
    top_half = input_grid[:half_height, :]

    # Find the largest object in the top half
    target_color, _ = find_largest_object(top_half)


    # Create a 2x2 output grid filled with the target color
    output_grid = np.full((2, 2), target_color, dtype=int)

    return output_grid