# e26a3af2 • 012 • refine_coder

---
```python
"""
The transformation rule is: Copy all non-black pixels from the input grid to the output grid, preserving their original positions and colors. Black pixels remain black. In effect, the transformation preserves all connected components formed by colored pixels, leaving empty (black) regions unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid, filled with zeros (black).
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input grid.
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_color in enumerate(row):
            # Check if the pixel is non-black.
            if pixel_color != 0:
                # Copy the pixel's color to the corresponding position in the output grid.
                output_grid[row_index, col_index] = pixel_color

    return output_grid
```

