```python
"""
The transformation rule takes each non-zero pixel in the input grid and expands it into a cross shape in the output grid. The cross is centered on the corresponding position of the original pixel, and its arms extend to the edges of the output grid. The color of the cross matches the original pixel's color. The output grid's dimensions are determined based on input dimensions and must be odd.
"""

import numpy as np

def get_output_dimensions(input_grid):
    """Determine output dimensions based on input.  Finds next odd dimension that will fit all crosses."""
    rows, cols = input_grid.shape
    max_dim = max(rows, cols)
    output_dim = max_dim * 2 + 1

    if (output_dim % 2 ==0):
       output_dim+=1

    return output_dim


def transform(input_grid):
    """Transforms the input grid according to the cross-expansion rule."""

    # Determine output grid size
    output_dim = get_output_dimensions(input_grid)

    output_grid = np.zeros((output_dim, output_dim), dtype=int)

    input_rows, input_cols = input_grid.shape

    # Iterate through input pixels
    for r in range(input_rows):
        for c in range(input_cols):
            pixel_value = input_grid[r, c]

            # Check for non-zero pixel
            if pixel_value != 0:
                # Horizontal Expansion
                output_grid[r*2+1, :] = pixel_value
                # Vertical Expansion
                output_grid[:, c*2+1] = pixel_value

    return output_grid
```