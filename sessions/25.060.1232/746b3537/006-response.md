# 746b3537 • 006 • example_2 • investigate_coder

---
```python
"""
Extracts the first row of the input grid and presents it as the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 2D grid by extracting its first row.

    Args:
        input_grid (list of lists): A 2D grid represented as a list of lists.

    Returns:
        list of lists: A new 2D grid consisting of only the first row of the input.
    """
    # Initialize output_grid as a list containing the first row of the input grid
    output_grid = [input_grid[0]]

    return output_grid
```

