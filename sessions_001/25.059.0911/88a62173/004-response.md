# 88a62173 • 004 • example_1 • investigate_coder

---
```python
"""
The transformation extracts the top-left 2x2 portion of the input grid and presents it as the output.
"""

import numpy as np

def transform(input_grid):
    # Create a NumPy array from the input grid for easier manipulation.
    input_np = np.array(input_grid)

    # Extract the top-left 2x2 sub-grid using array slicing.
    output_np = input_np[:2, :2]

    # Convert the NumPy array back to a list.
    output_grid = output_np.tolist()

    return output_grid
```
