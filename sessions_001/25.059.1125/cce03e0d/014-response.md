# cce03e0d • 014 • refine_coder

---
```python
"""
The input grid is replicated three times to create a larger output grid. The dimensions of the output grid are exactly three times the dimensions of the input grid (width * 3 and height * 3). The output grid is initially filled with zeros (black). The original input grid is then copied to three locations in the output:

1.  **Top-Right Corner:** The first copy is placed at the top-right corner of the output grid.
2.  **Bottom-Left Corner:** The second copy is placed at the bottom-left corner of the output grid.
3.  **Bottom-Right Corner:** The third copy is placed at the bottom-right corner of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Determine the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Calculate the dimensions of the output grid (3 times the input).
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize the output grid with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place the first copy (top-right corner).
    output_grid[0:input_height, (output_width - input_width):output_width] = input_grid

    # Place the second copy (bottom-left corner).
    output_grid[(output_height - input_height):output_height, 0:input_width] = input_grid

    # Place the third copy (bottom-right corner).
    output_grid[(output_height - input_height):output_height, (output_width - input_width):output_width] = input_grid

    return output_grid
```

