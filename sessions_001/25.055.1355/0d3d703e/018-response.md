# 0d3d703e • 018 • refine_coder

---
```python
"""
The transformation rule is a global color substitution:

1.  Every gray pixel (value 5) in the input grid is replaced with a blue pixel (value 1).
2.  Every azure pixel (value 8) in the input grid is replaced with a maroon pixel (value 9).
3.  Every magenta pixel (value 6) in the input grid is replaced with a red pixel (value 2).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Apply the color substitution rules.
    output_grid[input_grid == 5] = 1  # Replace gray (5) with blue (1)
    output_grid[input_grid == 8] = 9  # Replace azure (8) with maroon (9)
    output_grid[input_grid == 6] = 2  # Replace magenta (6) with red (2)

    return output_grid
```

