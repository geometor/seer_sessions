# a85d4709 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation rule is a color substitution: gray (5) becomes red (2), and white (0) becomes yellow (4).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified color substitution rule.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid.
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Apply the color substitution rules.
            if output_grid[i, j] == 5:  # If gray
                output_grid[i, j] = 2  # Change to red
            elif output_grid[i,j] == 0: # if white
                output_grid[i,j] = 4 # Change to yellow

    return output_grid
```
