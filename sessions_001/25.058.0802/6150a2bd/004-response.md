# 6150a2bd • 004 • refine_coder

---
```python
"""
The input grid is rotated 90 degrees counter-clockwise to produce the output grid. The values, which correspond to colors per a color map, don't change, only their position in the grid changes.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

