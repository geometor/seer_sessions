# 1b2d62fb • 020 • refine_coder

---
```python
"""
1.  **Input and Output:** The input and output grids are the same size.
2.  **Blue Pixel Identification:** For each row in the input grid, identify the *first* blue (1) pixel.
3.  **Azure Transformation:** In the output grid, change the pixel at the location of this *first* blue pixel to azure (8).
4. **Row Preservation:** If a row has no blue pixels, the row remains unchanged from input to output.
5. **Other Pixels:** All other pixels, except that *first* blue, remain in their original color and position in the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.array(input_grid).copy()

    # Iterate through each row
    for i in range(output_grid.shape[0]):
        # Find the index of the first blue (1) pixel in the row
        blue_indices = np.where(output_grid[i] == 1)[0]
        if len(blue_indices) > 0:
          #if blue pixel found
          first_blue_index = blue_indices[0]
          # Set the corresponding pixel in the output grid to azure (8)
          output_grid[i, first_blue_index] = 8

    return output_grid.tolist()
```
