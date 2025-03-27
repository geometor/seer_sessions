"""
The output grid is a single column of black (0) pixels. The height of the output grid is determined by counting the number of contiguous blocks of gray (5) pixels in the input grid. Contiguous blocks are groups of gray pixels that touch either directly or diagonally.
"""

import numpy as np

def count_contiguous_blocks(grid, color):
    """Counts contiguous blocks of a specified color in a grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    count = 0

    def dfs(row, col):
        """Depth-first search to explore a contiguous block."""
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row, col] or grid[row, col] != color:
            return
        visited[row, col] = True
        # Explore all 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                dfs(row + dr, col + dc)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == color and not visited[row, col]:
                dfs(row, col)
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid into an output grid based on the number of contiguous gray blocks.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Count the number of contiguous gray (5) blocks.
    num_blocks = count_contiguous_blocks(input_grid, 5)

    # Create an output grid that is a single column with a height equal to the number of blocks.
    output_grid = np.zeros((num_blocks, 1), dtype=int)

    # Fill all cells of the output grid with black (0). (Already done by np.zeros)

    return output_grid