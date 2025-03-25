```python
"""
1.  **Preservation:** The original blue (1), red (2), magenta (6), and azure (8) pixels in the input grid remain in their original positions in the output grid.

2.  **Yellow Pixel Placement (Conditional on Red):** For each red (2) pixel in the input grid, place three yellow (4) pixels in the output grid as follows:
    *   One yellow pixel one row *below* the red pixel.
    *   One yellow pixel one row *below* and two columns *to the left* of the red pixel.
    *   One yellow pixel one row *below* and two columns *to the right* of the red pixel.

3.  **Orange Pixel Placement (Conditional on Blue):** For each blue (1) pixel in the input grid, place three orange (7) pixels in the output grid as follows:
    *   One orange pixel one row *below* the blue pixel.
    *   One orange pixel in the same row, one column *to the left* of the blue pixel.
    *   One orange pixel in the same row, one column *to the right* of the blue pixel.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find red and blue pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:  # Red pixel
                # Add yellow pixels below, two to the left and two to the right RELATIVE to the red pixel
                if r + 1 < rows:
                    output_grid[r + 1, c] = 4  # One row below
                    if c - 2 >= 0:
                        output_grid[r + 1, c - 2] = 4  # One row below, two columns left
                    if c + 2 < cols:
                        output_grid[r + 1, c + 2] = 4  # One row below, two columns right
            elif input_grid[r, c] == 1:  # Blue pixel
                # Add orange pixels below, left, and right RELATIVE to the blue pixel
                if r + 1 < rows:
                    output_grid[r + 1, c] = 7  # One row below
                if c - 1 >= 0:
                    output_grid[r, c - 1] = 7  # Same row, one column left
                if c + 1 < cols:
                    output_grid[r, c + 1] = 7  # Same row, one column right

    return output_grid
```
