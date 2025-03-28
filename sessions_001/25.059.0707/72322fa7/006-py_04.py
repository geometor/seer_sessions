"""
1.  **Preservation:** Pixels with colors 3 (green) and 5 (gray) remain in their original positions and are not modified.
2.  **Color 8 (Azure) Mirroring:**  Pixels with color 8 (azure) create a mirrored copy of themselves on the opposite side of the grid's central column.
3.  **Color 6 (Magenta) Transformation and Mirroring:** Pixels with color 6 (magenta) first change their color to 8 (azure), and *then* create a mirrored copy of themselves (now as color 8) on the opposite side of the grid's central column.
4.  **Color 1 (Blue) Mirroring:** Pixels with color 1 (blue) create a mirrored copy of themselves on the opposite side of the grid's central column.
5.  **Mirror Axis:** The mirroring of pixels for colors 1, 6 and 8 occurs across the vertical axis defined by the center column of the input grid. The center column is determined by (number of columns - 1)/2
"""

import numpy as np

def find_pixels(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def mirror_pixel(grid, coord):
    """Mirrors a single pixel across a vertical axis derived from the input grid's overall shape."""
    rows, cols = grid.shape
    x, y = coord
    
    # central column.
    mirror_y = cols - 1 - y

    return (x, mirror_y)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # 1. Preservation of colors 3 and 5 (no change needed)

    # 2. Color 8 (Azure) Mirroring
    azure_pixels = find_pixels(input_grid, 8)
    for x, y in azure_pixels:
        mirrored_coord = mirror_pixel(output_grid, (x, y))
        output_grid[mirrored_coord] = 8

    # 3. Color 6 (Magenta) Transformation and Mirroring
    magenta_pixels = find_pixels(input_grid, 6)
    for x, y in magenta_pixels:
        output_grid[x, y] = 8  # Change to Azure
        mirrored_coord = mirror_pixel(output_grid, (x, y))
        output_grid[mirrored_coord] = 8

    # 4. Color 1 (Blue) Mirroring
    blue_pixels = find_pixels(input_grid, 1)
    for x, y in blue_pixels:
        mirrored_coord = mirror_pixel(output_grid, (x, y))
        output_grid[mirrored_coord] = 1

    return output_grid