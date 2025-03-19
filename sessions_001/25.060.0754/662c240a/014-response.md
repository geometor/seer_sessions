# 662c240a • 014 • example_2 • investigate_coder

---
```python
"""
The program extracts a 3x3 sub-grid from the input grid, specifically rows 4-6.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Extract rows 4-6 (index 3-5 in Python indexing) to create output array.
    output_array = input_array[3:6, :]

    # convert back to list 
    output_grid = output_array.tolist()

    return output_grid
```
