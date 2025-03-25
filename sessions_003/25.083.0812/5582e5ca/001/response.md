```python
"""
1.  **Examine the Input Grid:** Analyze the 3x3 input grid and identify all unique digits present.
2.  **Determine the Repeated Digit** The right-most digit of the first row will become the output.
3.  **Construct the Output Grid:** Create a new 3x3 grid. Fill every cell of this new grid with the repeating digit identified in step 2.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Determine the repeated digit
    repeated_digit = input_grid[0][-1]

    # change output pixels
    output_grid[:] = repeated_digit

    return output_grid
```
