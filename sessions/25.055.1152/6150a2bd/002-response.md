# 6150a2bd • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a 180-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees clockwise.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.
    
    Returns:
        list of lists: The rotated output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Rotate the array by 180 degrees clockwise, which is equivalent to two 90-degree rotations
    rotated_array = np.rot90(input_array, 2)

    # Convert the rotated array back to a list of lists
    output_grid = rotated_array.tolist()

    return output_grid
```
