"""
1.  **Locate Red Pixels:** Identify all pixels colored red (value 2) within the input grid.

2.  **Initiate Flood Fill:** For each red pixel, perform a flood fill operation using yellow (value 4).

3.  **Fill Propagation:** The flood fill extends outwards from the starting red pixel in all eight directions: horizontally, vertically, and diagonally.

4.  **Fill Termination:** The flood fill in a given direction stops when it encounters a pixel that is not colored white (0) or red (2).
"""

import numpy as np
from collections import deque

def get_red_pixels(grid):
    """
    Finds the coordinates of all red pixels in the grid.
    """
    red_pixels = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_idx, col_idx))
    return red_pixels

def flood_fill(grid, start_row, start_col):
    """
    Performs a flood fill operation starting from a given pixel.
    """
    rows, cols = grid.shape
    queue = deque([(start_row, start_col)])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    while queue:
        row, col = queue.popleft()

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row, new_col] == 0 or grid[new_row, new_col] == 2:
                    if grid[new_row,new_col] != 4: #don't re-add to the queue if already yellow
                        grid[new_row, new_col] = 4
                        queue.append((new_row, new_col))


def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)
    
    # Perform flood fill for each red pixel
    for row, col in red_pixels:
        flood_fill(output_grid, row, col)

    return output_grid