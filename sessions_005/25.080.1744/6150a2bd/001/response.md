```python
"""
Rotate the input grid counter-clockwise by 90 degrees.
Invert columns.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the input array counter-clockwise by 90 degrees.
    rotated_array = np.rot90(input_array, k=1)

    # Invert Columns: Reverse the order of rows to flip vertically.
    output_array = np.flipud(rotated_array)
    
    # Convert output_array to list format.
    output_grid = output_array.tolist()

    return output_grid
```