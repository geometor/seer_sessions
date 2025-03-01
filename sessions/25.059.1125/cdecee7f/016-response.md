# cdecee7f • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify:** Find all non-zero pixels within the 10x10 input grid.
2.  **Extract:** Collect these non-zero pixel values, preserving their original color (value).
3.  **Order:** Take the non-zero digits and place in reading order into the cells
    of the 3 x 3 output.
4.  Specifically, reading top to bottom, left to right.
5.  **Output**: construct new 3x3 grid with the digits.
"""

import numpy as np

def transform(input_grid):
    """Transforms a 10x10 input grid into a 3x3 output grid by extracting and
    rearranging non-zero pixels."""

    # Initialize an empty 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Find all non-zero pixels in the input grid.
    non_zero_pixels = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != 0:
                non_zero_pixels.append(input_grid[i, j])

    # Flatten non_zero_pixel for linear fill
    non_zero_pixels = sorted(non_zero_pixels, key=lambda x: (non_zero_pixels.index(x)))

    # Fill the output grid with the non-zero pixel values.
    k=0
    for i in range(3):
      for j in range(3):
        if k < len(non_zero_pixels):
          output_grid[i,j] = non_zero_pixels[k]
          k+=1

    return output_grid
```
