import numpy as np

"""
Transforms an input grid based on the location and color of non-white pixels.

1.  Create a new output grid with the same dimensions as the input grid, initialized with white (0).
2.  Find all non-white pixels ("trigger pixels") in the input grid.
3.  For each trigger pixel (with row `R`, column `C`, and color `Color`):
    a.  Determine its vertical zone: top zone (rows 0-4) or bottom zone (rows 5-9, assuming a 10-row grid).
    b.  Calculate the row boundaries for the zone (`min_row`, `max_row`). For the top zone, `min_row=0`, `max_row=4`. For the bottom zone, `min_row=5`, `max_row=height-1`.
    c.  Draw vertical lines in the output grid using `Color` at the leftmost column (0) and rightmost column (width-1), spanning from `min_row` to `max_row`.
    d.  Draw a horizontal line in the output grid using `Color` across the full width at the trigger pixel's row `R`.
    e.  Draw an additional horizontal boundary line using `Color` across the full width:
        i.  If the trigger pixel is in the top zone (`R < 5`), draw this line at row 0.
        ii. If the trigger pixel is in the bottom zone (`R >= 5`), draw this line at the bottommost row (`height - 1`).
4.  Return the final output grid. Modifications from later trigger pixels overwrite earlier ones.
"""

def find_trigger_pixels(grid):
    """Finds all non-white pixels in the grid."""
    triggers = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                triggers.append({'row': r, 'col': c, 'color': color})
    return triggers

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # 1. Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # 2. Find all non-white pixels (trigger pixels)
    trigger_pixels = find_trigger_pixels(input_grid)

    # 3. Process each trigger pixel
    for pixel_info in trigger_pixels:
        r = pixel_info['row']
        # col = pixel_info['col'] # Column index is not directly used for drawing lines
        color = pixel_info['color']

        min_row = 0
        max_row = 0
        is_top_zone = False

        # 3.a. Determine the vertical zone and its boundaries
        # Assuming zones are fixed at 0-4 and 5-9 for 10x10 grids
        # Adapt if grid height varies significantly and zone logic changes
        if r < 5:
            min_row = 0
            max_row = 4 # Assuming top zone always ends at 4 if grid is >= 5 high
            if height < 5: # Handle grids shorter than 5 rows
                max_row = height -1
            is_top_zone = True
        else: # r >= 5
            min_row = 5
            max_row = height - 1 # Bottom zone always extends to the last row
            is_top_zone = False
            if height <= 5: # Handle grids where r>=5 but height is small
                 min_row = 0 # Treat as one zone? Or is r>=5 impossible? Assume rule applies if possible.
                 # Re-evaluate if example with height <= 5 appears.
                 # Let's stick to the 10x10 observation for now.

        # Adjust max_row if it exceeds grid bounds (safety check)
        max_row = min(max_row, height - 1)
        # Adjust min_row if it exceeds grid bounds (safety check)
        min_row = min(min_row, height - 1)


        # 3.b. Draw vertical lines for the zone
        # Draw left vertical line
        if 0 <= min_row < height and 0 <= max_row < height : # Ensure row indices are valid
             output_grid[min_row : max_row + 1, 0] = color
        # Draw right vertical line
        if 0 <= min_row < height and 0 <= max_row < height: # Ensure row indices are valid
             output_grid[min_row : max_row + 1, width - 1] = color


        # 3.c. Draw the horizontal line at the trigger pixel's row
        if 0 <= r < height: # Ensure row index is valid
            output_grid[r, 0:width] = color

        # 3.d. Draw the zone boundary horizontal line
        if is_top_zone:
            # Draw top boundary line (row 0)
            output_grid[0, 0:width] = color
        else:
            # Draw bottom boundary line (row height - 1)
            output_grid[height - 1, 0:width] = color

    # 4. Return the final output grid
    return output_grid