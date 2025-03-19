# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array for easier manipulation.
    input_np = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise.
    output_np = np.rot90(input_np, k=-1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_np.tolist()

    return output_grid
```
