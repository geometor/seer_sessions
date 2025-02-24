# ed36ccf7 • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule identifies columns in the input grid containing magenta (6) pixels. 
These columns are entirely filled with magenta in the output grid. 
All other columns in the output grid are filled with white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find columns with magenta (6) pixels
    magenta_cols = np.where(input_grid == 6)[1]

    # Fill corresponding output columns with magenta
    for col in magenta_cols:
        output_grid[:, col] = 6
        
    # output grid is initialized to 0, so other values are already white

    return output_grid.tolist()
```
