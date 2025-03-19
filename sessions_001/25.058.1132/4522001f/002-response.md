# 4522001f • 002 • example_2 • investigate_coder

---
```python
"""
Transforms a 3x3 input grid into a 9x9 output grid based on the following rules:

1.  **Identify Objects:** Locate all contiguous regions of green (3) and red (2) pixels within the 3x3 input grid.
2.  **Red Removal:** Note the existance/location of any red pixels and remove them from consideration for expansion.
3.  **Green Expansion:**
    *   The original 3x3 input grid is embiggened to a 9x9 grid.
    *   Imagine extending lines outwards based on the input grid borders to create quadrants in the output grid.
    *    Any area in the input grid which contains one or more green pixel expands to fully fill that region.
    *   Any green expands to fill a 3x3 block for each of the original pixel locations.
    *    Empty areas are filled with the default white.
4.  **Output:** Construct the 9x9 output grid based on the expansion rules.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    input_grid = np.array(input_grid)
    output_grid = np.zeros((9, 9), dtype=int)

    # Iterate through the input grid
    for i in range(3):
        for j in range(3):
            # If the pixel is green, expand it
            if input_grid[i, j] == 3:
                output_grid[i*3:(i+1)*3, j*3:(j+1)*3] = 3

    return output_grid.tolist()
```
