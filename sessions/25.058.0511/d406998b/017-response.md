# d406998b • 017 • refine_coder

---
```python
"""
The input grid, which consists of a single rectangle of magenta color, 
is transformed into an output grid of the same dimensions. 
The output grid is filled entirely with the color red.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # change all pixels of the output_grid to red (color 2)
    output_grid[:] = 2

    return output_grid
```

