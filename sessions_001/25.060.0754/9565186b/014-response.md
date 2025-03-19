# 9565186b • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is to replace all azure (8) pixels in the input grid with gray (5) pixels, while keeping the red (2) pixels unchanged. The grid structure remains the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing azure pixels with gray pixels.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the locations of azure pixels (value 8).
    azure_pixels = (output_grid == 8)

    # Replace azure pixels with gray pixels (value 5).
    output_grid[azure_pixels] = 5

    return output_grid
```
