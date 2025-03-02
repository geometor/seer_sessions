# ed36ccf7 • 014 • refine_coder

---
```python
"""
The transformation rule involves these steps:

1.  **Count Magenta Pixels:** Determine the number of magenta (6) pixels in the input grid.
2.  **Determine Output Dimensions:** The output grid always has a width of 3. The height of the output grid is the same as the height of the input grid.
3.  **Place Magenta Pixels:** Place the magenta pixels in the first column of the output grid, starting from the top. The number of magenta pixels placed is equal to the number of magenta pixels in the input, not to exceed the height of the output.
4.  **Fill with White:** Fill all remaining cells in the output grid with white (0) pixels.
"""

import numpy as np

def count_pixels(grid, color):
    """Counts the number of pixels of a specific color in a grid."""
    return np.sum(grid == color)

def transform(input_grid):
    # Count Magenta Pixels
    magenta_count = count_pixels(input_grid, 6)

    # Determine Output Dimensions
    output_height = input_grid.shape[0]
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Place Magenta Pixels
    for i in range(min(magenta_count, output_height)):
        output_grid[i, 0] = 6

    # Fill with White (remaining cells are already 0, so this step is implicit)

    return output_grid
```

