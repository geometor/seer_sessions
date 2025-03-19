"""
1.  **Identify Blue Pixels:** Locate all blue pixels within the input grid.

2.  **Contextual Modification:**
    - Check for non-blue pixels around the blue pixels, not only horizontally but potentially vertically or diagonally.
    - If a pixel is azure or maroon, copy it to the three positions to its right.
    - If a pixel is red, yellow, or green, copy it to one position to its right.
    - If there is a blue pixel on its own, put another blue pixel directly under it.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is blue
            if input_grid[r, c] == 1:
                # Check for single blue pixels and add one below
                if r + 1 < rows:
                    output_grid[r+1,c] = 1

                # Check for adjacent non-blue pixels
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue  # Skip the blue pixel itself

                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] != 1:
                            color = input_grid[nr, nc]
                            # Apply duplication rules based on color
                            if color in [2, 4, 3]:  # Red, yellow, green
                                if nc + 1 < cols:
                                        output_grid[nr, nc + 1] = color
                            elif color in [8, 9]:  # Azure, maroon
                                for i in range(1, 4):
                                    if nc + i < cols:
                                        output_grid[nr, nc + i] = color
    return output_grid