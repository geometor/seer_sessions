# 3c9b0459 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule is a 90-degree clockwise rotation of the entire grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    """
    # Convert the input list of lists to a NumPy array.  NumPy is efficient for matrix operations.
    input_np = np.array(input_grid)

    # Use NumPy's rot90 function to rotate the grid.
    # The 'k=-1' argument specifies a 90-degree clockwise rotation.
    output_np = np.rot90(input_np, k=-1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_np.tolist()
    
    return output_grid
```
