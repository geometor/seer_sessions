"""
1. **Examine each row:** Iterate through every row in the input grid.
2. **Red Pixel Check:** For each row, determine if it contains *any* red pixels.
3. **Row Transformation (Conditional):**
    *   If a row contains at least one red pixel, change *all* pixels in that row to red in the output grid.
    *   If a row contains *no* red pixels, change *all* pixels in that row to white (0) in the output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid based on the presence of red pixels in each row."""
    output_grid = np.zeros_like(input_grid)  # Initialize output_grid with white (0)

    # Iterate through each row
    for i, row in enumerate(input_grid):
        # Check if the row contains any red pixels (2)
        if 2 in row:
            # If red is present, fill the entire row with red
            output_grid[i, :] = 2
        else:
            # If no red is present, fill the entire row with white (already initialized)
            pass

    return output_grid