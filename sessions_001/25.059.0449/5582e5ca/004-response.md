# 5582e5ca • 004 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to identify the color yellow (represented by the digit 4) in the input grid and fill an output grid of the same dimensions with this color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling an output grid of the same dimensions with the color yellow (4).
    """
    # Initialize output_grid with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Find the target color (yellow, represented by 4)
    target_color = 4

    # Fill the output grid with the target color
    output_grid[:] = target_color

    return output_grid
```

