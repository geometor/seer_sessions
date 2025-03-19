# 67a3c6ac • 014 • example_3 • investigate_coder

---
```python
"""
The transformation involves a reflection of the input grid. It can be viewed in two equivalent ways:

1. First, reflect the grid vertically (across a vertical axis). Then, rotate the reflected grid by 180 degrees.
2. Reflect the grid across the main diagonal (from top-left to bottom-right).

Both procedures lead to the same output. The code below implements the second, simpler method.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it across the main diagonal.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Reflect across main diagonal by transposing the array
    output_array = input_array.T

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
```
