import numpy as np
from collections import Counter

"""
Transforms an input grid based on row classification and a derived pattern template.

1.  **Identify Background Color:** Assume gray (7) is the background.
2.  **Identify Fill Rows and Colors:** Iterate through input rows. A row is a "fill row" if any single non-background color appears 2+ times. Store the row index and the specific color causing the fill ("fill color"). Other rows are implicitly "pattern rows" for output construction.
3.  **Derive Pattern Template:** Initialize a template row (width of grid) with the background color. Iterate through every input pixel (r, c). If the pixel's color is not background AND (the pixel's row 'r' is not a fill row OR the pixel's color is not the fill color for row 'r'), update the template row at column 'c' with the pixel's color.
4.  **Construct Output Grid:** Create an output grid. For each row index 'r': if 'r' corresponds to a fill row, fill the output row with that row's fill color; otherwise, copy the derived pattern template into the output row.
"""

def transform(input_grid):
    """
    Applies the row-based fill/pattern transformation.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    output_grid = np.zeros_like(input_grid_np)

    # --- Step 1: Identify Background Color ---
    background_color = 7 # Assume gray based on examples

    # --- Step 2: Identify Fill Rows and Fill Colors ---
    fill_info = {}  # {row_index: fill_color} for fill rows

    for r in range(height):
        row = input_grid_np[r, :]
        non_background_pixels = row[row != background_color]

        if len(non_background_pixels) > 0:
            color_counts = Counter(non_background_pixels)
            for color, count in color_counts.items():
                if count >= 2:
                    # Found a fill row
                    fill_info[r] = color
                    # Assume only one color triggers fill per row based on examples
                    break 

    # --- Step 3: Derive the Pattern Template ---
    pattern_template_row = np.full(width, background_color, dtype=int)

    for r in range(height):
        for c in range(width):
            pixel_color = input_grid_np[r, c]

            # Condition 1: Is it background? If yes, ignore.
            if pixel_color == background_color:
                continue

            # Condition 2: Is it the fill color for this specific fill row?
            is_fill_pixel_for_this_row = False
            if r in fill_info and pixel_color == fill_info[r]:
                is_fill_pixel_for_this_row = True

            # If not background and not the fill color for its row, use it for the template
            if not is_fill_pixel_for_this_row:
                pattern_template_row[c] = pixel_color

    # --- Step 4: Construct the Output Grid ---
    for r in range(height):
        if r in fill_info:
            # This is a fill row, fill with its specific fill color
            output_grid[r, :] = fill_info[r]
        else:
            # This is a pattern row, copy the derived template
            output_grid[r, :] = pattern_template_row

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()