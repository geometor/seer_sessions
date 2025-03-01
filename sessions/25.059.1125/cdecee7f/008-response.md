# cdecee7f • 008 • refine_coder

---
```python
"""
Transforms a 10x10 grid by finding the first row with a non-zero pixel and extracting that pixel's value. The output grid's dimensions are determined by the presence and number of non-zero pixels in that row. If there's only one non-zero pixel, the output is a 1x1 grid containing that pixel's value. If multiple non-zero pixels exist in the identified row, the output is a 3x3 grid with the first non-zero pixel's value at the top-left corner.
"""

import numpy as np

def transform(input_grid):
    # Find the first row with a non-zero pixel
    output_grid = None
    for row_index, row in enumerate(input_grid):
        non_zero_pixels = row[row != 0]
        if non_zero_pixels.size > 0:
            first_non_zero_pixel = non_zero_pixels[0]
            if non_zero_pixels.size == 1:
                # single pixel output
                output_grid = np.array([[first_non_zero_pixel]])

            else:
                # multi pixel output
                output_grid = np.zeros((3, 3), dtype=int)
                output_grid[0, 0] = first_non_zero_pixel
            break  # Stop after finding the first row with non-zero pixels

    # if no non-zero pixels found
    if output_grid is None:
        output_grid = np.zeros((3,3), dtype=int)

    return output_grid
```
