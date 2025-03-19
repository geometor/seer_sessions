# 5582e5ca • 012 • refine_coder

---
```python
"""
The transformation rule involves a one-to-one mapping of input grid colors to output grid colors.  Each example input consists of a grid of a single color.  The output is the same size and shape as the input, but all pixels are changed to a different, single color. The color mapping observed so far is:

*   Blue (1) in the input becomes Maroon (9) in the output.
*   Gray (5) in the input becomes Black (0) in the output.
*   Green (3) in the input becomes Yellow (4) in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a one-to-one color mapping.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    # Define the color mapping
    color_mapping = {
        1: 9,
        5: 0,
        3: 4,
    }

    # Get the input color (assuming the grid is uniform)
    input_color = input_grid[0, 0]

    # Get the corresponding output color from the mapping
    output_color = color_mapping.get(input_color)

    # Create an output grid of the same shape, filled with the output color
    output_grid = np.full(input_grid.shape, output_color)

    return output_grid
```

