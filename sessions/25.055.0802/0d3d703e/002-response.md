# 0d3d703e • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a simple color-to-color (or digit-to-digit) substitution.  The input grid is transformed into the output grid by replacing each digit in the input with a corresponding digit according to the following mapping:

1.  Input digit 3 (green) is replaced with digit 4 (yellow).
2.  Input digit 1 (blue) is replaced with digit 5 (gray).
3.  Input digit 2 (red) is replaced with digit 6 (magenta).

The grid structure (3x3) remains unchanged. It's a direct one-to-one mapping of cell values based on their original value, not their position.
"""

import numpy as np

def transform(input_grid):
    """Applies a color mapping to an input grid."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Define the color mapping.
    color_map = {
        3: 4,  # Green to Yellow
        1: 5,  # Blue to Gray
        2: 6   # Red to Magenta
    }

    # Iterate through the grid and apply the mapping.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid
```

