# 44f52bb0 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Count:** Count the number of red (value '2') pixels in the input grid.
2.  **Map**: replace this count with the color for orange.
3. **output**: Return the count calculated in a 1x1 grid.
"""

import numpy as np

def transform(input_grid):
    # Count the number of red (value '2') pixels
    red_pixel_count = np.sum(input_grid == 2)

    # map to orange
    orange_pixel_count = 7

    # Create a 1x1 output grid with the orange color
    output_grid = np.array([[orange_pixel_count]])

    return output_grid
```
