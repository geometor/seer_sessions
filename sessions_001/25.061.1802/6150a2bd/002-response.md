# 6150a2bd • 002 • example_2 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    output_array = np.rot90(input_array, k=-1)  # k=-1 rotates 90 degrees clockwise

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
