"""
1.  **Identify Target Pixels:** Locate all yellow (4) pixels and their immediate, vertically adjacent (above and below) green (3) pixels in the input grid.
2.  **Conditional Green Movement:**
    *   If a green pixel is *directly above* a yellow pixel, move the green pixel one position to the *left* of the yellow pixel. The new value replaces any 0, but does not replace any other color.
    *   If a green pixel is *directly below* a yellow pixel, it remains in its original position.
    *   All green pixels are turned to 0 if moved.
3.  **Preserve Other Pixels:** All other pixels (including empty/white pixels and non-adjacent green pixels) remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through to find yellow pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 4:  # Found a yellow pixel
                # Check for green pixel above
                if r > 0 and input_grid[r-1, c] == 3:
                    # Move green pixel to the left of yellow, if possible, clear previous
                    if c > 0:
                        output_grid[r-1,c-1] = 3
                        output_grid[r-1, c] = 0

    return output_grid.tolist()