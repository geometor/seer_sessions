import numpy as np

"""
Transforms an input grid by drawing frames and lines based on non-white pixels.

1.  Create a new output grid of the same dimensions as the input grid, initially filled entirely with white pixels (color 0).
2.  Identify all pixels in the input grid that are not white (color 0). These are the "trigger pixels".
3.  For each trigger pixel found, characterized by its row `R`, column `C_idx`, and color `C`:
    a.  Determine the vertical zone based on the trigger pixel's row `R`:
        i.  If `R` is less than 5 (rows 0-4), the zone covers rows 0 through 4. Set `min_row = 0`, `max_row = 4`.
        ii. If `R` is 5 or greater (rows 5-9), the zone covers rows 5 through 9. Set `min_row = 5`, `max_row = 9`.
    b.  Draw a frame using the trigger pixel's color `C` within its determined zone:
        i.  Draw a horizontal line of color `C` across the full width at `min_row`.
        ii. Draw a horizontal line of color `C` across the full width at `max_row`.
        iii. Draw a vertical line of color `C` in the leftmost column (column 0) from `min_row` to `max_row`.
        iv. Draw a vertical line of color `C` in the rightmost column (column width-1) from `min_row` to `max_row`.
    c.  Draw an additional horizontal line of color `C` across the full width at the trigger pixel's original row `R`.
4.  Return the completed output grid. If multiple trigger pixels modify the same pixel, the last modification prevails.
"""

def transform(input_grid):
    """
    Applies the frame and line drawing transformation based on trigger pixels.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # 1. Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid)

    # 2. Find all non-white pixels (trigger pixels)
    trigger_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_grid[r, c]
            if color != 0:
                trigger_pixels.append({'row': r, 'col': c, 'color': color})

    # 3. Process each trigger pixel
    for pixel_info in trigger_pixels:
        r = pixel_info['row']
        # c_idx = pixel_info['col'] # Column index is not used in the updated logic
        color = pixel_info['color']

        min_row = 0
        max_row = 0

        # 3.a. Determine the vertical zone and its boundaries
        if r < 5:
            min_row = 0
            max_row = 4
        else: # r >= 5
            min_row = 5
            # Assuming 10x10 grid based on examples, max row is 9
            max_row = height - 1 # Use height for generality

        # Check if grid dimensions are consistent with zone logic (height >= 10)
        if height < 10 and r >= 5 :
             # Adjust max_row if height is less than 10 but pixel is in 'second zone'
             # This case might need more clarification based on task constraints if
             # grids smaller than 10x10 are possible and use this rule.
             # For now, stick to the observed 10x10 pattern.
             max_row = height - 1 # Still the last row
             # It might be that the zone concept only applies strictly to 10x10 grids.
             # If grids can be smaller, the rule might adapt differently.
             # Let's assume grids are 10x10 as per examples.

        # 3.b. Draw the frame for the zone
        # Draw top horizontal line of the zone
        output_grid[min_row, 0:width] = color
        # Draw bottom horizontal line of the zone
        output_grid[max_row, 0:width] = color
        # Draw left vertical line for the zone
        output_grid[min_row:max_row + 1, 0] = color
        # Draw right vertical line for the zone
        output_grid[min_row:max_row + 1, width - 1] = color

        # 3.c. Draw the additional horizontal line at the trigger pixel's row
        output_grid[r, 0:width] = color

    # 4. Return the final output grid
    return output_grid