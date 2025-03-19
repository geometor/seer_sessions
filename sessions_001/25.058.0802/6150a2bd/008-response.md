# 6150a2bd • 008 • example_2 • investigate_coder

---
```python
"""
1. Rotate the entire input grid 90 degrees clockwise.
2. Maintain the number value and positioning, and change only the color based on the color mapping
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.rot90(input_grid, k=-1)

    # change output pixels - none to change, this is a simple rotation task

    return output_grid.tolist()
```
