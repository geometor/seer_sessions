# 44f52bb0 • 006 • refine_coder

---
```python
"""
Counts the number of red (value '2') pixels in the input grid.
Creates an output grid which is a single column with height equal to the red pixel count.
All cells in the output grid are grey (value '5').
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Count the number of red (2) pixels.
    red_count = np.count_nonzero(input_array == 2)

    # Create an output grid of size red_count x 1, filled with grey (5).
    output_grid = np.full((red_count, 1), 5)

    return output_grid.tolist() # convert back to list of lists
```

