"""
1.  **Identify Azure Border:** Locate all azure (8) pixels. These form the boundary.
2.  **Locate Green Pixels:** Within the grid bounded by azure, locate all green (3) pixels.
3.  **Flood Fill:** For *each* green pixel:
    *   Perform a flood fill operation using red (2) as the fill color.
    *   The flood fill should stop when it encounters an azure (8) pixel or a red(2) pixel.
    * The fill should propagate in all four cardinal directions (up, down, left, right).
4.  **Result:** The final output grid consists of the original azure border, the green pixels, and red pixels resulting from the flood fill operations.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return list(zip(*np.where(grid == color)))

def constrained_flood_fill(grid, start_coord, fill_color, border_color, stop_color):
    """
    Performs a constrained flood fill, starting from a single coordinate.
    """
    rows, cols = grid.shape
    new_grid = np.copy(grid)
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def fill(r, c):
        if (r, c) in visited or not is_valid(r, c) or new_grid[r, c] == border_color or new_grid[r, c] == stop_color:
            return

        visited.add((r, c))
        new_grid[r, c] = fill_color

        fill(r + 1, c)
        fill(r - 1, c)
        fill(r, c + 1)
        fill(r, c - 1)
    
    fill(start_coord[0], start_coord[1])
    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find azure border pixels
    border_pixels = find_pixels_by_color(output_grid, 8)

    # Find green pixels
    green_pixels = find_pixels_by_color(output_grid, 3)
    
    # Perform flood fill for each green pixel
    for green_pixel in green_pixels:
        output_grid = constrained_flood_fill(output_grid, green_pixel, 2, 8, 2)

    return output_grid