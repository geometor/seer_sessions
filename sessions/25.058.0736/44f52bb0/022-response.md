# 44f52bb0 • 022 • example_5 • investigate_coder

---
```python
"""
Counts the number of non-white pixels in the input grid and transforms that count to produce the output value.
In this case the transformation is count * 2 - 1 .
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count the number of non-white (non-zero) pixels.
    non_white_count = np.count_nonzero(input_array)

    # Apply a transformation to the count.  We are guessing based on limited
    # information. example: count * 2 - 1
    output_value = non_white_count * 2 - 1

    return output_value
```
