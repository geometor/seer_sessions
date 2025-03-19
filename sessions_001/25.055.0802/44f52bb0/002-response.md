# 44f52bb0 • 002 • example_1 • investigate_coder

---
```python
"""
Counts the number of red (2) pixels in the input grid.
If the count is greater than zero, output a 1x1 grid with a blue (1) pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of red pixels (value 2).
    red_count = np.sum(input_array == 2)

    # Create the output grid.
    if red_count > 0:
        output_grid = [[1]]  # Output a 1x1 grid with a blue pixel (1).
    else:
        output_grid = [[0]]  # Default to the original grid if needed

    return output_grid
```

