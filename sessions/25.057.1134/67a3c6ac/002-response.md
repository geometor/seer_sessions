# 67a3c6ac • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is transformed into the output grid by rotating the entire grid 90 degrees clockwise.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise.
    output_array = np.rot90(input_array, k=-1)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    
    return output_grid
```
