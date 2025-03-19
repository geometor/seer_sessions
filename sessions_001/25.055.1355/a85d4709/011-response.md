# a85d4709 • 011 • refine_coder

---
```python
"""
The transformation rule is extremely simple:

1.  **Change all pixels:** Iterate through every pixel in the input grid.
2.  **Recolor:** Change the color of each pixel from azure (8) to green (3).
3.  **Preserve shape:** The dimensions of the output grid match the dimensions of the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # change output pixels 
    output_grid[:] = 3

    return output_grid.tolist()
```
