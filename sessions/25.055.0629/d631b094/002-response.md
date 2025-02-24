# d631b094 • 002 • example_1 • investigate_coder

---
```python
"""
The output counts the number of rows with at least one blue pixel, N, and returns a 1xN grid filled with 1s (blue).
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier processing.
    input_array = np.array(input_grid)

    # Find rows containing at least one blue pixel (value 1).
    rows_with_blue = np.any(input_array == 1, axis=1)

    # Count the number of such rows.
    num_rows_with_blue = np.sum(rows_with_blue)

    # Create an output grid of size 1xN, filled with 1s (blue).
    output_grid = np.ones((1, num_rows_with_blue), dtype=int)
    
    return output_grid.tolist()
```
