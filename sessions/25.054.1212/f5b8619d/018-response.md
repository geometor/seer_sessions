# f5b8619d • 018 • refine_coder

---
```python
"""
Expands each cell in the input grid into a 2x2 block in the output grid. The
top-left cell of the 2x2 block matches the input cell's value. If the input
cell is white (0), the 2x2 block is [0, 8; 8, 0]. Otherwise, the 2x2 block is
[input, 8; 8, 8].
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for i in range(input_height):
        for j in range(input_width):
            # Get the original cell value
            original_value = input_grid[i, j]

            # Calculate the top-left corner of the 2x2 block in the output grid
            output_row = i * 2
            output_col = j * 2

            # Assign values to the 2x2 block
            if original_value == 0:  # White
                output_grid[output_row, output_col] = 0      # Top-left
                output_grid[output_row, output_col + 1] = 8  # Top-right
                output_grid[output_row + 1, output_col] = 8  # Bottom-left
                output_grid[output_row + 1, output_col + 1] = 0  # Bottom-right
            else:  # Non-white
                output_grid[output_row, output_col] = original_value  # Top-left
                output_grid[output_row, output_col + 1] = 8      # Top-right
                output_grid[output_row + 1, output_col] = 8      # Bottom-left
                output_grid[output_row + 1, output_col + 1] = 8  # Bottom-right

    return output_grid
```

