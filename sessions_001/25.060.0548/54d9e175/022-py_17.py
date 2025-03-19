"""
1. **Identify Key Pixels:** Locate all non-gray pixels (blue, red, green, yellow) in the *input grid*, excluding those in the gray dividing line, and also excluding all white colored pixels.
2. **Gray Line Preservation:** Copy the horizontal gray line (row index 3) from the input grid to the output grid directly.
3. **Generate Blocks:** For each identified key pixel:
    *   Determine the corresponding output color: blue becomes azure, red becomes maroon, green becomes orange, and yellow becomes magenta.
    *   Create a 3x3 square block of the corresponding output color in the *output grid*.
    *   Center the 3x3 block on the location of the original key pixel in the input grid.
4. **Background**: All remaining pixels should have the same color as those of the dividing gray line.
"""

import numpy as np

COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

OUTPUT_COLOR_MAPPING = {
    1: 8,  # blue -> azure
    2: 9,  # red -> maroon
    3: 7,  # green -> orange
    4: 6,  # yellow -> magenta
}

def get_key_pixels(grid):
    # Find non-gray, non-white pixels excluding row 3
    key_pixels = []
    for i, row in enumerate(grid):
        if i != 3:
          for j, pixel in enumerate(row):
              if pixel != 0 and pixel != 5:  # Not white and not gray
                  key_pixels.append((i, j, pixel))
    return key_pixels

def transform(input_grid):
    # Initialize output_grid with the same dimensions and gray background
    output_grid = np.full_like(input_grid, 5)

    # Preserve the gray line
    output_grid[3, :] = input_grid[3, :]

    # Get key pixels (non-gray, non-white pixels excluding row 3)
    key_pixels = get_key_pixels(input_grid)


    # Generate 3x3 blocks
    for i, j, pixel_color in key_pixels:
        output_color = OUTPUT_COLOR_MAPPING.get(pixel_color)
        if output_color:
            # Calculate block boundaries, handling edge cases
            row_start = max(0, i - 1)
            row_end = min(output_grid.shape[0], i + 2)
            col_start = max(0, j - 1)
            col_end = min(output_grid.shape[1], j + 2)

            # Fill the block with the output color
            output_grid[row_start:row_end, col_start:col_end] = output_color

    return output_grid