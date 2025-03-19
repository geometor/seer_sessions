# 94f9d214 • 022 • example_4 • investigate_coder

---
```python
"""
Extracts a 4x4 subgrid from the top-left of the input grid.
Replaces all instances of '3' in the subgrid with '2'.
The result is the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Extract the 4x4 subgrid from the top-left.
    subgrid = input_grid[:4, :4]

    # Create a copy to serve as the output, so we don't modify the original.
    output_grid = np.copy(subgrid)

    # Replace all 3s with 2s in the output grid.
    output_grid[output_grid == 3] = 2
    
    output_grid[output_grid == 1] = 0

    return output_grid
```
