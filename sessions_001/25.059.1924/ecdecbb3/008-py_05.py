"""
1.  **Identify Initial Red Pixels:** Locate all red (2) pixels in the input grid. These mark the origins of the red lines.

2.  **Define Red Lines:** For each initial red pixel, create a vertical "red_line" object. This object is conceptually a vertical line extending from the top to the bottom of the grid, passing through the initial red pixel's column. It is important to only store the column and the original row.

3.  **Extend Red Vertically (Visually):** For each initial red pixel, extend red color vertically upwards and downwards to the grid's edges.

4.  **Transform Azure Pixels:** Identify all azure (8) pixels. For each azure pixel:
    *   Check Adjacency to Original Red Line: Determine if the azure pixel is horizontally or vertically (not diagonally) adjacent to *any* pixel that belongs to the original red_line defined in step 2 (only check column not the extended red).
    *   Conditional Transformation:
        *   If adjacent to an original red_line, change the azure pixel to red (2).
        *   Otherwise, change the azure pixel to white (0).
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color in the grid."""
    pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == color:
                pixels.append((row_index, col_index))
    return pixels

def is_adjacent(coord1, coord2):
    """Checks if two coordinates are adjacent (not diagonally)."""
    row1, col1 = coord1
    row2, col2 = coord2
    return (abs(row1 - row2) <= 1 and col1 == col2) or \
           (abs(col1 - col2) <= 1 and row1 == row2)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    grid_height = len(input_grid)

    # 1. Identify Initial Red Pixels
    initial_red_pixels = get_pixels_by_color(input_grid, 2)

    # 2. Define Red Lines (store origin and column)
    red_lines = [{'origin': red_pixel, 'col': red_pixel[1]} for red_pixel in initial_red_pixels]

    # 3. Extend Red Vertically (Visually)
    for red_line in red_lines:
        col = red_line['col']
        for r in range(grid_height):
            output_grid[r, col] = 2

    # 4. Transform Azure Pixels
    azure_pixels = get_pixels_by_color(output_grid, 8)
    for azure_pixel in azure_pixels:
        row, col = azure_pixel
        adjacent_to_red_line = False

        # Check Adjacency to *Original* Red Line
        for red_line in red_lines:
            if is_adjacent((row, col), (red_line['origin'][0] ,red_line['col'])): # check against original line
                adjacent_to_red_line=True
                break

        # Conditional Transformation
        if adjacent_to_red_line:
            output_grid[row, col] = 2
        else:
            output_grid[row, col] = 0

    return output_grid