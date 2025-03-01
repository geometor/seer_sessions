"""
1. Preserve Blue Pixels: Copy all blue pixels (value 1) from the input grid to the output grid without any changes to their position or value.
2. Identify Left-most White Pixels: For each row, scan from left to right. Identify contiguous sequences of white pixels (value 0) that are immediately followed by a blue pixel (value 1). Within each such sequence, only the left-most white pixel is selected.
3. Change to Red: Change the color of the selected left-most white pixels to red (value 2).
4. Preserve other Pixels: All other pixels that are not blue or identified as the "left-most" white pixels remain with their input value.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)  # Start with a copy to preserve blues and other pixels
    rows, cols = input_grid.shape

    # Iterate through each row
    for r in range(rows):
        # Scan from left to right
        c = 0
        while c < cols:
            # Check for a sequence of white pixels followed by a blue pixel
            if input_grid[r, c] == 0:
                start_white = c
                while c < cols and input_grid[r, c] == 0:
                    c += 1
                # Check if the sequence is followed by a blue pixel
                if c < cols and input_grid[r, c] == 1:
                    # Change the left-most white pixel to red
                    output_grid[r, start_white] = 2
            else:
                c += 1

    return output_grid