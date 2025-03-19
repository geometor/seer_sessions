# dae9d2b5 • 002 • example_5 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Non-White Pixels:** Locate all pixels in the input grid that are not white (0).
2.  **Color Replacement:** Change the color of all identified non-white pixels to magenta (6). Keep white pixels as white.
3.  **Grid Resizing:** Resize the grid to a 3x3 grid.
4. **Positional mapping**:
    *   Iterate through the original grid's rows.
    *    If a non-white pixel is present in the any position in a row, the corresponding row is magenta.
        Otherwise the row is white.
    *    Combine the new color with the new dimensions to generate output.
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid according to the described rule."""

    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)

    # Positional mapping and color replacement
    for i in range(3):
        if i < rows:
           if np.any(input_grid[i] != 0):
               output_grid[i,:] = 6

    return output_grid
```
