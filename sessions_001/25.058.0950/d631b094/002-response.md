# d631b094 • 002 • example_4 • investigate_coder

---
```python
"""
1.  **Identify** all non-zero pixels within the input grid.
2.  **Count** the number of non-zero pixels.
3. **Create output**:
    *   If there is one non-zero pixel make output a 1 x 1 grid.
    *   If there are two, make a 1 x 2 grid
    *   If there are three, a 1 x 3 grid.
    *    If four, a 1 x 4 grid.
4. **Populate Output**:
   *   Fill the output grid with the non-zero values, preserving the original colors.
   * Each value is place in the output from left to right.
5.  **Discard** all zero-valued (white) pixels.
"""

import numpy as np

def transform(input_grid):
    # Find all non-zero pixels
    non_zero_pixels = []
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != 0:
                non_zero_pixels.append(input_grid[i, j])

    # Count the number of non-zero pixels
    count = len(non_zero_pixels)

    # Create output grid based on the count
    if count == 0:
      return np.array([[]])
    
    output_grid = np.zeros((1, count), dtype=int)


    # Populate the output grid with the non-zero values
    for i in range(count):
        output_grid[0, i] = non_zero_pixels[i]

    return output_grid
```
