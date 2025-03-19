# fafffa47 • 022 • example_4 • investigate_coder

---
```python
"""
The transformation rule involves compressing the input grid vertically by a factor of two and mapping colors. Each pair of rows in the input becomes a single row in the output. Maroon (9) is mapped to red (2), blue(1) to white(0), and white (0) remains white (0).
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height // 2
    output_width = input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels 
    for i in range(output_height):
        for j in range(output_width):
            # Consider two rows at a time from the input_grid
            val1 = input_grid[2*i, j]
            val2 = input_grid[2*i + 1, j]

            # color mapping
            if val1 == 9 or val2 == 9:
                output_grid[i,j] = 2 # maroon becomes red
            elif val1 == 1 or val2 == 1:
                output_grid[i,j] = 0 # blue becomes white
            else:
                output_grid[i,j] = 0 # default to white

    return output_grid
```
