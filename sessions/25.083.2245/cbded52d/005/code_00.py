"""
1.  **Iterate** through each pixel of the input grid.
2.  **Preserve** the values 0 and 1, keep them unchanged in the output grid.
3.  **Check Pixel's Value and Column Index**: For each pixel, consider its value and column index.
    *   If the pixel's value is 0 or 1, copy it directly to the output grid without changes.
    *   If the pixel's value is not 0 or 1, and the pixel in an even column, check if there is another pixel in the *same row* that has:
        1.  The same value.
        2.  An odd column index.
4. **Conditional Change**:
        *  If such a pixel exists, keep the same value.
    * If not, change the pixel to the value 1.
5.  **Return** the modified output grid.

Refined based on initial results:
    * Make search for matching pixels include the pixel itself (important for cases with only one non-0/1 in row)
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

            # Check if the pixel is not 0 or 1 and in an even column
            if c % 2 == 0:
                found_match = False
                for search_c in range(cols):
                    # Include the cell itself and make sure we find a match in an odd column
                    if search_c % 2 != 0 and input_grid[r,search_c] == input_grid[r,c]:
                        found_match = True
                        break

                if not found_match:
                    output_grid[r,c] = 1

    return output_grid