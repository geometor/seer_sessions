# 9565186b • 023 • refine_coder

---
```python
"""
The transformation rule involves increasing the dimensions of a single rectangular object of uniform color.

1. Identify the Object: The input consists of a single rectangular object of a uniform color.
2. Determine Output Dimensions:
    *   Output Width: Double the input width.
    *   Output Height: Double the minimum dimension of the input.
3. Create Output: Create a new rectangle with the calculated output width and height, filled with the same color as the input object.

This can be summarized more concisely as: Double the width of the rectangle, double the smaller dimension for the new height, and preserve the color.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Get the color of the input object
    color = input_grid[0, 0]

    # Get input dimensions
    input_height, input_width = input_grid.shape

    # Calculate output dimensions
    output_width = input_width * 2
    output_height = min(input_height, input_width) * 2

    # Create output grid filled with the same color
    output_grid = np.full((output_height, output_width), color)

    return output_grid
```
