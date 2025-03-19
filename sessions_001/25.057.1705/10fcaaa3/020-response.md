# 10fcaaa3 • 020 • example_4 • investigate_coder

---
```python
"""
1.  **Expand Grid:** Double the dimensions of the input grid (from 4x4 to 8x8).

2.  **Replicate Red:** Duplicate input red pixel
    *   first replicated pixel will appear at same row but in column = column * 2
    *   second replicated pixel will appear at row = row * 4, column will stay
        the same

3.  **Populate Azure Checkboard:** Fill alternating cells in the expanded output grid with azure (8), starting at the top-left cell (0,0). Specifically add an azure cell to the output grid if:
    *   the sum of its row and column indices is even.

4. **Fill Remaining with White**: Any output cells not filled with a value are filled with white (0).
"""

import numpy as np

def transform(input_grid):
    # Expand Grid: Double the dimensions of the input grid.
    input_height, input_width = input_grid.shape
    output_height, output_width = input_height * 2, input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the red pixel in the input grid.
    red_pixels = np.argwhere(input_grid == 2)
    if len(red_pixels) > 0:
        red_row, red_col = red_pixels[0]

        # Replicate Red (first instance).
        output_grid[red_row, red_col * 2] = 2
        # second red pixel
        output_grid[red_row * 4, red_col] = 2


    # Populate Azure Checkerboard.
    for row in range(output_height):
        for col in range(output_width):
            if (row + col) % 2 == 0:
                output_grid[row, col] = 8

    # the fill remaining with white happens by default
    # because of np.zeros initialization

    return output_grid
```
