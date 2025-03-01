# b1948b0a • 002 • example_1 • investigate_coder

---
```python
"""
Iterate through each pixel in the input grid.
If the color is magenta (6), change it to red (2) in the output grid.
If the color is orange (7), keep it as orange (7) in the output grid.
Maintain the original position of each pixel within the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified color mapping rule.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Check the color and apply the transformation
            if input_grid[i][j] == 6:
                output_grid[i][j] = 2
            elif input_grid[i][j] == 7:
                output_grid[i][j] = 7
            else:
                output_grid[i][j] = input_grid[i][j]  # in case there are other colors, copy them as is
    return output_grid
```

