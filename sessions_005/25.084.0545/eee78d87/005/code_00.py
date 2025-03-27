"""
Transforms an input grid into a 16x16 output grid. The input is embedded in the center,
non-7 pixels within the embedded input are replaced with 9, and the remaining area is
filled with a checkerboard pattern of 0s and 7s, starting with 0 at the top-left corner.
"""

import numpy as np

def transform(input_grid):
    # Create Output Grid: Create a 16x16 output grid filled with 0s.
    output_height, output_width = 16, 16
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Embed Input: Center the input grid within the output grid.
    input_height, input_width = input_grid.shape
    row_offset = (output_height - input_height) // 2
    col_offset = (output_width - input_width) // 2

    # Replace within Embedded Region:
    for r in range(input_height):
        for c in range(input_width):
            # Pixels that are 7 in the input grid remain 7.
            if input_grid[r, c] == 7:
                output_grid[row_offset + r, col_offset + c] = 7
            # Other pixels become 9.
            else:
                output_grid[row_offset + r, col_offset + c] = 9

    # Checkerboard Fill: Fill outside the embedded region.
    for r in range(output_height):
        for c in range(output_width):
            # Check if the current position is outside the embedded region.
            if not (row_offset <= r < row_offset + input_height and
                    col_offset <= c < col_offset + input_width):
                # Checkerboard pattern: 0 at (0,0), alternating.
                if (r + c) % 2 == 0:
                    output_grid[r, c] = 0
                else:
                    output_grid[r, c] = 7

    return output_grid