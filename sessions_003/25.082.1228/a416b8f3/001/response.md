```python
"""
The transformation rule is to duplicate the input grid horizontally.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Duplicate the input array horizontally
    output_array = np.concatenate((input_array, input_array), axis=1)

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```