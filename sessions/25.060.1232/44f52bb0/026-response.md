# 44f52bb0 • 026 • example_6 • investigate_coder

---
```python
"""
Counts the number of red pixels (value 2) in the input grid, multiplies this count by 2, and adds 1 to produce the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to produce a single-value output.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        int: The calculated output value.
    """
    # Count the number of red pixels (value 2).
    red_count = np.count_nonzero(input_grid == 2)

    # Calculate the output value: red_count * 2 + 1.
    output_value = red_count * 2 + 1

    return output_value
```

