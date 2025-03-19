# ed36ccf7 • 014 • example_3 • investigate_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise to produce the output grid. The positions of the white (0) and maroon (9) pixels are rearranged according to this rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)
    
    # Rotate the array 90 degrees clockwise.
    output_array = np.rot90(input_array, k=-1)
    
    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()
    
    return output_grid
```
