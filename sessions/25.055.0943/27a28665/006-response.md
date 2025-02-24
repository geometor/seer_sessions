# 27a28665 • 006 • refine_coder

---
```python
"""
Checks if the input grid contains any gray (5) pixels. If gray pixels are
present, the output is a 1x1 grid containing blue (1). If no gray pixels are
present, the output is a 1x1 grid containing white/background (0).
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Check for the presence of gray (5) pixels.
    gray_pixels_exist = np.any(input_array == 5)

    # Create the output grid based on the presence of gray pixels.
    if gray_pixels_exist:
        output_grid = [[1]]  # Output is blue (1) if gray is present.
    else:
        output_grid = [[0]]  # Output is white (0) if gray is absent.

    return output_grid
```
