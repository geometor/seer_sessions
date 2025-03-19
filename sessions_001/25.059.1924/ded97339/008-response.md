# ded97339 • 008 • refine_coder

---
```python
"""
Create an output grid with the same dimensions as the input grid, filled entirely with white (0) pixels. Iterate through each pixel of the input grid. If a pixel is azure (8), draw a vertical strip of azure pixels in the output grid. The strip starts at the row of the found azure pixel and extends to the last row of the output grid. The column remains the same. The pixels which are not part of any azure strips, initiated by the rule above, should all be white (color 0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as all white with the same dimensions as input_grid.
    output_grid = np.zeros_like(input_grid)

    # Iterate through all pixels in the input grid.
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # Check if the pixel is azure (8).
            if pixel_value == 8:
                # Create a vertical strip downwards.
                for r in range(row_index, len(input_grid)):
                    output_grid[r][col_index] = 8

    return output_grid
```

