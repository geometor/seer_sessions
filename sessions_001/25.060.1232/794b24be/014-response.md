# 794b24be • 014 • example_3 • investigate_coder

---
```python
"""
Transforms a grid by changing blue (1) pixels to red (2) in a top-left biased manner,
and preserving white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.zeros_like(input_grid)  # Initialize output grid with zeros

    # Find the top-leftmost blue pixel
    blue_pixels = np.argwhere(input_grid == 1)
    
    if len(blue_pixels)>0:
        top_left_blue = blue_pixels[0]
        output_grid[0,0]=2
        if top_left_blue[1]<2:
           output_grid[0,1]=2

    return output_grid
```

