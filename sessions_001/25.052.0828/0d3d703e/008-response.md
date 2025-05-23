# 4-0d3d703e • 008 • refine_code - CODE

---
```python
"""
Transformation Rule:

1.  **Object Identification:** The input grid consists of vertical lines (columns) of uniform color. Each column is an object.

2.  **Color Transformation:** Each color in the input grid is consistently mapped to a different color in the output grid. The positions and shapes of the objects (columns) remain identical; only the colors change.

3. **Color Mapping:**
    - from example 1
    - 9 (Maroon) -> 8(Azure)
    - 4 (Yellow) -> 3(Green)
    - 2 (Red) -> 6(Magenta)
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a color substitution rule, preserving structure.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Define the color mapping based on the observed transformations.
    color_map = {
        9: 8,  # Maroon -> Azure
        4: 3,  # Yellow -> Green
        2: 6,  # Red -> Magenta
    }

    # Iterate through each cell and apply the color mapping.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            original_color = output_grid[i, j]
            if original_color in color_map:
                output_grid[i, j] = color_map[original_color]

    return output_grid
```

