# 44f52bb0 • 010 • example_3 • investigate_coder

---
```python
"""
Counts the number of red pixels in the input grid, divides that number by two,
and returns a 1x1 grid with the resulting value.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a grid by counting red pixels, dividing by two, and outputting the result.
    """
    # Count the red pixels (value 2).
    red_count = np.sum(input_grid == 2)

    # Divide by two
    output_value = red_count // 2
    
    # Create the 1x1 output grid.
    output_grid = np.array([[output_value]])

    return output_grid
```
