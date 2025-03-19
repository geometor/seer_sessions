# beb8660c • 018 • refine_coder

---
```python
"""
The input grid is rotated 90 degrees clockwise.  An azure diagonal line is then drawn
from the new top-left corner to the new bottom-right corner.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)  # k=-1 for 90 degrees clockwise

    # Create a copy to serve as the output (to draw the line on)
    output_array = np.copy(rotated_array)

    # Get dimensions of the rotated array
    rows, cols = output_array.shape

    # Draw the azure diagonal line
    for i in range(min(rows, cols)):
        output_array[i, i] = 8  # 8 is the color code for azure

    return output_array.tolist()
```
