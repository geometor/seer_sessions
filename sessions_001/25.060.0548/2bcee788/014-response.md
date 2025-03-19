# 2bcee788 • 014 • refine_coder

---
```python
"""
1.  **Background Replacement:** Change all white pixels (color 0) in the input grid to green pixels (color 3).
2.  **Color Transformation:** Change all red pixels (color 2) in the input grid to magenta pixels (color 6).
3.  **Preservation:** Keep all other colored pixels the same. Specifically, magenta pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change output pixels 
    # Replace all white (0) pixels with green (3)
    output_grid[output_grid == 0] = 3

    # Replace all red (2) pixels with magenta (6)
    output_grid[output_grid == 2] = 6

    # Magenta (6) pixels remain unchanged

    return output_grid
```
