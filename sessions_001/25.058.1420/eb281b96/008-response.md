# eb281b96 • 008 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to "double the input grid vertically."
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating it vertically.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Replicate the input grid vertically
    output_grid = np.concatenate((input_grid, input_grid), axis=0)

    return output_grid
```

