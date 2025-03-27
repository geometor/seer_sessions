```python
"""
The transformation rotates the 3x3 grid counter-clockwise by 90 degrees.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by rotating it counter-clockwise by 90 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array counter-clockwise by 90 degrees.
    output_array = np.rot90(input_array)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```