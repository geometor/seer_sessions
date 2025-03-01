# 44f52bb0 • 008 • example_2 • investigate_coder

---
```python
"""
Counts the number of red pixels (value '2') in the input grid, multiplies this count by 2, and adds 1 to produce the final output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to output a single number.
    
    Args:
      input_grid: A 2D numpy array representing the input grid.

    Returns:
       A single integer representing the output.    
    """
    # Count the number of pixels with value 2 (red pixels).
    red_count = np.count_nonzero(input_grid == 2)

    # Calculate the output: (number of 2s) * 2 + 1
    output_value = (red_count * 2) + 1

    return output_value
```
