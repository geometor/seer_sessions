"""
1.  **Divide:** Split the input grid vertically into two equal halves: a left and a right half.
2.  **Identify Rightmost Non-Background Pixel:** For each row in the *right* half, find the rightmost pixel that *does not* have the background color (8/azure).
3.  **Copy to Left:** Create an output grid with the same dimensions as the *left* half of the input. For each row, copy the color of the identified rightmost non-background pixel (from step 2) to the *last* column of the output grid, maintaining the row position. If no non-background pixel was found in a row, leave the corresponding row in the output grid unchanged (all zeros).
"""

import numpy as np

def transform(input_grid):
    # Divide the input grid into left and right halves.
    rows, cols = input_grid.shape
    mid_col = cols // 2
    left_half = input_grid[:, :mid_col]
    right_half = input_grid[:, mid_col:]

    # Initialize the output grid as a copy of the left half.
    output_grid = np.copy(left_half)

    # Iterate through each row of the right half.
    for r in range(rows):
        # Find the rightmost non-background pixel in the current row.
        rightmost_color = 0  # Default to 0 if no non-background pixel is found.
        for c in range(right_half.shape[1] - 1, -1, -1):
            if right_half[r, c] != 8:
                rightmost_color = right_half[r, c]
                break  # Stop searching after finding the first non-background pixel.

        # Copy the color to the last column of the output grid.
        target_col = output_grid.shape[1] - 1
        if 0 <= r < output_grid.shape[0]: # make sure row in range
            output_grid[r, target_col] = rightmost_color

    return output_grid