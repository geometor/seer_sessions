# 9565186b • 008 • example_2 • investigate_coder

---
```python
"""
Iterate through each pixel in the input grid. If the color is 1 (blue), keep the color unchanged. 
If the color is 8, 3, or 2 (azure, green, or red), change the color to 5 (gray).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified color change rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for i in range(rows):
        for j in range(cols):
            # Check the color and apply the transformation rule
            if input_grid[i, j] == 1:  # Blue remains unchanged
                output_grid[i, j] = 1
            elif input_grid[i, j] in [8, 3, 2]:  # Azure, Green, Red change to Gray
                output_grid[i, j] = 5

    return output_grid
```
