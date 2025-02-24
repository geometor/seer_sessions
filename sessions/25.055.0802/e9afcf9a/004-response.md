# e9afcf9a • 004 • refine_coder

---
```python
"""
1.  **Preserve Dimensions:** The output grid has the same dimensions as the input grid.

2.  **Row-wise Transformation:** Each row of the input grid is transformed independently.

3. **Identify Row's initial color:** For each row, use the color of the first pixel of that row in the input grid as color_1.

4.  **Alternating Pattern:** Each row in the output grid consists of an alternating pattern of two colors.

5.  **Determine Color 1:** The first pixel of each output row has the same color as the first pixel of the corresponding input row (color_1).

6.  **Determine Color 2:**
    - If color_1 is *not* 9, the second color (color_2) used in the alternating pattern is 9.
    - If color_1 *is* 9, then the second color (color_2) will match the color value of the *second* pixel of the input row.

7. **Apply alternating colors:** Apply the two colors on each row in an alternating pattern
    - odd numbered columns get color_1
    - even numbered columns get color_2.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for r in range(rows):
        # Determine color_1 (first pixel's color)
        color_1 = input_grid[r, 0]

        # Determine color_2 based on color_1
        if color_1 != 9:
            color_2 = 9
        else:
            color_2 = input_grid[r, 1]  # Second pixel's color if the first is 9

        for c in range(cols):
            # Apply alternating colors
            if c % 2 == 0:  # Even columns
                output_grid[r, c] = color_1
            else:  # Odd columns
                output_grid[r, c] = color_2

    return output_grid
```

