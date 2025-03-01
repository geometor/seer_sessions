# 6fa7a44f • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is to repeat the input grid vertically. Specifically, the entire input grid is duplicated once and placed directly below the original grid, creating an output grid with twice the height of the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.concatenate((input_grid, input_grid), axis=0)

    # change output pixels (in this case, no further changes are needed)

    return output_grid
```

