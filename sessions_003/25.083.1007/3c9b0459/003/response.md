```python
"""
The transformation rule is a 90-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    rotated_array = np.rot90(input_array, k=-1)  # k=-1 for clockwise rotation

    # Convert the NumPy array back to a list of lists.
    output_grid = rotated_array.tolist()

    return output_grid
```