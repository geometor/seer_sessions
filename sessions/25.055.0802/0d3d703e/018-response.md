# 0d3d703e • 018 • refine_coder

---
```python
"""
The transformation rule involves a direct color substitution. The input and output grids maintain the same dimensions, and only specific colors are altered. The following color substitutions are consistently applied:

1.  All gray (5) pixels in the input grid are replaced with blue (1) pixels in the output grid.
2.  All azure (8) pixels in the input grid are replaced with maroon (9) pixels in the output grid.
3.  All magenta (6) pixels in the input grid are replaced with red (2) pixels in the output grid.
4.  All other colors present in the input grid remain unchanged in the output grid.

There are no changes to positions, sizes, or any other geometrical transformations; only colors are changed according to the defined mapping.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid to preserve dimensions.
    output_grid = np.copy(input_grid)

    # Define the color mapping for substitutions.
    color_map = {
        5: 1,  # Gray to Blue
        8: 9,  # Azure to Maroon
        6: 2   # Magenta to Red
    }

    # Iterate through each cell in the output_grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the current cell's color is in the color_map.
            if output_grid[i, j] in color_map:
                # Apply the color substitution based on the color_map.
                output_grid[i, j] = color_map[output_grid[i, j]]

    # Return the transformed grid.
    return output_grid
```

