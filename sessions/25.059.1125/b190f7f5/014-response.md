# b190f7f5 • 014 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Output Grid Initialization:** Create an output grid with dimensions three times larger than the input grid (width * 3, height * 3). Initialize it with all white (0) pixels.

2.  **Input Grid Iteration:** Iterate through each pixel of the input grid.

3.  **Azure Pixel Handling:** If the input pixel is azure (8) or white (0), skip to the next pixel.

4.  **Plus Shape Generation:** For each non-azure, non-white pixel:
    *   Calculate the output coordinates for the top-left of the shape: Multiply the row and column indices of the input pixel by 3.  This gives the top-left corner of the 3x3 plus shape.
    *   Create 3x3 'plus' shape - centered at (out_row + 1, out_col + 1), using a fill of the input pixel's color.

5.  **Return Output Grid:** The output grid now contains the transformed representation of the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid based on input_grid size, multiplied by 3
    output_rows = input_grid.shape[0] * 3
    output_cols = input_grid.shape[1] * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # iterate through the input grid
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            color = input_grid[r, c]

            # skip azure (8) and white (0)
            if color == 8 or color == 0:
                continue

            # calculate the top-left coordinates for the plus shape
            out_r = r * 3
            out_c = c * 3

            # Create the plus shape, ensuring it stays within bounds.
            # Center is at (out_r + 1, out_c + 1)
            center_r = out_r + 1
            center_c = out_c + 1

            if center_r > 0:
                output_grid[center_r - 1, center_c] = color  # Up
            if center_r < output_rows - 1:
                output_grid[center_r + 1, center_c] = color  # Down
            if center_c > 0:
                output_grid[center_r, center_c - 1] = color  # Left
            if center_c < output_cols - 1:
                output_grid[center_r, center_c + 1] = color  # Right
            output_grid[center_r, center_c] = color  # Center

    return output_grid
```
