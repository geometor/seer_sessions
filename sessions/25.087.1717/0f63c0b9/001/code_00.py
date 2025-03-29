import numpy as np

"""
Transforms an input grid containing sparse colored pixels into an output grid with horizontal zones defined by those pixels.

1. Identify all non-white pixels in the input grid, recording their color and row index.
2. Sort these pixels based on their row index (top to bottom).
3. Initialize an output grid of the same dimensions as the input, filled with white (0).
4. Iterate through the sorted pixels. For each pixel (color C, row R):
    a. Draw a solid horizontal line of color C across the full width at row R in the output grid.
    b. Determine the starting row for the vertical borders. This is the row immediately after the previous pixel's row (or row 0 if it's the first pixel).
    c. Draw vertical lines of color C in the leftmost (column 0) and rightmost (last column) columns, from the starting row up to (but not including) row R.
5. After processing all pixels, identify the color (C_last) and row (R_last) of the last (lowest) pixel.
6. Draw vertical lines of color C_last in the leftmost and rightmost columns from row R_last + 1 up to (but not including) the final row.
7. Draw a solid horizontal line of color C_last across the full width at the very last row of the output grid.
"""

def transform(input_grid):
    """
    Applies the described zone-filling transformation to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid containing pixels 0-9.

    Returns:
        np.array: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.zeros_like(input_np) # Initialize with background color 0 (white)

    # 1. Identify all non-white pixels
    pixels = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != 0:
                pixels.append({'color': color, 'row': r, 'col': c})

    # Handle case with no non-white pixels (return empty grid)
    if not pixels:
        return output_grid

    # 2. Sort pixels by row index
    sorted_pixels = sorted(pixels, key=lambda p: p['row'])

    # 3. Initialize output grid (already done)

    # 4. Iterate through sorted pixels and draw zones
    previous_row = -1
    for pixel in sorted_pixels:
        color = pixel['color']
        row = pixel['row']

        # a. Draw solid horizontal line
        output_grid[row, :] = color

        # b. Determine start row for vertical borders
        start_row_borders = previous_row + 1

        # c. Draw vertical borders
        # Ensure start index is not greater than end index before slicing
        if start_row_borders < row:
            output_grid[start_row_borders:row, 0] = color  # Left border
            output_grid[start_row_borders:row, width - 1] = color # Right border

        # Update previous_row for the next iteration
        previous_row = row

    # 5. Get info for the last pixel
    last_pixel = sorted_pixels[-1]
    last_color = last_pixel['color']
    last_row = last_pixel['row']

    # 6. Draw remaining vertical borders below the last pixel's row
    start_row_final_borders = last_row + 1
    # Ensure start index is not greater than end index before slicing
    if start_row_final_borders < height - 1:
         output_grid[start_row_final_borders:height - 1, 0] = last_color # Left border
         output_grid[start_row_final_borders:height - 1, width - 1] = last_color # Right border

    # 7. Draw final solid horizontal line at the bottom
    output_grid[height - 1, :] = last_color

    return output_grid.tolist() # Return as list of lists per ARC standard