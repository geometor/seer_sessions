# a85d4709 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation involves mapping the input grid's pixel colors (0 and 5) to a new set of colors (2, 3, and 4) in the output grid. The colors are placed in the output grid in reverse order of their appearance on a diagonal (top-right to bottom-left) in the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Mapping dictionary for input to output colors, in reverse order
    color_map = {
        0: [3, 4, 2],  # white to green, yellow, red
        5: [3, 4, 2]   # gray to green, yellow, red
    }

    # Counters for color sequence
    color_index_0 = 0
    color_index_5 = 0
    
    # Iterate through the grid in reverse diagonal order (top-right to bottom-left)
    for i in range(rows):
      for j in range(cols):
          if (i+j) == (rows -1):
            # Get input pixel value
            input_pixel = input_grid[j,i]

            # Get corresponding output color from the mapping
            if input_pixel == 0:
                output_color = color_map[0][color_index_0]
                color_index_0 = (color_index_0 + 1) % 3

            elif input_pixel == 5:
                output_color = color_map[5][color_index_5]
                color_index_5 = (color_index_5 + 1) % 3

            # set value in output grid
            output_grid[i,j] = output_color

    return output_grid
```
