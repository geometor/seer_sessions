```python
"""
1.  **Identify 3-Pixel Lines:** Find all horizontal and vertical lines consisting of exactly 3 contiguous pixels, where all pixels in the line are non-zero. These lines define "objects," and each object will be used once in the final output.

2.  **Center Pixel Expansion:** For each identified 3-pixel line, expand the central pixel. The center expands to fill a 3x3 block around it, keeping its original color, but respecting grid boundaries (i.e. at the edge of the grid, this will be a 3x2, 2x3, or 2x2 block.

3.  **Wing Pixel Transformation and Mirrored Block Creation:**
    *   For each 3-pixel line, identify the two "wing" pixels (the pixels on either end of the line).
    *   Determine the transformed color of the wing pixels: If a wing pixel is orange (7), its transformed color is red (2). If a wing pixel is azure (8), its transformed color is magenta (6).
    *   For *each* wing pixel, create a new 1x3 block *mirrored* across the central pixel of the original 3-pixel line. This new block will have the *transformed* color. This new block does *not* replace the original wing pixels; it is an additional element.

4.  **Output:** The output grid consists of the expanded central pixels and the mirrored 1x3 blocks created from the wing pixels. Note: the original 3-pixel line's wing pixels are *not* directly present in the output, only their transformation on the opposite side of the center.
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
                })

    # Check for vertical objects
    for r in range(rows - 2):
        for c in range(cols):
            if grid[r, c] != 0 and grid[r+1, c] != 0 and grid[r+2, c] != 0:
                objects.append({
                    'type': 'vertical',
                    'central': (r+1, c),
                    'wings': [(r, c), (r+2, c)],
                })

    return objects

def expand_center_pixel(grid, row, col, color):
    """Expands the central pixel into a 3x3 block, respecting boundaries."""
    rows, cols = grid.shape
    for r in range(max(0, row - 1), min(rows, row + 2)):
        for c in range(max(0, col - 1), min(cols, col + 2)):
            grid[r, c] = color

def create_mirrored_block(grid, central_row, central_col, wing_row, wing_col, color):
    """Creates a 1x3 mirrored block."""
    row_offset = wing_row - central_row
    col_offset = wing_col - central_col
    mirrored_row = central_row - row_offset
    mirrored_col = central_col - col_offset

    if 0 <= mirrored_row < grid.shape[0]:
      grid[mirrored_row, max(0, mirrored_col - 1)] = color
      grid[mirrored_row, mirrored_col] = color
      grid[mirrored_row, min(grid.shape[1] - 1, mirrored_col + 1)] = color



def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    objects = find_3_pixel_objects(input_grid)

    for obj in objects:
        central_row, central_col = obj['central']
        central_color = input_grid[central_row, central_col]

        # Expand central pixel
        expand_center_pixel(output_grid, central_row, central_col, central_color)

        for wing_row, wing_col in obj['wings']:
            wing_color = input_grid[wing_row, wing_col]

            # Determine transformed color
            if wing_color == 7:
                transformed_color = 2
            elif wing_color == 8:
                transformed_color = 6
            else:
                transformed_color = wing_color  # Should not happen, but good practice

            # Create mirrored block
            create_mirrored_block(output_grid, central_row, central_col, wing_row, wing_col, transformed_color)

    return output_grid
```