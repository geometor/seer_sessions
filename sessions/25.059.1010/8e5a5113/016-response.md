# 8e5a5113 • 016 • example_3 • investigate_coder

---
```python
"""
The input grid is divided into two sections: a left section (first four columns) and a right section (remaining columns).
The output grid is constructed as follows:
1. The left section of the input grid is copied to the output grid.
2. A mirrored version of the left section is inserted to columns 5-7.
3. An inverted version of the left section is placed in the final four columns.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    # Initialize the output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Copy the left section (first four columns) to the output
    left_section = input_grid[:, :4]
    output_grid[:, :4] = left_section

    # 2. Mirror the left Section and add
    mirrored_section = np.flip(left_section, axis=(0, 1))
    output_grid[:, 4:7] = mirrored_section[:, 1:]

    # 3. Invert Left section and insert in final three columns.
    inverted_section = np.flip(left_section, axis=1)
    output_grid[:, 7:11] = inverted_section

    return output_grid
```
