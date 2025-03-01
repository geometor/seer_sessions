# d90796e8 • 010 • example_2 • investigate_coder

---
```python
"""
1.  Identify all pixels with the color green (3).
2.  Change the color of these identified green pixels to azure (8).
3.  Identify all pixels that are the color red (2).
4.  Change the color of the identified red pixels to white(0).
5.  Preserve all other pixels (gray (5) and white (0)) in their original state and positions.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified color change rules."""
    output_grid = np.copy(input_grid)  # Create a copy to modify

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Change green (3) to azure (8)
            if output_grid[i, j] == 3:
                output_grid[i, j] = 8
            # Change red (2) to white (0)
            elif output_grid[i, j] == 2:
                output_grid[i, j] = 0

    return output_grid
```

