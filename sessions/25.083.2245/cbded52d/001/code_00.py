"""
1.  **Iterate** through each pixel of the input grid.
2.  **Preserve** the values 0 and 1, and keep them unchanged in the output grid.
3.  **check pixel's value and column index**:
    - If the pixel's value is not 0 or 1, and it is in the even column. Check if exist another pixel in the same row, with the same value and odd column index.
    - If exist, keep the original value.
    -If not, change the original value
4.  All other pixels are copied to the output grid with no change.
5. **Return** output grid
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
                  if search_c % 2 != 0:
                    if input_grid[r,search_c] == input_grid[r,c]:
                      found_match = True
                      break

                if not found_match:
                    # find next candidate to change pixel

                    candidates = []
                    for search_c in range(cols):
                        if input_grid[r,search_c] != 0 and input_grid[r,search_c] != 1:
                          candidates.append(input_grid[r,search_c])

                    if len(candidates)>0:
                        output_grid[r,c] = candidates[0]

    return output_grid