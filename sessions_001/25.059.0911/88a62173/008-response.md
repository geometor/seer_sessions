# 88a62173 • 008 • refine_coder

---
```python
"""
The transformation extracts the top-left 2x2 subgrid from the input grid. 
Regardless of the input grid's dimensions, the output grid is always a 2x2 
grid containing the color values from the corresponding top-left section 
of the input. If the input dimensions are smaller than 2x2 in either 
direction, the available pixels are used, and the missing pixels are not 
considered, resulting in a smaller output.
In this set of examples, the output will always be a 2 x 2 section of gray (5) pixels.
"""

import numpy as np

def transform(input_grid):
    # Create a NumPy array from the input grid for easier manipulation.
    input_np = np.array(input_grid)

    # Extract the top-left 2x2 sub-grid using array slicing.
    output_np = input_np[:2, :2]

    # Convert the NumPy array back to a list.
    output_grid = output_np.tolist()

    return output_grid
```

