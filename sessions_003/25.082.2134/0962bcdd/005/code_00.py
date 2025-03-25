"""
1.  **Identify 3-Pixel Lines:** Find all horizontal and vertical lines consisting of 3 pixels. These are the "objects."
2.  **Object Structure:** For each object, identify the central pixel and the two "wing" pixels.
3.  **Central Pixel Expansion:** Expand the central pixel into a 1x3 block (itself and one pixel to the left, and one to the right, if on the same row; or one pixel up and one down, if on the same column).
4.  **Wing Pixel Mirroring and Expansion:**
    *   For each wing pixel, find its mirrored position relative to the central pixel.
    *   Expand *both* the original wing pixel and its mirrored counterpart into 1x3 blocks.
5.  **Color Transformation:**
    *   If a wing pixel is orange (7), change it to red (2) during its expansion.
    *    If a wing pixel is azure (8), change it to magenta (6) during its expansion.
    *   The color of central pixels is kept without changes.
"""

import numpy as np

def find_3_pixel_objects(grid):
    """Finds horizontal and vertical 3-pixel objects."""
    rows, cols = grid.shape
    objects = []

    # Check for horizontal objects
    for r in range(rows):
        for c in range(cols - 2):
            if grid[r, c] != 0 and grid[r, c+1] != 0 and grid[r, c+2] != 0:
                objects.append({
                    'type': 'horizontal',
                    'central': (r, c+1),
                    'wings': [(r, c), (r, c+2)],
                    'colors': [grid[r,c], grid[r,c+1], grid[r,c+2]]
                })

    # Check for vertical objects
    for r in range(rows - 2):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r+1, c] != 0 and grid[r+2, c] != 0:
                objects.append({
                    'type': 'vertical',
                    'central': (r+1, c),
                    'wings': [(r, c), (r+2, c)],
                    'colors' : [grid[r,c], grid[r+1,c], grid[r+2,c]]
                })

    return objects

def expand_pixel(grid, row, col, color):
    """Expands a pixel into a 1x3 block."""
    if 0 <= row < grid.shape[0]:
        grid[row, max(0, col - 1)] = color
        grid[row, col] = color
        grid[row, min(grid.shape[1] - 1, col + 1)] = color


def transform(input_grid):
    """Transforms the input grid based on 3-pixel line mirroring and expansion."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    objects = find_3_pixel_objects(input_grid)

    for obj in objects:
        central_row, central_col = obj['central']
        central_color = input_grid[central_row, central_col]

        # Expand central pixel
        expand_pixel(output_grid, central_row, central_col, central_color)


        for wing_row, wing_col in obj['wings']:
            wing_color = input_grid[wing_row, wing_col]

            # Mirror wing pixels
            row_offset = wing_row - central_row
            col_offset = wing_col - central_col
            mirrored_row = central_row - row_offset
            mirrored_col = central_col - col_offset

            # Color change
            if wing_color == 7:
                transformed_color = 2
            elif wing_color == 8:
                transformed_color = 6
            else:
                transformed_color = wing_color

            # Expand original wing pixel
            expand_pixel(output_grid, wing_row, wing_col, transformed_color)
            

            # Expand mirrored wing pixel
            if 0 <= mirrored_row < output_grid.shape[0] and 0 <= mirrored_col < output_grid.shape[1]:
                expand_pixel(output_grid, mirrored_row, mirrored_col, transformed_color)
    return output_grid