# 5582e5ca • 008 • refine_coder

---
```python
"""
If the input grid contains any yellow pixels, the output grid is the same size as the input, and filled entirely with yellow pixels.
If the input grid contains no yellow pixels, the output grid is the same size as the input, and filled entirely with black pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input_grid
    output_grid = np.zeros_like(input_grid)

    # Check for the presence of yellow (4) in the input_grid
    if np.any(input_grid == 4):
        # If yellow is present, fill the output_grid with yellow
        output_grid[:] = 4
    # Else, output_grid remains all zeros (black), as initialized.

    return output_grid
```

