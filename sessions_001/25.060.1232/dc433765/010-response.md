# dc433765 • 010 • example_2 • investigate_coder

---
```python
"""
Moves the green (3) pixel one position to the right, leaving other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Moves the green (3) pixel one position to the right, leaving other pixels unchanged.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the position of the green pixel (3).
    green_pos = None
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 3:
                green_pos = (r, c)
                break
        if green_pos:
            break

    # If a green pixel is found, move it one position to the right.
    if green_pos:
        r, c = green_pos
        output_grid[r,c] = 0 # zero out the position.
        new_c = min(cols -1, c + 1)  # Ensure new column is within bounds
        output_grid[r, new_c] = 3

    return output_grid
```

