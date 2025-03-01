"""
1.  **Identify and Remove Gray:** Locate all gray (value 5) pixels in the input grid and remove them, setting those pixels to 0 (white).
2.  **Identify Blue Pixels:** Find all blue pixels (value 1).
3.  **Expand Blue:** For *each* blue pixel, expand it to fill all connected (horizontally and vertically) white pixels (value 0) that replace the gray. The expansion continues until it encounters a pixel that is not 0 (white).
4.  **Preserve Other Colors:** All other colored pixels (e.g., red, green) remain in their original positions and retain their original values.
"""

import numpy as np
from collections import deque

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def expand_blue(grid, start_x, start_y):
    """Expands the blue pixel from (start_x, start_y) to fill connected 0s."""
    queue = deque([(start_x, start_y)])
    while queue:
        x, y = queue.popleft()
        if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1] and grid[x, y] == 0:
            grid[x, y] = 1  # Fill with blue
            # Add adjacent cells to the queue
            queue.append((x + 1, y))
            queue.append((x - 1, y))
            queue.append((x, y + 1))
            queue.append((x, y - 1))


def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Remove gray (5) pixels, converting them to white (0).
    gray_pixels = find_pixels_by_color(input_grid, 5)
    for x, y in gray_pixels:
        output_grid[x, y] = 0

    # Find all blue (1) pixels.
    blue_pixels = find_pixels_by_color(input_grid, 1)

    # Expand each blue pixel. Use the output_grid for expansion.
    for x, y in blue_pixels:
        expand_blue(output_grid, x, y)


    return output_grid