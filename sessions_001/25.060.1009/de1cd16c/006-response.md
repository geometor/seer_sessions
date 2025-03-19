# de1cd16c • 006 • refine_coder

---
```python
"""
1. Examine the input grid and identify all unique colors present.
2. The output is a 1x1 grid.
3. The color of the output grid is one of the colors present in the input grid. If a non-white color exists, use this color.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Identify all unique colors present in the input grid
    unique_colors = np.unique(input_grid)

    # Initialize the output color to white (0)
    output_color = 0

    # Iterate through unique colors and set the output color to the first non-white color found
    for color in unique_colors:
        if color != 0:
            output_color = color
            break

    # Create a 1x1 output grid with the determined output color
    output_grid = np.array([[output_color]])

    return output_grid
```
