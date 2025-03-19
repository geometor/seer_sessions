# 44f52bb0 • 016 • example_4 • investigate_coder

---
```python
"""
Counts the occurrences of the value '2' (red) in the input grid. If the count is 2, the output is a 1x1 grid with the value '1' (blue).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid.  Start with a default value, we'll change if conditions are met.
    output_grid = np.array([[0]])

    # Count the occurrences of '2' in the input grid.
    count_of_2 = np.count_nonzero(input_grid == 2)

    # If the count is 2, set the output to 1.
    if count_of_2 == 2:
        output_grid = np.array([[1]])

    return output_grid
```

