# a85d4709 • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule replaces all pixel values in the input grid with the value 3, effectively changing the entire grid to green.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change all output pixel values to 3
    output_grid[:] = 3

    return output_grid
```
