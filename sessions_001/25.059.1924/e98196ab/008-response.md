# e98196ab • 008 • refine_coder

---
```python
"""
The transformation rule identifies and preserves azure (8) pixels in the input, setting all other pixels to white (0). The number and arrangement of azure pixels in the input grid *exactly* matches the number and arrangement of azure pixels the output grid. All pixels that are not azure in the input grid are replaced with white pixels in the output grid. Azure pixels form a contiguous block in the input, and it seems like the whole block is an object and transferred.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Iterate through the input grid
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            # If the pixel is azure, copy it to the output grid
            if input_grid[r, c] == 8:
                output_grid[r, c] = 8

    return output_grid
```

