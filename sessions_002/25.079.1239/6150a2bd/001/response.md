```python
"""
The input grid is transformed into the output grid by performing a 90 degree counter-clockwise rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array, k=-1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```
