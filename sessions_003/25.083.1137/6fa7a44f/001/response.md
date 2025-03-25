```python
"""
The input grid is repeated and inverted to construct the output grid.
Specifically, the input is repeated once, inverted vertically, and then repeated again at the very beginning.
"""

import numpy as np

def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)

    # Copy the original
    original_copy = np.copy(input_array)

    # Reverse the order of rows (vertical flip)
    reversed_copy = np.flipud(input_array)
    
    #duplicate
    double_original = np.concatenate((original_copy, original_copy), axis=0)

    # Combine the original and reversed copies to create output
    output_array = np.concatenate((reversed_copy, original_copy), axis=0)

    return output_array.tolist()
```