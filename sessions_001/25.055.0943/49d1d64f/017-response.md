# 49d1d64f • 017 • refine_coder

---
```python
"""
The transformation rule is a simple pixel-wise scaling. Each pixel in the input grid is replaced by a 3x3 block of pixels of the same color in the output grid. This effectively magnifies the input image by a factor of 3 in both dimensions. The position of the magnified pixel block corresponds directly to the original pixel's position in the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by scaling up each pixel to a 3x3 block.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Use numpy's kron function for efficient scaling.
    # Create a 3x3 matrix of ones.
    scale_matrix = np.ones((3, 3))
    # Apply the Kronecker product between the input grid and the scale matrix.
    output_grid = np.kron(input_grid, scale_matrix)

    return output_grid
```
