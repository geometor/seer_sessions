# 662c240a • 026 • example_4 • investigate_coder

---
```python
"""
Extract the top 3x3 subgrid from the input grid to create the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top 3x3 subgrid from the input grid.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The 3x3 subgrid extracted from the input grid.
    """
    # Initialize the output grid as a copy of the top 3x3 section of the input.
    output_grid = input_grid[:3, :3].copy()

    return output_grid
```
