# e8593010 • 016 • example_3 • investigate_coder

---
```python
"""
Preserve Gray: Copy all gray (5) pixels from the input grid to the same positions in the output grid.

Transform White: For each white (0) pixel in the input grid:
    If the white cell is at an even row and an even column, replace with red(2)
    If the white cell is at an odd row and an odd column, replace with green(3)
    If the white cell is at an odd row and an even column, OR an even row and an odd column, replace with blue(1)
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    output_grid = np.copy(input_grid)  # Start with a copy to preserve gray pixels
    rows = len(input_grid)
    cols = len(input_grid[0])

    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] == 0:  # Check for white pixels
                if r % 2 == 0 and c % 2 == 0:
                    output_grid[r][c] = 2  # Even row, even column -> red
                elif r % 2 != 0 and c % 2 != 0:
                    output_grid[r][c] = 3  # Odd row, odd column -> green
                else:
                    output_grid[r][c] = 1  # Odd/even or even/odd -> blue

    return output_grid
```
