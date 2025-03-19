# ed36ccf7 • 012 • refine_coder

---
```python
"""
The transformation rule identifies the presence of magenta (6) pixels within columns of the input grid. If a column contains at least one magenta pixel, the entire corresponding column in the output grid is filled with magenta. If a column does not contain any magenta pixels, it remains unchanged (all white/0) in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of magenta pixels in columns.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Iterate through each column of the input grid
    for j in range(input_grid.shape[1]):
        # Check if the current column contains any magenta pixels
        if 6 in input_grid[:, j]:
            # Fill the entire corresponding column in the output grid with magenta
            output_grid[:, j] = 6

    return output_grid.tolist()
```

