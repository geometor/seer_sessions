# b190f7f5 • 016 • example_3 • investigate_coder

---
```python
"""
Transforms a smaller input grid into a larger output grid by expanding and mirroring non-zero pixels.
"""

import numpy as np

def transform(input_grid):
    # Determine Output Grid Size
    input_height, input_width = input_grid.shape
    new_width = 2 * input_width
    new_height = 4 * input_height
    output_size = max(new_width, new_height)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Center and Expand
    center_x = output_size // 2
    center_y = output_size // 2

    # Pixel Expansion and Mirroring
    for y in range(input_height):
        for x in range(input_width):
            pixel_value = input_grid[y, x]
            if pixel_value != 0:
                # Calculate output coordinates based on centering
                out_x = center_x - input_width + x*2
                out_y = center_y - input_height*2 + y*4

                # Create 2x2 block
                output_grid[out_y:out_y+2, out_x:out_x+2] = pixel_value
                
                #mirror to create 4x4 block
                output_grid[out_y+2:out_y+4, out_x:out_x+2] = pixel_value
                output_grid[out_y:out_y+2, out_x+2:out_x+4] = pixel_value
                output_grid[out_y+2:out_y+4, out_x+2:out_x+4] = pixel_value

    return output_grid
```
