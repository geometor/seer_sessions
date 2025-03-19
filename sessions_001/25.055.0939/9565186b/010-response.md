# 9565186b • 010 • refine_coder

---
```python
"""
Replace colors 8, 2, and 3 with color 5, while keeping other colors unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing colors 8, 2 and 3 with 5.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Replace colors 8, 2, and 3 with 5.
    output_grid[output_grid == 8] = 5
    output_grid[output_grid == 2] = 5
    output_grid[output_grid == 3] = 5
    

    return output_grid
```

