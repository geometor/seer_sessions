"""
1.  **Iterate** through each pixel of the input grid.
2.  **Preserve 0 and 1:** If a pixel's value is 0 or 1, copy it directly to the output grid without changes.
3.  **Check Odd Columns First:** For any other pixel value (not 0 or 1), check every odd-indexed column *in the same row*.
    * **Matching Value in Odd Column Found:** If *any* odd-indexed column in the same row has the *same value* as the current pixel, copy current pixel's value to the output grid.
    * **No Matching Value in Odd Column Found**: If no odd-indexed column contains that value, if the current column is even, set to value of 1 in the output. Otherwise if the current column is odd, copy current pixel's value to the output.
4.  **Return** the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    output_grid = np.copy(input_grid)  # Initialize output grid as a copy
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # Preserve 0 and 1 values
            if input_grid[r, c] == 0 or input_grid[r, c] == 1:
                continue  # Skip to the next iteration

            # Check for matching values in odd-indexed columns
            found_match = False
            for odd_c in range(1, cols, 2):  # Iterate through odd columns only
                if input_grid[r, odd_c] == input_grid[r, c]:
                    found_match = True
                    break

            if not found_match and c % 2 == 0:
                output_grid[r,c] = 1


    return output_grid