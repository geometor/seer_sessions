# 2dee498d • 005 • refine_coder

---
```python
"""
The transformation rule is to select the first four columns of the input grid to produce the output grid. The height of the output grid is the same as the height of the input grid. The width of the output grid is always 4.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Get the number of rows and columns of the input array.
    rows, cols = input_array.shape

    # Create a new array consisting of the first four columns of the input array.
    output_array = input_array[:, :4]

    # Convert the output array to a list.
    output_grid = output_array.tolist()
    
    return output_grid
```

