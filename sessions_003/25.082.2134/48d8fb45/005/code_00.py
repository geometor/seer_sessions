"""
1.  **Identify Non-Black Pixels:** Locate all pixels within the input grid that are not black (color 0).
2.  **Determine Bounding Box:** Calculate the smallest rectangular bounding box that encompasses all identified non-black pixels.
3.  **Calculate Relative Positions:** For each non-black pixel within the bounding box, determine its relative position. This is calculated as the pixel's row and column offset from the top-left corner of the bounding box, divided by the bounding box's height and width, respectively.  This results in fractional coordinates between 0 and 1.
4.  **Map to Output Grid:** Scale these relative positions to fit a 3x3 output grid. Multiply the relative row by 3 (the height of output) and the relative column by 3 (width of output). Round these values to get integer row and column indices within the 3x3 output grid.
5. **Fill the Output.** Place each non-black pixel's color from bounding box at these new integer coordinates in the output grid, keeping colors. If multiple pixels map to the same output cell, prioritize the pixel that comes first when iterating through all non black pixels inside bounding box row-wise.
6.  **Empty Output:** If there are no non-black pixels, return a 3x3 grid filled with zeros.
"""

import numpy as np

def get_non_black_pixels(grid):
    """Finds coordinates and colors of non-black pixels."""
    coords = np.argwhere(grid != 0)
    return [(tuple(coord), grid[tuple(coord)]) for coord in coords]

def get_bounding_box(coords):
    """Calculates the minimal bounding box for given coordinates."""
    if not coords:
        return (0, 0, 0, 0)
    min_row, min_col = np.min(coords, axis=0)
    max_row, max_col = np.max(coords, axis=0)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Get non-black pixels
    non_black_pixels = get_non_black_pixels(input_grid)

    # Get bounding box coordinates
    if not non_black_pixels:
        return output_grid

    coords = [pixel[0] for pixel in non_black_pixels]
    min_row, min_col, max_row, max_col = get_bounding_box(coords)
    width = max_col - min_col + 1
    height = max_row - min_row + 1


    # Calculate relative positions and map to output grid
    for pixel, color in non_black_pixels:
        rel_row = (pixel[0] - min_row) / height
        rel_col = (pixel[1] - min_col) / width
        output_row = int(rel_row * 3)
        output_col = int(rel_col * 3)

        # Ensure indices are within bounds
        output_row = max(0, min(output_row, 2))
        output_col = max(0, min(output_col, 2))
        
        # Fill output grid, only if the cell is currently empty (prioritize earlier pixels)
        if output_grid[output_row, output_col] == 0:
            output_grid[output_row, output_col] = color

    return output_grid