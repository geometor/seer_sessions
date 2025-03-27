```python
"""
The input grid is transformed into an output grid by expanding each pixel in the input grid into a 2x2 block in the output grid. The expansion involves both horizontal and vertical reflection to generate the output pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to the output grid by expanding each pixel to a 2x2 block and applying horizontal and vertical reflections.
    """
    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Expand and Reflect: For each pixel, create a 2x2 block.
    for r in range(rows):
        for c in range(cols):
            # Original
            output_grid[r, c] = input_np[r,c]

            #horizontal
            output_grid[r, 2*cols - 1 - c] = input_np[r,c]

            # Vertical
            output_grid[2*rows-1-r, c] = input_np[r,c]

            # Both
            output_grid[2*rows-1-r, 2*cols -1 -c] = input_np[r,c]

    # Expand: duplicate the created row
    for r in range(rows):
      output_grid[2*r,:] = output_grid[r,:]
      output_grid[2*r+1,:] = output_grid[r,:]

    return output_grid.tolist()
```