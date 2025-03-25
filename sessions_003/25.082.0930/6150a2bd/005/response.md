```python
"""
The input grid is rotated 90 degrees clockwise to produce the output grid. The colors of each pixel are maintained during the rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a numpy array
    input_np = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    output_np = np.rot90(input_np, k=-1)  # k=-1 for 90-degree clockwise rotation

    # Convert the numpy array back to a list
    output_grid = output_np.tolist()

    return output_grid
```