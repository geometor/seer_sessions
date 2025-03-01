# 8be77c9e • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is a vertical reflection of the input grid. The output is the original grid with its vertically mirrored copy appended below it.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reflect the input array vertically.
    reflected_array = np.flipud(input_array)

    # Concatenate the original and reflected arrays vertically.
    output_array = np.concatenate((input_array, reflected_array), axis=0)

    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()

    return output_grid
```
