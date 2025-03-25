```python
"""
The transformation rule swaps the columns. Specifically the second column in the input becomes the first column of the output. The first column of the input becomes the second column of the output, and the third columns remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Swap the first and second columns
    output_grid[:, 0] = input_grid[:, 1]  # Second column of input to first column of output
    output_grid[:, 1] = input_grid[:, 0]  # First column of input to second column of output
    # output_grid[:, 2] = input_grid[:, 2] # Third column remains the same (optional, for clarity)
    
    return output_grid
```