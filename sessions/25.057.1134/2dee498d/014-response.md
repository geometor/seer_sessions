# 2dee498d • 014 • example_3 • investigate_coder

---
```python
"""
The transformation extracts the first two columns of the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the appropriate dimensions.
    # The output grid has the same height as the input grid and a width of 2.
    output_grid = np.zeros((input_grid.shape[0], 2), dtype=int)

    # Copy the first two columns of the input grid to the output grid.
    output_grid[:, 0] = input_grid[:, 0]
    output_grid[:, 1] = input_grid[:, 1]
    
    return output_grid
```
