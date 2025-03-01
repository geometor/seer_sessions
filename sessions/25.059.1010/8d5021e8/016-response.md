# 8d5021e8 • 016 • example_3 • investigate_coder

---
```python
"""
The input grid is expanded and reflected to create the output grid. The input grid (3x2) is expanded by a factor of 3 vertically and 2 horizontally, resulting in a 9x4 output grid. The expansion involves reflecting the original pattern along both the horizontal and vertical axes.
"""

import numpy as np

def transform(input_grid):
    # Initialize the input grid as a NumPy array
    input_array = np.array(input_grid)

    # Get dimensions of the input grid
    input_rows, input_cols = input_array.shape

    # Determine expansion factors (output grid is 9x4)
    vertical_expansion = 3  # 9 / 3
    horizontal_expansion = 2 # 4 / 2

    # Create reflected versions of the input array
    reflected_horizontal = np.fliplr(input_array)
    reflected_vertical = np.flipud(input_array)
    reflected_both = np.flipud(np.fliplr(input_array))

    # Concatenate horizontally to double the width
    row_1 = np.concatenate((input_array, reflected_horizontal), axis=1)

    # reflect the vertical
    row_2 = np.flipud(row_1)

    # build output in thirds
    output_array = np.concatenate((row_1, row_2, row_1), axis=0)

    return output_array.tolist()
```
