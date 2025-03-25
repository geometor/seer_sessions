"""
1.  **Scan:** Iterate through the grid, looking for black (0) pixels.
2.  **Contextual Check:** For each black pixel, check its immediate neighbors (left and right).
3.  **Condition:** If the left neighbor is a non-black color (A), and the right neighbor has the *same* color (B) as a sequence of 2 or more,
4. **Transformation:** Change the black pixel's color to color A.
5.  **Repeat:** Continue scanning the entire grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for r in range(rows):
        for c in range(cols):
            # Scan: Find black pixels.
            if input_grid[r, c] == 0:
                # Contextual Check: Check left and right neighbors.
                if c > 0 and c < cols - 1:  # Ensure we're not at the edges
                    left_color = input_grid[r, c - 1]
                    right_color = input_grid[r, c + 1]
                    
                    # Condition: Left is non-black (A), Right is different and part of a sequence
                    if left_color != 0 and right_color != 0 and left_color != right_color:
                      # Check for a sequence to the right of color B of at least 2 length
                      if c + 2 < cols and input_grid[r,c+2] == right_color:
                        # Transformation: Change the black pixel to color A.
                        output_grid[r, c] = left_color
    return output_grid