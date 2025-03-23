```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Convert the NumPy array back to a list of lists
    output_grid = rotated_array.tolist()

    return output_grid
```