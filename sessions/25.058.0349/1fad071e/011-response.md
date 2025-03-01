# 1fad071e • 011 • refine_coder

---
```python
"""
Iterates through each row of the input grid and selects the row if it contains at least one blue (value 1) pixel.
If multiple rows qualify, it picks the first one encountered. If no rows qualify then an error.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array for easier processing
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for i in range(rows):
        # Check if the current row contains any blue pixels
        if np.any(input_grid[i, :] == 1):
            # If it does, return this row as the output
            return input_grid[i, :]

    # Should never get here based on the prompt and the examples
    raise ValueError("No rows found containing blue pixels.")
```

