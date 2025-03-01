# ed36ccf7 • 010 • refine_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Identify Object:** Find the contiguous block of magenta (color 6) pixels. This constitutes the primary object.
2.  **Identify Context:** Consider the 3x3 grid. The magenta object is always, in these training example, surrounded by white.
3.  **Rotate Object:** The magenta pixel moves one position counter-clockwise around the perimeter of the 3x3 grid. The previously occupied space become white (0).
"""

import numpy as np

def find_magenta_pixel(grid):
    """Finds the coordinates of the magenta pixel."""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == 6:
                return (i, j)
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the magenta pixel
    magenta_pos = find_magenta_pixel(input_grid)

    if magenta_pos is None:
        return output_grid  # No magenta pixel found, return original grid

    magenta_row, magenta_col = magenta_pos

    # Define the possible positions in counter-clockwise order
    positions = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

    # Find the current position index
    current_index = positions.index((magenta_row, magenta_col))

    # Calculate the next position index (counter-clockwise)
    next_index = (current_index - 1) % len(positions)

    # Get the next position coordinates
    next_row, next_col = positions[next_index]

    # Clear the current magenta pixel and set the next position
    output_grid[magenta_row, magenta_col] = 0
    output_grid[next_row, next_col] = 6


    return output_grid
```
