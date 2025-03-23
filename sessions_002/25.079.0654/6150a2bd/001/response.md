```python
"""
Rotate the input grid 90 degrees counter-clockwise.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    rotated_array = np.rot90(input_array)
    
    # the numpy rot90 function does the rotation and transpose in one step

    return rotated_array.tolist()
```