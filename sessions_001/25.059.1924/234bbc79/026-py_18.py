"""
1.  **Filter:** Examine each row of the input grid. Count the occurrences of blue (1) and red (2) pixels, ignoring gray (5) pixels.
2.  **Output Dimensions:**
    *   The output grid's *height* is the number of rows in the input grid that contain *at least one* blue or red pixel.
    *   The output grid's *width* is equal to the maximum number of blue and red pixels found in any single row of the input grid (after removing gray pixels).
3.  **Arrange:** For each row in the input grid that contains blue or red pixels, create a corresponding row in the output grid. Place all blue pixels (if any) to the left, followed by all red pixels (if any).
4.  **Fill:** Fill any remaining cells in each output row with black (0) pixels, up to the determined output grid width.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Identify and remove gray pixels, retain and count blue and red.
    filtered_pixels = []
    for r in range(rows):
        row_pixels = []
        for c in range(cols):
            if input_grid[r, c] in (1, 2):
                row_pixels.append(input_grid[r, c])
        if row_pixels:  # Only add rows with blue or red pixels
          filtered_pixels.append(row_pixels)


    # Determine output grid dimensions.
    max_width = 0
    for row in filtered_pixels:
        max_width = max(max_width, len(row))
    output_rows = len(filtered_pixels) # Number of rows with blue or red

    output_grid = np.zeros((output_rows, max_width), dtype=int)
    
    # Arrange pixels in output grid: blue to the left of red.
    for r, row_pixels in enumerate(filtered_pixels):
        blue_pixels = [p for p in row_pixels if p == 1]
        red_pixels = [p for p in row_pixels if p == 2]
        new_row = blue_pixels + red_pixels
        output_grid[r, :len(new_row)] = new_row

    return output_grid.tolist()