# a85d4709 • 022 • example_4 • investigate_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Initialization:** Start with a 3x3 input grid.
2.  **Iteration:** For each pixel in the input grid:
    *   **Conditional Check:**
        *   If the pixel's value is 5 (gray), change it to 3 (green) in the output grid.
        *   If the pixel's value is 0 (white), change it to 4 (yellow) in the output grid.
3.  **Output:** The result is a 3x3 output grid where each pixel's color has been transformed according to the above rule, maintaining the original grid structure.

In simpler terms, the program replaces all gray pixels with green pixels and all white pixels with yellow pixels, keeping the positions the same.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    # Initialize the output grid with the same dimensions as the input.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of the input grid.
    for i in range(rows):
        for j in range(cols):
            # Apply the transformation rules based on the input pixel's value.
            if input_grid[i, j] == 5:  # If gray
                output_grid[i, j] = 3  # Change to green
            elif input_grid[i, j] == 0:  # If white
                output_grid[i, j] = 4  # Change to yellow
            else:
                output_grid[i,j] = input_grid[i,j] # transfer others

    return output_grid
```
