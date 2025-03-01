# cdecee7f • 004 • example_1 • investigate_coder

---
```python
"""
Transforms a 10x10 grid by extracting non-zero pixels and arranging them into a 3x3 grid, preserving their original colors.
"""

import numpy as np

def transform(input_grid):
    # Initialize an empty list to store non-zero pixels and their original positions
    non_zero_pixels = []

    # Iterate through the input grid to find non-zero pixels
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            if pixel_value != 0:
                non_zero_pixels.append((pixel_value, row_index, col_index))

    # Sort the non-zero pixels based on their original positions (first by row, then by column)
    non_zero_pixels.sort(key=lambda x: (x[1], x[2]))

    # Initialize the output grid as a 3x3 array filled with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Populate the output grid with the non-zero pixels
    for i in range(min(len(non_zero_pixels),9)):
        row = i // 3
        col = i % 3
        output_grid[row][col] = non_zero_pixels[i][0]

    return output_grid
```
