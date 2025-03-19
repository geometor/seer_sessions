# cdecee7f • 020 • refine_coder

---
```python
"""
1.  **Identify Non-Zero Pixels:** Locate all pixels in the input grid with a non-zero value (i.e., not white).
2.  **Extract and Order by Column (Uniquely):** Record these non-zero pixels. Maintain their original input value, and order them based on the column in which they appear in the input grid, left-to-right. If there are other pixels in a column already represented, ignore.
3.  **Create Output Grid:** Construct a 3x3 output grid.
4. **Populate:** Fill the 3x3 output grid row by row, left to right.
    Use the ordered, unique sequence of non-zero pixels. Fill any remaining cells with 0.
"""

import numpy as np

def get_nonzero_by_column(input_grid):
    """Extracts non-zero pixels, preserving column order and removing duplicates within columns."""
    non_zero_pixels = []
    columns_added = set()

    for j in range(input_grid.shape[1]):
        for i in range(input_grid.shape[0]):
            value = input_grid[i,j]
            if value != 0 and j not in columns_added:
                non_zero_pixels.append(value)
                columns_added.add(j)
    return non_zero_pixels

def transform(input_grid):
    """Transforms a 10x10 input grid into a 3x3 output grid by extracting and
    rearranging non-zero pixels based on column order."""

    # Initialize an empty 3x3 output grid filled with zeros.
    output_grid = np.zeros((3, 3), dtype=int)

    # Find and order non-zero pixels by their column position.
    non_zero_pixels = get_nonzero_by_column(input_grid)

    # Fill the output grid with the ordered non-zero pixel values.
    k = 0
    for i in range(3):
        for j in range(3):
            if k < len(non_zero_pixels):
                output_grid[i, j] = non_zero_pixels[k]
                k += 1

    return output_grid
```
