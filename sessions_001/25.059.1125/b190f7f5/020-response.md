# b190f7f5 • 020 • refine_coder

---
```python
"""
Transforms an input grid into a larger output grid by expanding each pixel into a 4x4 block, including the background pixels (value 0).
"""

import numpy as np

def transform(input_grid):
    # Determine Output Grid Size
    input_height, input_width = input_grid.shape
    output_height = input_height * 4
    output_width = input_width * 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Pixel Expansion: Includes background pixels
    for y in range(input_height):
        for x in range(input_width):
            pixel_value = input_grid[y, x]
            # Calculate output coordinates
            out_x = x * 4
            out_y = y * 4

            # Create 4x4 block, even for background
            output_grid[out_y:out_y+4, out_x:out_x+4] = pixel_value

    return output_grid
```
