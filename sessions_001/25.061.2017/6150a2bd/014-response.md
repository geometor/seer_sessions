# 6150a2bd • 014 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves inverting the positions of colored pixels in a 3x3 grid. Each colored pixel in the input grid is moved to its inverse position in the output grid, calculated by subtracting its row and column indices from 2. The rest of the pixels are filled with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by inverting the positions of colored pixels.
    """
    # Initialize output_grid as a 3x3 grid filled with white (0).
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the input grid to find colored pixels (non-white).
    for row in range(3):
        for col in range(3):
            if input_grid[row][col] != 0:
                # Calculate the inverted position.
                inverted_row = 2 - row
                inverted_col = 2 - col
                # Place the color in the inverted position in the output grid.
                output_grid[inverted_row][inverted_col] = input_grid[row][col]

    return output_grid
```
