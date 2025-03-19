# 44f52bb0 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify** the non-zero color values present in the input grid.
2.  Sum the non zero values in the input
3.   **Return** the sum
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Find all non-zero values in the input array.
    non_zero_values = input_array[input_array != 0]
    
    sum_non_zero = np.sum(non_zero_values)

    return sum_non_zero
```

