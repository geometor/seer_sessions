# 6150a2bd • 008 • example_1 • investigate_coder

---
```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the 3x3 grid. Each element in the input grid is moved to its new position in the output grid as if the entire grid were rotated. The values/colors of the individual cells are preserved, only their position changes.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Initialize the output grid as a copy of the input array.
    output_array = np.copy(input_array)
    
    # use numpys built in rot90 function
    output_array = np.rot90(input_array, k=1) # k=1 for 90-degree CCW rotation


    return output_array.tolist() # convert back
```
