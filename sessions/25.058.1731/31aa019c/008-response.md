# 31aa019c • 008 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  The output is always an 11x11 grid filled with white (0).
2.  Regardless of the input, a 3x3 red (2) square with a yellow (4) center is placed at a fixed position in the output grid.
3.  The top-left corner of the 3x3 square is located at row 4, column 4 of the output grid (making the center at row 5, column 5).
4. Any colored pixels in the input grid are disregarded with respect to placement or any other consideration in the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 11x11 with all white (0)
    output_grid = np.zeros((11, 11), dtype=int)

    # Create the 3x3 red square (2)
    block_start_row = 4
    block_start_col = 4

    for i in range(3):
        for j in range(3):
            row = block_start_row + i
            col = block_start_col + j
            output_grid[row, col] = 2

    # Change center pixel to yellow (4)
    output_grid[5, 5] = 4

    return output_grid
```

