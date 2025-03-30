import numpy as np
from typing import List, Tuple

"""
The transformation identifies green (3) and red (2) pixels within the input grid.
It then removes these green and red pixels from the grid, setting their corresponding locations in the output grid to the background color (white, 0).
Additionally, any azure (8) pixels that are directly adjacent (horizontally or vertically) to a green pixel in the input grid are also removed (set to white, 0) in the output grid.
All other pixels retain their original colors.
"""

def find_pixels_by_color(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Removes green (3) and red (2) pixels, and any azure (8) pixels
    directly adjacent (N, S, E, W) to the green pixels.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # Find locations of green and red pixels
    green_pixels = find_pixels_by_color(input_array, 3)
    red_pixels = find_pixels_by_color(input_array, 2)

    # Remove red pixels
    for r, c in red_pixels:
        output_array[r, c] = 0

    # Process green pixels and their adjacent azure neighbors
    for r_green, c_green in green_pixels:
        # Remove the green pixel itself
        output_array[r_green, c_green] = 0

        # Check neighbours (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_green + dr, c_green + dc

            # Check if neighbour is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbour in the *original* grid was azure
                if input_array[nr, nc] == 8:
                    # Remove the adjacent azure pixel in the output grid
                    output_array[nr, nc] = 0

    return output_array.tolist()