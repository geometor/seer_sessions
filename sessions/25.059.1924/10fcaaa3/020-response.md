# 10fcaaa3 • 020 • refine_coder

---
```python
"""
1.  **Double the Grid:** Create an output grid that is twice the height and twice the width of the input grid.
2.  **Locate and Copy Red Pixel:** Find the red pixel (value 2) in the input grid. Copy this pixel to the output grid. The row and column indices are calculated as `(input_row + 1) * 2 - 2` and `(input_col + 1) * 2 -2` respectively.
3. **Horizontal Translation:** Create a second red pixel in the output grid.  The row index is the same as calculated in step 2. The column index is calculated by adding 4 to the column index from step 2.
4.  **Azure Fill:** Fill every other cell in the output grid with azure (value 8) in rows where a red pixel exists and rows that are multiple of red pixel's initial row index.  Start filling azure from column index 0 of that row.
5. **Retain Background**: all white pixels should remain in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Double the grid
    input_height, input_width = input_grid.shape
    output_height, output_width = 2 * input_height, 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the red pixel in the input grid
    red_pixels = np.argwhere(input_grid == 2)

    for red_pixel in red_pixels:
        # Copy and translate red pixel
        row, col = red_pixel
        output_row = (row + 1) * 2 - 2
        output_col = (col + 1) * 2 - 2
        output_grid[output_row, output_col] = 2

        # Horizontal translation
        new_col = output_col + 4
        if new_col < output_width:
            output_grid[output_row, new_col] = 2

        # Azure fill based on red pixel row and multiples
        for i in range(output_height):
          if i == output_row or (output_row !=0 and i % (output_row+1) == 0) :
            for j in range(0, output_width, 2):
                output_grid[i, j] = 8

    return output_grid
```
