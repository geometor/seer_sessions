# 44f52bb0 • 020 • example_5 • investigate_coder

---
```python
"""
The output is a 1x1 grid. The value of the single cell in the output grid is the number of red (2) pixels in the input grid, plus one and colored orange (7).
"""

import numpy as np

def transform(input_grid):
    # Count the number of red (2) pixels.
    red_pixel_count = np.sum(input_grid == 2)

    # Add one to the count.
    output_value = red_pixel_count + 1

    # Create a 1x1 output grid with the calculated value and make it orange.
    output_grid = np.array([[output_value]])
    
    return output_grid
```
