"""
1.  **Find the Yellow Pixel:** Locate the yellow pixel (color 4) within the input grid. If no yellow pixel is found, assume the position (0, 0).
2.  **Extract 2x2 Subgrid:** Extract a 2x2 subgrid from the input grid. The top-left corner of this subgrid is the location of the yellow pixel.
3.  **Boundary Handling:** If the 2x2 subgrid extends beyond the boundaries of the input grid, fill up any missing cells with azure color (8).
4. **Return 2x2 Grid** The output is always 2x2.
"""

import numpy as np

def find_pixel_by_color(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return (r, c)
    return (0,0) #Return (0,0) if not found.

def transform(input_grid):
    # Find the yellow pixel or default to (0, 0).
    yellow_pos = find_pixel_by_color(input_grid, 4)

    # Extract the 2x2 subgrid.
    row_start = yellow_pos[0]
    col_start = yellow_pos[1]
    output_grid = []

    for r in range(row_start, min(row_start + 2, len(input_grid))):
        row = []
        for c in range(col_start, min(col_start + 2, len(input_grid[0]))):
            row.append(input_grid[r][c])
        
        # Fill missing columns with azure (8).
        while len(row) < 2:
            row.append(8)
        output_grid.append(row)

    # Fill missing rows with azure (8).
    while len(output_grid) < 2:
        output_grid.append([8, 8])

    return output_grid