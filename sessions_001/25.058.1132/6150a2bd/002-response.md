# 6150a2bd • 002 • example_2 • investigate_coder

---
```python
"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid. Each cell's value (color) in the input grid is moved to the corresponding cell's position in the output grid after the rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the rotated output grid.
    """
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise
    output_array = np.rot90(input_array)

    # Convert the NumPy array back to a list of lists.  The ARC
    # framework uses lists of lists for grid, even though numpy array
    # is generally easier and more efficient to work with
    output_grid = output_array.tolist()
    
    return output_grid
```
